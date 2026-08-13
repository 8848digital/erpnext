# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt


import frappe
from frappe.tests.utils import FrappeTestCase

from .supplier_scorecard_criteria import get_criteria_list, get_variables

class TestSupplierScorecardCriteria(FrappeTestCase):
	def test_variables_exist(self):
		for d in test_good_criteria:
			frappe.get_doc(d).insert()

		self.assertRaises(frappe.ValidationError, frappe.get_doc(test_bad_criteria[0]).insert)

	def test_formula_validate(self):
		self.assertRaises(frappe.ValidationError, frappe.get_doc(test_bad_criteria[1]).insert)
		self.assertRaises(frappe.ValidationError, frappe.get_doc(test_bad_criteria[2]).insert)

	def test_creteria_list_TC_B_179(self):
		criteria_name = frappe.get_doc(
			{
				"doctype": "Supplier Scorecard Criteria",
				"criteria_name": "test supplier cretiria" + frappe.generate_hash(length=4),
				"max_score": 100,
				"formula": "10",
			}
		).insert(ignore_permissions=True)

		creteria_list = get_criteria_list()
		self.assertTrue(creteria_list)

		variables = get_variables(criteria_name.name)
		self.assertFalse(variables)


test_good_criteria = [
	{
		"name": "Delivery",
		"weight": 40.0,
		"doctype": "Supplier Scorecard Criteria",
		"formula": "(({cost_of_on_time_shipments} / {tot_cost_shipments}) if {tot_cost_shipments} > 0 else 1 )* 100",
		"criteria_name": "Delivery",
		"max_score": 100.0,
	},
]

test_bad_criteria = [
	{
		"name": "Fake Criteria 1",
		"weight": 40.0,
		"doctype": "Supplier Scorecard Criteria",
		"formula": "(({fake_variable} / {tot_cost_shipments}) if {tot_cost_shipments} > 0 else 1 )* 100",  # Invalid variable name
		"criteria_name": "Fake Criteria 1",
		"max_score": 100.0,
	},
	{
		"name": "Fake Criteria 2",
		"weight": 40.0,
		"doctype": "Supplier Scorecard Criteria",
		"formula": "(({cost_of_on_time_shipments} / {tot_cost_shipments}))* 100",  # Force 0 divided by 0
		"criteria_name": "Fake Criteria 2",
		"max_score": 100.0,
	},
	{
		"name": "Fake Criteria 3",
		"weight": 40.0,
		"doctype": "Supplier Scorecard Criteria",
		"formula": "(({cost_of_on_time_shipments} {cost_of_on_time_shipments} / {tot_cost_shipments}))* 100",  # Two variables beside eachother
		"criteria_name": "Fake Criteria 3",
		"max_score": 100.0,
	},
]
