# Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt
import frappe
from frappe.tests.utils import FrappeTestCase

from erpnext.accounts.doctype.payment_entry.test_payment_entry import create_customer
from erpnext.accounts.doctype.pos_closing_entry.pos_closing_entry import make_closing_entry_from_opening


class TestPOSOpeningEntry(unittest.TestCase):
	pass


def create_opening_entry(pos_profile, user):
	entry = frappe.new_doc("POS Opening Entry")
	entry.pos_profile = pos_profile.name
	entry.user = user
	entry.company = pos_profile.company
	entry.period_start_date = frappe.utils.get_datetime()

	balance_details = []
	for d in pos_profile.payments:
		balance_details.append(frappe._dict({"mode_of_payment": d.mode_of_payment}))

	entry.set("balance_details", balance_details)
	entry.submit()

	return entry


def get_mode_of_payment():
	mode = "__Test Mode Payment"
	if not frappe.db.exists("Mode of Payment", mode):
		frappe.get_doc({"doctype": "Mode of Payment", "mode_of_payment": mode}).insert(
			ignore_permissions=True
		)
	return mode
