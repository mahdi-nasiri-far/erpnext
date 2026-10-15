# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

"""Iran VAT report (گزارش مالیات بر ارزش افزوده).

Summarises the value added tax and duties charged on sales and purchases of a period,
in the layout of the quarterly VAT return (اظهارنامه مالیات بر ارزش افزوده):

	* فروش کالا و خدمات مشمول (۹٪ مالیات + ۱٪ عوارض)
	* فروش صادراتی با نرخ صفر و فروش معاف از مالیات
	* خرید کالا و خدمات مشمول (اعتبار مالیاتی)
	* خالص مالیات و عوارض قابل پرداخت یا اعتبار مالیاتی

Invoices are classified with the Tax Category (صادرات / معاف / داخلی) set by the
tax templates that ship with the Iranian setup wizard, and the rate is read from the
taxes and charges rows of each invoice.
"""

import frappe
from frappe import _
from frappe.utils import flt, getdate

SALES = "sales"
PURCHASE = "purchase"

TAXABLE = "taxable"
ZERO_RATED = "zero_rated"
EXEMPT = "exempt"
UNCLASSIFIED = "unclassified"

# Tax Category values used by the Iranian tax templates (setup wizard)
ZERO_RATED_CATEGORIES = {"صادرات", "export", "zero rated", "zero-rated"}
EXEMPT_CATEGORIES = {"معاف", "معاف از مالیات", "exempt"}


def execute(filters=None):
	return IranVATReport(filters).run()


class IranVATReport:
	def __init__(self, filters=None):
		self.filters = frappe._dict(filters or {})
		self.currency = None

	def run(self):
		self.validate_filters()
		self.currency = frappe.get_cached_value("Company", self.filters.company, "default_currency")

		invoices = self.get_invoices()
		taxes = self.get_taxes(list(invoices))
		summary = summarize_invoices(invoices, taxes)

		return get_columns(), get_data(summary, self.currency)

	def validate_filters(self):
		if not self.filters.get("company"):
			frappe.throw(_("Please set Company"))

		if not self.filters.get("from_date") or not self.filters.get("to_date"):
			frappe.throw(_("Please set From Date and To Date"))

		if getdate(self.filters.from_date) > getdate(self.filters.to_date):
			frappe.throw(_("From Date cannot be after To Date"))

		frappe.has_permission("Company", doc=self.filters.company, throw=True)

	def get_invoices(self):
		"""Submitted invoices of the period, per doctype (kept in insertion order)."""
		invoices = frappe._dict()

		for doctype, kind, party_field in (
			("Sales Invoice", SALES, "customer"),
			("Purchase Invoice", PURCHASE, "supplier"),
		):
			filters = [["docstatus", "=", 1], ["company", "=", self.filters.company]]
			if self.filters.get("from_date"):
				filters.append(["posting_date", ">=", self.filters.from_date])
			if self.filters.get("to_date"):
				filters.append(["posting_date", "<=", self.filters.to_date])

			rows = frappe.get_list(
				doctype,
				filters=filters,
				fields=[
					"name",
					"posting_date",
					"tax_category",
					"is_return",
					"net_total",
					f"{party_field} as party",
				],
				order_by="posting_date",
				limit_page_length=0,
			)

			for row in rows:
				row["kind"] = kind
				invoices[row["name"]] = row

		return invoices

	def get_taxes(self, invoice_names):
		"""Tax rows of the given invoices, keyed by invoice name."""
		taxes = frappe._dict()
		if not invoice_names:
			return taxes

		for tax_doctype in ("Sales Taxes and Charges", "Purchase Taxes and Charges"):
			rows = frappe.db.sql(
				f"""
				select parent, rate, tax_amount, charge_type
				from `tab{tax_doctype}`
				where parent in %(parents)s
				""",
				{"parents": invoice_names},
				as_dict=True,
			)
			for row in rows:
				taxes.setdefault(row["parent"], []).append(row)

		return taxes


def summarize_invoices(invoices, taxes):
	"""Group invoices into (kind, classification, rate) buckets.

	Pure function: `invoices` is a mapping name -> invoice dict (with `kind`,
	`tax_category` and `net_total`), `taxes` a mapping name -> list of tax rows
	(`rate` and `tax_amount`). Returns a dict of buckets with the invoice count,
	the taxable amount and the tax + duties amount.
	"""
	buckets = frappe._dict()

	for name, invoice in invoices.items():
		tax_rows = taxes.get(name) or []
		classification, rate = classify_invoice(invoice, tax_rows)

		key = (invoice.get("kind"), classification, rate)
		bucket = buckets.setdefault(
			key, frappe._dict(vouchers=0, taxable_amount=0.0, tax_amount=0.0)
		)

		bucket["vouchers"] += 1
		bucket["taxable_amount"] += flt(invoice.get("net_total"))
		bucket["tax_amount"] += sum(flt(row.get("tax_amount")) for row in tax_rows)

	return buckets


def classify_invoice(invoice, tax_rows):
	"""Return (classification, effective rate) of an invoice.

	Rates are read from the taxes and charges rows; invoices with no tax rows are
	classified with their Tax Category (صادرات = zero rated, معاف = exempt).
	"""
	rates = [flt(row.get("rate")) for row in tax_rows if flt(row.get("rate"))]
	if rates:
		return TAXABLE, flt(sum(rates), 2)

	if any(flt(row.get("tax_amount")) for row in tax_rows):
		# eg. an "Actual" charge, where the rate is not maintained on the row
		return TAXABLE, 0.0

	category = str(invoice.get("tax_category") or "").strip().lower()
	if category in ZERO_RATED_CATEGORIES:
		return ZERO_RATED, 0.0
	if category in EXEMPT_CATEGORIES:
		return EXEMPT, 0.0
	if tax_rows:
		# a tax row without a rate (eg. an actual charge) is treated as zero rated
		return ZERO_RATED, 0.0

	return UNCLASSIFIED, 0.0


def get_bucket_rows(buckets, kind):
	"""Rows of one side of the return, taxable buckets first (by rate)."""
	classification_order = {
		TAXABLE: 0,
		ZERO_RATED: 1,
		EXEMPT: 2,
		UNCLASSIFIED: 3,
	}

	keys = [
		key
		for key in buckets
		if key[0] == kind and (buckets[key]["vouchers"] or buckets[key]["tax_amount"])
	]
	keys.sort(key=lambda key: (classification_order.get(key[1], 9), -key[2]))

	return [(key, buckets[key]) for key in keys]


def get_data(summary, currency=None):
	data = []

	sales_rows = get_bucket_rows(summary, SALES)
	purchase_rows = get_bucket_rows(summary, PURCHASE)

	sales_taxable = sales_tax = 0.0
	purchase_taxable = purchase_tax = 0.0

	data.append(make_section_row(_("Sales of Goods and Services")))
	for key, bucket in sales_rows:
		data.append(make_bucket_row(key, bucket, currency))
		sales_taxable += bucket["taxable_amount"]
		sales_tax += bucket["tax_amount"]

	data.append(
		make_row(
			_("Total Sales"),
			vouchers=sum(bucket["vouchers"] for _, bucket in sales_rows),
			taxable_amount=sales_taxable,
			tax_amount=sales_tax,
			currency=currency,
			bold=True,
		)
	)
	data.append({})

	data.append(make_section_row(_("Purchases of Goods and Services")))
	for key, bucket in purchase_rows:
		data.append(make_bucket_row(key, bucket, currency))
		purchase_taxable += bucket["taxable_amount"]
		purchase_tax += bucket["tax_amount"]

	data.append(
		make_row(
			_("Total Purchases"),
			vouchers=sum(bucket["vouchers"] for _, bucket in purchase_rows),
			taxable_amount=purchase_taxable,
			tax_amount=purchase_tax,
			currency=currency,
			bold=True,
		)
	)
	data.append({})

	data.append(make_section_row(_("VAT and Duties Settlement")))
	data.append(
		make_row(
			_("Output VAT and Duties (Payable)"),
			tax_amount=sales_tax,
			currency=currency,
		)
	)
	data.append(
		make_row(
			_("Input VAT and Duties (Tax Credit)"),
			tax_amount=purchase_tax,
			currency=currency,
		)
	)

	net_tax = flt(sales_tax - purchase_tax, 2)
	if net_tax >= 0:
		data.append(
			make_row(
				_("Net VAT and Duties Payable"),
				tax_amount=net_tax,
				currency=currency,
				bold=True,
			)
		)
	else:
		data.append(
			make_row(
				_("Tax Credit Carried Forward"),
				tax_amount=abs(net_tax),
				currency=currency,
				bold=True,
			)
		)

	return data


def make_section_row(label):
	return {"description": label, "bold": 1, "is_section": 1}


def make_bucket_row(key, bucket, currency=None):
	kind, classification, rate = key
	label = get_bucket_label(kind, classification)

	return make_row(
		label,
		rate=rate,
		vouchers=bucket["vouchers"],
		taxable_amount=bucket["taxable_amount"],
		tax_amount=bucket["tax_amount"],
		currency=currency,
	)


def get_bucket_label(kind, classification):
	if kind == SALES:
		return {
			TAXABLE: _("Taxable Sales"),
			ZERO_RATED: _("Export Sales (Zero Rated)"),
			EXEMPT: _("Exempt Sales"),
			UNCLASSIFIED: _("Sales without Tax Category"),
		}[classification]

	return {
		TAXABLE: _("Taxable Purchases"),
		ZERO_RATED: _("Zero Rated Purchases (Imports)"),
		EXEMPT: _("Exempt Purchases"),
		UNCLASSIFIED: _("Purchases without Tax Category"),
	}[classification]


def make_row(
	description,
	rate=None,
	vouchers=0,
	taxable_amount=0.0,
	tax_amount=0.0,
	currency=None,
	bold=False,
):
	row = {
		"description": description,
		"vouchers": vouchers,
		"taxable_amount": flt(taxable_amount, 2),
		"tax_amount": flt(tax_amount, 2),
		"total": flt(flt(taxable_amount) + flt(tax_amount), 2),
		"currency": currency,
	}
	if rate:
		row["rate"] = rate
	if bold:
		row["bold"] = 1

	return row


def get_columns():
	return [
		{
			"fieldname": "description",
			"label": _("Description"),
			"fieldtype": "Data",
			"width": 320,
		},
		{
			"fieldname": "rate",
			"label": _("Tax Rate (%)"),
			"fieldtype": "Percent",
			"width": 100,
		},
		{
			"fieldname": "vouchers",
			"label": _("No. of Invoices"),
			"fieldtype": "Int",
			"width": 110,
		},
		{
			"fieldname": "taxable_amount",
			"label": _("Taxable Amount"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 160,
		},
		{
			"fieldname": "tax_amount",
			"label": _("Tax and Duties"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 160,
		},
		{
			"fieldname": "total",
			"label": _("Total"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 160,
		},
		{
			"fieldname": "currency",
			"label": _("Currency"),
			"fieldtype": "Link",
			"options": "Currency",
			"hidden": 1,
		},
	]
