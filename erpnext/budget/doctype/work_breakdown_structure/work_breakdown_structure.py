# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import (cint, getdate)
from frappe.query_builder.functions import Coalesce, Sum
from frappe import qb
from erpnext.accounts.report.financial_statements import sort_accounts

class WorkBreakdownStructure(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		actual_overall_budget: DF.Currency
		amended_from: DF.Link | None
		assigned_overall_budget: DF.Currency
		available_budget: DF.Currency
		committed_overall_budget: DF.Currency
		company: DF.Link | None
		created_from_project: DF.Check
		gl_account: DF.Link | None
		is_group: DF.Check
		lft: DF.Int
		linked_monthly_distribution: DF.Link | None
		locked: DF.Check
		original_budget: DF.Currency
		overall_budget: DF.Currency
		parent_work_breakdown_structure: DF.Link | None
		project: DF.Link | None
		project_name: DF.Data | None
		project_type: DF.Data | None
		rgt: DF.Int
		wbs_level: DF.Data | None
		wbs_name: DF.Data | None
	# end: auto-generated types

@frappe.whitelist()
def get_children(doctype, parent, project = None, is_root=False):
    parent_fieldname = "parent_" + doctype.lower().replace(" ", "_")
    fields = [
        "CONCAT_WS(' : ', name, wbs_name) as value", 
        "is_group as expandable"
    ]
    filters = " where docstatus < 2 "
    
    if is_root:
        filters += """ and project = '{0}' """.format(project)
        filters += """ and coalesce({0}, '') = '' """.format(parent_fieldname)  # Use coalesce properly
    else:
        parts = parent.split(" : ")
        fields += [parent_fieldname + " as parent"]
        filters += """ and coalesce({0}, '') = '{1}' """.format(parent_fieldname, parts[0])  # Adjusting filter for non-root

    acc = frappe.db.sql("""
        SELECT CONCAT_WS(' : ', name, wbs_name) as value,
            is_group as expandable,
            {0} as parent
        FROM `tab{1}`
        {2} """.format(parent_fieldname, doctype, filters), as_dict=1)
    
    if doctype == "Account":
        sort_accounts(acc, is_root, key="value")

    return acc

def create_warehouse(name, company=None):
	if frappe.db.exists("Warehouse", name):
		return frappe.get_doc("Warehouse", name)

	warehouse = frappe.new_doc("Warehouse")
	warehouse.warehouse_name = name
	warehouse.company = company
	warehouse.insert(ignore_permissions=True)
	return warehouse


@frappe.whitelist()
def add_wbs_from_tree_view(arguments=None):
    from frappe.desk.treeview import make_tree_args
    
    if not arguments:
        arguments = frappe.local.form_dict

    arguments.doctype = "Work Breakdown Structure"
    arguments = make_tree_args(**arguments)

    if arguments.get("parent"):
        parent = arguments.get("parent")
        parts = parent.split(" : ")
        arguments.update({
            "parent": parts[0]
        })

    if arguments.get("parent_work_breakdown_structure"):
        parent = arguments.get("parent_work_breakdown_structure")
        parts = parent.split(" : ")
        arguments.update({
            "parent_work_breakdown_structure": parts[0]
        })

    wbs = frappe.new_doc("Work Breakdown Structure")

    if arguments.get("ignore_permissions"):
        wbs.flags.ignore_permissions = True
        arguments.pop("ignore_permissions")

    wbs.update(arguments)

    if not wbs.parent_work_breakdown_structure:
        wbs.parent_work_breakdown_structure = arguments.get("parent")

    wbs.old_parent = ""
    if cint(wbs.get("is_root")):
        wbs.parent_work_breakdown_structure = None
        wbs.flags.ignore_mandatory = True

    wbs.insert()

    if int(arguments.get("warehouse_required")) == 1:
        create_warehouse(wbs.name, wbs.company)

    return wbs.name


@frappe.whitelist()
def delete_wbs_from_tree_view(wbs):
    if wbs:
        frappe.delete_doc('Work Breakdown Structure',wbs)
        # delete_warehouse(wbs)

def after_insert(self):
    if self.is_wbs == 1:
        data = frappe.new_doc("Work Breakdown Structure")
        data.name = self.name
        print(self.name)
        if "projects" in frappe.get_installed_apps():
            data.project_type = self.project_type
            data.project_name = self.project_name
        data.company = self.company
        data.insert()
        data.submit()
	

@frappe.whitelist()
def check_available_budget(wbs,amt,doctype,txn_date):
        month_name = getdate(txn_date).strftime("%B")
        wbs_doc = frappe.get_doc("Work Breakdown Structure", wbs)
        controls = get_control_actions(wbs_doc.linked_monthly_distribution)
        be = frappe.qb.DocType('Budget Entry')
        dt_action = ""

        query = (
            frappe.qb.from_(be)
            .select(Sum(be.overall_credit - be.overall_debit).as_('sob'))
            .where(
                (be.wbs == wbs_doc.name) &
                (be.voucher_type.isin(["Budget Amendment", "Budget Transfer"]))
            )
        )
        statistical_amt = query.run(as_dict=True)
        
        ab = wbs_doc.available_budget - statistical_amt[0].get("sob") if statistical_amt[0].get("sob") else wbs_doc.available_budget
        cob = wbs_doc.committed_overall_budget
        aob = wbs_doc.actual_overall_budget
        ab_upd = ab
        monthly_ab = get_available_budget_for_month(month_name,wbs_doc.linked_monthly_distribution,wbs_doc.available_budget)
        wbs_id = ""
        if wbs:
            wbs_id = wbs_doc.name
            if doctype in ["Material Request" ,"Stock Entry","Budget Transfer","Budget Amendment", "Expense Claim", "Journal Entry"]:
                dt_action = controls.get("mr_action") 
                ab_upd = monthly_ab - amt
            if doctype in ["Purchase Order","Purchase Receipt"]:
                if doctype == "Purchase Order":
                    dt_action = controls.get("po_action")
                elif doctype == "Purchase Receipt":
                    dt_action = controls.get("pr_action")
                ab_upd = (monthly_ab + cob) - amt
            if doctype in ["Purchase Invoice"]:
                dt_action = controls.get("pi_action")
                ab_upd = (monthly_ab + aob) - amt

        return {"available_bgt":ab_upd,"wbs":wbs_id,"action":dt_action}


def get_available_budget_for_month(month_name,monthly_distribution_name,total_avl_bgt):
    # Fetch the available budget from the WBS record
    if not total_avl_bgt:
        return 0.0

    # Fetch the linked monthly distribution record associated with this WBS
    if not monthly_distribution_name:
        return total_avl_bgt

    # Retrieve the allocation percentage for the specified month from the linked Monthly Distribution
    allocation_percentage = frappe.db.get_value("Distribution Percentage", 
                                                {"parent": monthly_distribution_name, "month": month_name}, 
                                                "allocation")
    if not allocation_percentage:
        return total_avl_bgt

    # Calculate the available budget based on the allocation percentage
    avl_bgt = total_avl_bgt * (allocation_percentage / 100)

    # Return the available budget object
    return  avl_bgt

def get_control_actions(monthly_distribution=None):
    controls = {"mr_action":"Ignore","po_action":"Ignore","pr_action":"Ignore","pi_action":"Ignore"}
    if monthly_distribution:
        md = frappe.get_doc("WBS Monthly Distribution",monthly_distribution)
        if md.applicable_on_material_request:
            controls.update({
                "mr_action":md.action_if_accumulated_monthly_budget_exceeded_on_mr
            })

        if md.applicable_on_purchase_order:
            controls.update({
                "po_action":md.action_if_accumulated_monthly_budget_exceeded_on_po
            })

        if md.applicable_on_booking_actual_expenses:
            controls.update({
                "pi_action":md.action_if_accumulated_monthly_budget_exceeded_on_actual,
                "pr_action":md.action_if_accumulated_monthly_budget_exceeded_on_actual
            })

    return controls
    