import frappe
from frappe import _
from pypika import Case
from frappe.query_builder import CustomFunction
from erpnext.budget.report.commited_line_item.cli_columns import get_columns

date_func = CustomFunction("DATE", ["date_str"])

def execute(filters=None):
	columns =  get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_conditions(filters):
	conditions = []
	wbs_doc = frappe.qb.DocType("Work Breakdown Structure")
	if filters.get("wbs"):
		if filters.get("project"):
			if len(filters.get("project")) > 1:
				conditions.append(wbs_doc.project.isin(tuple(list(filters.get("project")))))
			if len(filters.get("project")) == 1:
				conditions.append(wbs_doc.project == filters.get("project")[0])
	else:
		if filters.get("project"):
			if len(filters.get("project")) > 1:
				conditions.append(wbs_doc.project.isin(tuple(list(filters.get("project")))))
			if len(filters.get("project")) == 1:
				conditions.append(wbs_doc.project == filters.get("project")[0])
	if filters.get("project"):
		if filters.get("wbs"):
			if filters.get("show_group_totals"):
				wbs_list = get_all_wbs(filters.get("wbs"))
				if len(wbs_list) > 1:
					wbs_list = tuple(wbs_list)
					conditions.append(wbs_doc.name.isin(wbs_list))
				elif len(wbs_list) == 1:
					wbs_list = wbs_list[0]
					conditions.append(wbs_doc.name == wbs_list)
			else:
				if len(filters.get("wbs"))>1:
					wbs = tuple(filters.get("wbs"))
					conditions.append(wbs_doc.name.isin(wbs))	
				else:
					wbs = filters.get("wbs")[0]
					conditions.append(wbs_doc.name == wbs)
	else:
		if filters.get("wbs"):
			if filters.get("show_group_totals"):
				wbs_list = get_all_wbs(filters.get("wbs"))
				if len(wbs_list) > 1:
					wbs_list = tuple(wbs_list)
					conditions.append(wbs_doc.name.isin(wbs_list))
				elif len(wbs_list) == 1:
					wbs_list = wbs_list[0]
					conditions.append(wbs_doc.name == wbs_list)
			else:
				if len(filters.get("wbs"))>1:
					wbs = tuple(filters.get("wbs"))
					conditions.append(wbs_doc.name.isin(wbs))
				elif len(filters.get("wbs")) == 1:
					wbs = filters.get("wbs")[0]
					conditions.append(wbs_doc.name == wbs)
	return conditions

def get_conditions_for_mr(filters): 
	conditions_mr =[]
	mri = frappe.qb.DocType('Material Request Item')
	mr = frappe.qb.DocType('Material Request')

	if filters.from_date and filters.to_date:
		conditions_mr.append(mr.transaction_date.between(filters.from_date, filters.to_date))
	if filters.voucher_type:
		conditions_mr.append(mri.parenttype == filters.voucher_type)     
	if filters.voucher_name:
		if len(filters.voucher_name) > 1:
			conditions_mr.append(mr.name.isin(tuple(list(filters.project))))
		if len(filters.voucher_name) == 1:
			conditions_mr.append(mr.name == (filters.project)[0])
	if filters.supplier:
		if len(filters.supplier) > 1:
			conditions_mr.append(mr.name.isin(tuple(list(filters.supplier))))
		if len(filters.supplier) == 1:
			conditions_mr.append(mr.name == (filters.supplier)[0])
	if filters.item_code:
		if len(filters.item_code) > 1:
			conditions_mr.append(mri.item_code.isin(tuple(list(filters.item_code))))
		if len(filters.item_code) == 1:
			conditions_mr.append(mri.item_code == (filters.item_code)[0])
	if filters.item_group:
		if len(filters.item_group) > 1:
			conditions_mr.append(mri.item_group.isin(tuple(list(filters.item_group))))
		if len(filters.item_group) == 1:
			conditions_mr.append(mri.item_group == (filters.item_group)[0])

	return conditions_mr

def get_conditions_for_po(filters):
	conditions_po =[]
	poi = frappe.qb.DocType('Purchase Order Item')
	po = frappe.qb.DocType('Purchase Order')

	if filters.from_date and filters.to_date:
		conditions_po.append(po.transaction_date.between(filters.from_date, filters.to_date))
	if filters.voucher_type:
		conditions_po.append(poi.parenttype == filters.voucher_type)     
	if filters.voucher_name:
		if len(filters.voucher_name) > 1:
			conditions_po.append(po.name.isin(tuple(list(filters.project))))
		if len(filters.voucher_name) == 1:
			conditions_po.append(po.name == (filters.project)[0])
	if filters.supplier:
		if len(filters.supplier) > 1:
			conditions_po.append(po.supplier.isin(tuple(list(filters.supplier))))
		if len(filters.supplier) == 1:
			conditions_po.append(po.supplier == (filters.supplier)[0])
	if filters.item_code:
		if len(filters.item_code) > 1:
			conditions_po.append(poi.item_code.isin(tuple(list(filters.item_code))))
		if len(filters.item_code) == 1:
			conditions_po.append(poi.item_code == (filters.item_code)[0])
	if filters.item_group:
		if len(filters.item_group) > 1:
			conditions_po.append(poi.item_group.isin(tuple(list(filters.item_group))))
		if len(filters.item_group) == 1:
			conditions_po.append(poi.item_group == (filters.item_group)[0])

	return conditions_po

def get_all_wbs(wbs):
	all_wbs = []
	if len(wbs) > 1:
		for w in wbs:
			wbs_parent = frappe.get_doc('Work Breakdown Structure',w)
			if wbs_parent:
				all_wbs.append(w)
				child_list =  frappe.db.get_all ("Work Breakdown Structure", {"lft":[">", wbs_parent.get("lft")], "rgt":["<",wbs_parent.get("rgt")]},['name'])
				if child_list:
					for i in  child_list:
						all_wbs.append(i.get("name"))
	elif len(wbs) == 1:
		wbs_parent = frappe.get_doc('Work Breakdown Structure',wbs[0])
		if wbs_parent:
			all_wbs.append(wbs[0])
			child_list =  frappe.db.get_all ("Work Breakdown Structure", {"lft":[">", wbs_parent.get("lft")], "rgt":["<",wbs_parent.get("rgt")]},['name'])
			if child_list:
				for i in  child_list:
					all_wbs.append(i.get("name"))
	
	return all_wbs

def get_data(filters):
	grand_total_qty = 0
	grand_total_amount = 0
	grand_total_rate = 0
	rows = []
	conditions = get_conditions(filters)
	conditions_mr = get_conditions_for_mr(filters)
	conditions_po = get_conditions_for_po(filters)
	wbs_doc = frappe.qb.DocType("Work Breakdown Structure")
	poi = frappe.qb.DocType('Purchase Order Item')
	po = frappe.qb.DocType('Purchase Order')
	mri = frappe.qb.DocType('Material Request Item')
	mr = frappe.qb.DocType('Material Request')
	
	query = (frappe.qb.from_(wbs_doc).select(wbs_doc.name, wbs_doc.wbs_name))
	if conditions:
		for cond in conditions:
			query = query.where(cond)
	all_wbs = query.run(as_dict=True)

	for i in all_wbs:
		query1 = (
			frappe.qb.from_(mri)
			.left_join(mr).on(mr.name == mri.parent)
			.select(
				mri.work_breakdown_structure.as_("wbs"),
				mri.item_code,
				mri.uom,
				mri.item_group,
				date_func(mr.creation).as_("voucher_date"),
				mr.transaction_date.as_("document_date"),
				mri.item_name.as_("item"),
				mri.idx,
				(mri.qty - mri.ordered_qty).as_("qty"),
				mri.rate,
				((mri.qty - mri.ordered_qty) * mri.rate).as_("amount"),
				mri.parenttype.as_("voucher_type"),
				mri.parent.as_("voucher_name")
			)
			.where(
				(mri.work_breakdown_structure == i.get("name")) &
				(mr.docstatus == 1)
			)
		)
		if conditions_mr:
			for cond1 in conditions_mr:
				query1 = query1.where(cond1)
		query1 = query1.orderby(mr.name, mri.idx)
		mr_data = query1.run(as_dict=1)

		query2 = (
			frappe.qb.from_(poi)
			.left_join(po).on(po.name == poi.parent)
			.select(
				poi.work_breakdown_structure.as_("wbs"),
				poi.uom,
				poi.item_group,
				(Case()
					.when(poi.custom_billed_qty > poi.received_qty, poi.qty - poi.custom_billed_qty)
					.else_(poi.qty - poi.received_qty)
				).as_("qty"),
				date_func(po.creation).as_("voucher_date"),
				po.supplier,
				po.supplier_name,
				po.transaction_date.as_("document_date"),
				poi.item_code,
				poi.item_name.as_("item"),
				poi.net_rate.as_("rate"),
				(Case()
					.when(poi.custom_billed_qty > poi.received_qty, poi.qty - poi.custom_billed_qty)
					.else_((poi.qty - poi.received_qty) * poi.net_rate)
				).as_("amount"),
				poi.idx,
				(poi.qty - poi.received_qty).as_('qty'),
				poi.parenttype.as_("voucher_type"),
				poi.parent.as_("voucher_name")
			)
			.where(
				(poi.work_breakdown_structure == i.get("name")) &
				(po.docstatus == 1)
			)
		)
		if conditions_po:
			for cond2 in conditions_po:
				query2 = query2.where(cond2)
		query2 = query2.orderby(po.name, poi.idx)
		po_data = query2.run(as_dict=1)
		
		all_data = mr_data + po_data
		total_qty = sum(x.get("qty") for x in all_data if x.get("wbs")==i.get("name") and x.get("qty")>0)
		total_amount = sum(x.get("amount") for x in all_data if x.get("wbs")==i.get("name") and x.get("qty")>0)
		total_rate = sum(x.get("rate") for x in all_data if x.get("wbs")==i.get("name") and x.get("qty")>0)
		grand_total_qty += total_qty
		grand_total_amount += total_amount
		grand_total_rate += total_rate
		if total_qty >0 :
			rows.append({"wbs":i.get("name"),"wbs_name":i.get("wbs_name"),"qty":total_qty,"amount":total_amount, "rate": total_rate})
		
		for j in all_data:
			if i.get("name") == j.get("wbs"):
				if j.get("qty")>0:
					rows.append({
						"wbs":i.get("name"),
						"wbs_name":i.get("wbs_name"),
						"voucher_type":j.get("voucher_type"),
						"voucher_name":j.get("voucher_name"),
						"voucher_date":j.get("voucher_date"),
						"document_date":j.get("document_date"),
						"supplier":j.get("supplier") if j.get("supplier") else None,
						"supplier_name":j.get("supplier_name") if j.get("supplier_name") else None,
						"idx":j.get("idx"),
						'item_code':j.get("item_code"),
						"item":j.get("item"),
						"item_group":j.get("item_group"),
						"qty":j.get("qty"),
						"uom":j.get("uom"),
						"currency":frappe.defaults.get_global_default("currency"),
						"rate":j.get("rate"),
						"amount":j.get("amount"),
						"indent":1
					})

	rows.append({"wbs":"Grand Total","qty":grand_total_qty,"amount":grand_total_amount, "rate": grand_total_rate})
	return rows