# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

"""Iran periodic transactions report (صورت معاملات فصلی - ماده ۱۶۹).

Lists the sales and purchase transactions of a quarter per party, along with the
economic code (کد اقتصادی) and national ID (شناسه ملی) that have to be reported to
the Iranian tax administration (سازمان امور مالیاتی) in the quarterly transaction
statement of Article 169 of the Direct Taxes Act.

The economic code and national ID are the fields added by the Iranian regional setup
(erpnext.regional.iran.setup) and are read defensively: if they are not installed yet
the report simply falls back to the Tax ID (شناسه مالیاتی) of the party.
"""

import frappe
from frappe import _
from frappe.utils import flt, getdate

SALES = "sales"
PURCHASE = "purchase"

SIDE_LABELS = {SALES: "Sales", PURCHASE: "Purchases"}
PERSON_TYPE_LABELS = {"Company": "Legal Entity", "Individual": "Natural Person"}


def execute(filters=None):
	return IranPeriodicTransactions(filters).run()


class IranPeriodicTransactions:
	def __init__(self, filters=None):
		self.filters = frappe._dict(filters or {})
		self.currency = None

	def run(self):
		self.validate_filters()
		self.currency = frappe.get_cached_value("Company", self.filters.company, "default_currency")

		invoices = self.get_invoices()
		taxes = self.get_taxes(list(invoices))
		party_details = self.get_party_details(invoices)

		return get_columns(), get_data(invoices, taxes, party_details, self.currency)

	def validate_filters(self):
		if not self.filters.get("company"):
			frappe.throw(_("Please set Company"))

		if not self.filters.get("from_date") or not self.filters.get("to_date"):
			frappe.throw(_("Please set From Date and To Date"))

		if getdate(self.filters.from_date) > getdate(self.filters.to_date):
			frappe.throw(_("From Date cannot be after To Date"))

		frappe.has_permission("Company", doc=self.filters.company, throw=True)

	def get_invoices(self):
		invoices = frappe._dict()

		for doctype, kind, party_type, party_field in (
			("Sales Invoice", SALES, "Customer", "customer"),
			("Purchase Invoice", PURCHASE, "Supplier", "supplier"),
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
					"net_total",
					"grand_total",
					f"{party_field} as party",
				],
				order_by="posting_date",
				limit_page_length=0,
			)

			for row in rows:
				row["kind"] = kind
				row["party_type"] = party_type
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
				select parent, rate, tax_amount
				from `tab{tax_doctype}`
				where parent in %(parents)s
				""",
				{"parents": invoice_names},
				as_dict=True,
			)
			for row in rows:
				taxes.setdefault(row["parent"], []).append(row)

		return taxes

	def get_party_details(self, invoices):
		"""Name, type and statutory IDs of the parties of the given invoices."""
		parties = frappe._dict()
		for invoice in invoices.values():
			parties.setdefault(invoice["party_type"], set()).add(invoice["party"])

		details = frappe._dict()
		for party_type, names in parties.items():
			fields = ["name", "tax_id"]
			for field in (
				"customer_name" if party_type == "Customer" else "supplier_name",
				"customer_type" if party_type == "Customer" else "supplier_type",
				"iran_economic_code",
				"iran_national_id",
			):
				if field and frappe.db.has_column(party_type, field):
					fields.append(field)

			for row in frappe.get_all(
				party_type, filters={"name": ("in", list(names))}, fields=fields
			):
				details[(party_type, row["name"])] = row

		return details


def aggregate_transactions(invoices, taxes, party_details):
	"""One row per (side, party) with the transaction totals.

	Pure function: `invoices` is a mapping name -> invoice dict (with `kind`,
	`party_type`, `party`, `net_total` and `grand_total`), `taxes` a mapping
	invoice name -> list of tax rows and `party_details` a mapping
	(party_type, party) -> party dict.
	"""
	rows = frappe._dict()

	for name, invoice in invoices.items():
		key = (invoice["kind"], invoice["party_type"], invoice["party"])
		row = rows.setdefault(
			key,
			frappe._dict(vouchers=0, net_total=0.0, tax_amount=0.0, grand_total=0.0),
		)

		row["vouchers"] += 1
		row["net_total"] += flt(invoice.get("net_total"))
		row["grand_total"] += flt(invoice.get("grand_total"))
		row["tax_amount"] += sum(flt(tax.get("tax_amount")) for tax in taxes.get(name) or [])

	return rows


def get_data(invoices, taxes, party_details, currency=None):
	summary = aggregate_transactions(invoices, taxes, party_details)

	kind_order = {SALES: 0, PURCHASE: 1}
	keys = sorted(
		summary, key=lambda key: (kind_order.get(key[0], 9), -summary[key]["grand_total"])
	)

	data = []
	totals = frappe._dict(vouchers=0, net_total=0.0, tax_amount=0.0, grand_total=0.0)

	for key in keys:
		kind, party_type, party = key
		row = summary[key]
		details = party_details.get((party_type, party)) or {}

		data.append(
			{
				"transaction_type": _(SIDE_LABELS[kind]),
				"party_type": party_type,
				"party": party,
				"party_name": details.get("customer_name")
				or details.get("supplier_name")
				or party,
				"person_type": get_person_type(details),
				"economic_code": details.get("iran_economic_code") or details.get("tax_id"),
				"national_id": details.get("iran_national_id"),
				"tax_id": details.get("tax_id"),
				"vouchers": row["vouchers"],
				"net_total": flt(row["net_total"], 2),
				"tax_amount": flt(row["tax_amount"], 2),
				"grand_total": flt(row["grand_total"], 2),
				"currency": currency,
			}
		)

		for field in totals:
			totals[field] += row[field]

	if data:
		data.append({})
		data.append(
			{
				"transaction_type": _("Total"),
				"vouchers": totals["vouchers"],
				"net_total": flt(totals["net_total"], 2),
				"tax_amount": flt(totals["tax_amount"], 2),
				"grand_total": flt(totals["grand_total"], 2),
				"currency": currency,
				"bold": 1,
			}
		)

	return data


def get_person_type(party_details):
	"""حقوقی / حقیقی label of a party, empty when the party has no type."""
	person_type = party_details.get("customer_type") or party_details.get("supplier_type")
	return _(PERSON_TYPE_LABELS[person_type]) if person_type in PERSON_TYPE_LABELS else person_type


def get_columns():
	return [
		{
			"fieldname": "transaction_type",
			"label": _("Transaction Type"),
			"fieldtype": "Data",
			"width": 110,
		},
		{
			"fieldname": "party_type",
			"label": _("Party Type"),
			"fieldtype": "Data",
			"hidden": 1,
		},
		{
			"fieldname": "party",
			"label": _("Party"),
			"fieldtype": "Dynamic Link",
			"options": "party_type",
			"width": 150,
		},
		{
			"fieldname": "party_name",
			"label": _("Party Name"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "person_type",
			"label": _("Person Type"),
			"fieldtype": "Data",
			"width": 100,
		},
		{
			"fieldname": "economic_code",
			"label": _("Economic Code"),
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"fieldname": "national_id",
			"label": _("National ID"),
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"fieldname": "tax_id",
			"label": _("Tax ID"),
			"fieldtype": "Data",
			"width": 150,
			"hidden": 1,
		},
		{
			"fieldname": "vouchers",
			"label": _("No. of Invoices"),
			"fieldtype": "Int",
			"width": 110,
		},
		{
			"fieldname": "net_total",
			"label": _("Net Total"),
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
			"fieldname": "grand_total",
			"label": _("Grand Total"),
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
