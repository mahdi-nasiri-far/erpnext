# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

"""Iran regional setup.

Iranian statutory documents (صورتحساب فروش کالا و خدمات) require the national ID
(شناسه ملی), economic code (کد اقتصادی) and registration number (شماره ثبت) of the
company, customers and suppliers to be printed on the invoice. These are added as
custom fields whenever a company with country "Iran" is created.

The Iranian chart of accounts (طرح حساب‌های نمونه) is shipped as a chart template
and the VAT (مالیات بر ارزش افزوده ۹٪ + عوارض ۱٪) templates are created by the
setup wizard from `country_wise_tax.json`.

The Persian print formats of the financial statements (ترازنامه، صورت سود و زیان و
صورت گردش وجوه نقد) in the Iranian standard layout, with the signature block of the
board, are loaded from `erpnext/regional/print_format` as well.
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

PRINT_FORMATS = (
	"iran_balance_sheet",
	"iran_profit_and_loss_statement",
	"iran_cash_flow_statement",
)


def setup(company=None, patch=True):
	make_custom_fields()
	add_print_formats()


def add_print_formats():
	for print_format in PRINT_FORMATS:
		frappe.reload_doc("regional", "print_format", print_format)


def get_custom_fields():
	national_id = dict(
		fieldname="iran_national_id",
		label="شناسه ملی",
		fieldtype="Data",
		insert_after="tax_id",
		translatable=0,
	)
	economic_code = dict(
		fieldname="iran_economic_code",
		label="کد اقتصادی",
		fieldtype="Data",
		insert_after="iran_national_id",
		translatable=0,
	)
	registration_number = dict(
		fieldname="iran_registration_number",
		label="شماره ثبت",
		fieldtype="Data",
		insert_after="iran_economic_code",
		translatable=0,
	)

	return {
		"Company": [national_id, economic_code, registration_number],
		"Customer": [dict(national_id), dict(economic_code)],
		"Supplier": [dict(national_id), dict(economic_code)],
	}


def make_custom_fields(update=True):
	create_custom_fields(get_custom_fields(), update=update)
