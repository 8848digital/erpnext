import frappe
def execute():
	if frappe.conf.db_type == "postgres":
		frappe.db.sql(
			"""
			UPDATE 
				`tabWork Order Item` woi
			SET 
				stock_uom = i.stock_uom
			FROM 
				`tabItem` i
			WHERE 
				woi.item_code = i.name
				AND woi.docstatus = 1
		"""
		)
	else:
		frappe.db.sql(
			"""
			UPDATE
				`tabWork Order Item`, `tabItem`
			SET
				`tabWork Order Item`.stock_uom = `tabItem`.stock_uom
			WHERE
				`tabWork Order Item`.item_code = `tabItem`.name
				AND `tabWork Order Item`.docstatus = 1
		"""
		)