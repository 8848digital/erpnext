// Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.provide("erpnext.accounts.bank_reconciliation");

frappe.ui.form.on("Bank Reconciliation Tool ERPNext", {
	refresh(frm) {
		frm.disable_save();
		// frappe.require("bank-reconciliation-tool.bundle.js", () => frm.trigger("make_reconciliation_tool"));
		if (frm.doc.closing_balance_as_per_bank_statement && frm.doc.closing_balance_as_per_erp) {
			frm.set_value(
				"difference_amount",
				(frm.doc.closing_balance_as_per_bank_statement - frm.doc.closing_balance_as_per_erp)
			);
		}

		frm.add_custom_button(__("Upload Bank Statement"), () =>
			frappe.call({
				method: "erpnext.accounts.doctype.bank_statement_import.bank_statement_import.upload_bank_statement",
				args: {
					dt: frm.doc.doctype,
					dn: frm.doc.name,
					company: frm.doc.company,
					bank_account: frm.doc.bank_account,
				},
				callback: function (r) {
					if (!r.exc) {
						var doc = frappe.model.sync(r.message);
						frappe.set_route("Form", doc[0].doctype, doc[0].name);
					}
				},
			})
		);
		if (frm.doc.closing_balance_as_per_erp && frm.doc.closing_balance_as_per_bank_statement) {
			frm.set_value(
				"difference_amount",
				frm.doc.closing_balance_as_per_bank_statement - frm.doc.closing_balance_as_per_erp
			);
		}
		// console.log(" NOT ALLLOCSATE",frm.doc.bank_statement.length)
		if (frm.doc.bank_statement.length && frm.doc.erp_transaction.length) {
			// console.log("ALLLOCSATE")
			frm.add_custom_button(__("Allocate"), () => frm.trigger("allocate"));
			frm.change_custom_button_type(__("Allocate"), null, "primary");
			frm.change_custom_button_type(__("Get Unreconciled Entries"), null, "default");
		}
		if (frm.doc.matching_table.length) {
			frm.add_custom_button(__("Reconcile"), () => frm.trigger("reconcile"));
			frm.change_custom_button_type(__("Reconcile"), null, "primary");
			frm.change_custom_button_type(__("Get Unreconciled Entries"), null, "default");
			frm.change_custom_button_type(__("Allocate"), null, "default");
			// frm.refresh_field("erp_transaction");
		}

	},
	setup: function (frm) {
		frm.set_query("bank_account", function () {
			return {
				filters: {
					company: frm.doc.company,
					is_company_account: 1,
				},
			};
		});
		// let no_bank_transactions_text = `<div class="text-muted text-center">${__(
		// 	"No Matching Bank Transactions Found"
		// )}</div>`;
		// set_field_options("no_bank_transactions", no_bank_transactions_text);
	},
	bank_account: function (frm) {
		frappe.db.get_value("Bank Account", frm.doc.bank_account, "account", (r) => {
			frappe.db.get_value("Account", r.account, "account_currency", (r) => {
				frm.doc.account_currency = r.account_currency;
				// console.log('rrrr',r, frm.doc.account_currency)
				// frm.trigger("render_chart");
			});
		});
		// frm.trigger("render_chart");
		frm.trigger("get_account_opening_balance");
		frm.doc.difference_amount = (frm.doc.closing_balance_as_per_bank_statement - frm.doc.closing_balance_as_per_erp)
		frm.refresh_fields();
		frm.add_custom_button(__("Get Unreconciled Entries"), function () {
			frm.set_value(
				"difference_amount",
				(frm.doc.closing_balance_as_per_bank_statement - frm.doc.closing_balance_as_per_erp)
			);
			frm.doc.bank_statement = []
			frm.doc.erp_transaction = []
			frm.trigger("unreconcile_entries");
			// frappe.call({
			// 	method: "erpnext.accounts.doctype.bank_reconciliation_tool_erpnext.bank_reconciliation_tool_erpnext.get_bank_transaction",
			// 	args: {
			// 		bank_account: frm.doc.bank_account,
			// 		company: frm.doc.company,
			// 		from_statement_date: frm.doc.from_statement_date,
			// 		to_statement_date: frm.doc.to_statement_date,
			// 	},
			// 	callback: (response) => {
			// 		let existingTransactionIds = new Set(
			// 			frm.doc.bank_statement.map((row) => row.bank_transaction_id) // Collect existing IDs
			// 		);
			// 		console.log('Response:', response.message);

			// 		if (Array.isArray(response.message)) {
			// 			response.message.forEach((transaction) => {
			// 				if (!existingTransactionIds.has(transaction.name)) {
			// 					if (transaction.deposit || transaction.withdrawal) {
			// 						// Add a new child row to the bank_statement table
			// 						let bankTransaction = frm.add_child("bank_statement");
			// 						bankTransaction.date = transaction.date;
			// 						bankTransaction.bank_transaction_id = transaction.name;
			// 						bankTransaction.description = transaction.description;
			// 						bankTransaction.deposit = transaction.deposit;
			// 						bankTransaction.withdraw = transaction.withdrawal;
			// 						bankTransaction.reference_no = transaction.reference_number;
			// 						bankTransaction.unallocated_amount = transaction.unallocated_amount;

			// 						// Track added transaction IDs
			// 						existingTransactionIds.add(transaction.name);
			// 					}
			// 				}
			// 			});
			// 		} else {
			// 			console.error("Invalid response.message:", response.message);
			// 		}

			// 		frm.refresh_field("bank_statement");
			// 	},
			// });
			// frappe.call({
			// 	method: "erpnext.accounts.doctype.bank_reconciliation_tool_erpnext.bank_reconciliation_tool_erpnext.get_erp_transaction",
			// 	args: {
			// 		bank_account: frm.doc.bank_account,
			// 		company: frm.doc.company,
			// 		from_statement_date: frm.doc.from_erp_date,
			// 		to_statement_date: frm.doc.to_erp_date,
			// 	},
			// 	callback: async (response) => {
			// 		// Create a Set of existing reference IDs in the `erp_transaction` table
			// 		let existingReferenceIds = new Set(
			// 			frm.doc.erp_transaction.map((row) => row.reference_id)
			// 		);
				
			// 		for (const i of response.message) {
			// 			if (i.paid_amount > 0 && !existingReferenceIds.has(i.name)) {
			// 				// Add the transaction if it does not already exist
			// 				let bnk_tr = frm.add_child("erp_transaction");
			// 				bnk_tr.date = i.posting_date;
			// 				bnk_tr.reference_id = i.name; // Unique reference ID
			// 				bnk_tr.reference_number = i.reference_no;
			// 				bnk_tr.reference_doc = i.doctype;
				
			// 				if (i.doctype === "Payment Entry") {
			// 					const payment_type = await frappe.db.get_value(
			// 						"Payment Entry",
			// 						i.name,
			// 						"payment_type"
			// 					);
				
			// 					if (payment_type.message.payment_type === "Pay") {
			// 						bnk_tr.withdraw = i.amount;
			// 						bnk_tr.remaining_amount = i.paid_amount;
			// 						bnk_tr.deposit = 0;
			// 					} else if (payment_type.message.payment_type === "Receive") {
			// 						bnk_tr.deposit = i.amount;
			// 						bnk_tr.remaining_amount = i.paid_amount;
			// 						bnk_tr.withdraw = 0;
			// 					} else {
			// 						bnk_tr.withdraw = i.amount;
			// 						bnk_tr.remaining_amount = i.paid_amount;
			// 						bnk_tr.deposit = 0;
			// 					}
			// 				} else if (i.doctype === "Journal Entry") {
			// 					if (i.bank == 'Credit'){
			// 						bnk_tr.deposit = 0;
			// 						bnk_tr.withdraw = i.amount; // Confirm logic here.
			// 						bnk_tr.remaining_amount = i.paid_amount;
			// 					}
			// 					else if (i.bank == 'Debit'){
			// 						bnk_tr.deposit = i.amount;
			// 						bnk_tr.remaining_amount = i.paid_amount;
			// 						bnk_tr.withdraw = 0; // Confirm logic here.
			// 					}
			// 				}
				
			// 				// Add the reference ID to the Set to track it
			// 				existingReferenceIds.add(i.name);
			// 			}
			// 		}
				
			// 		// Refresh field after processing all transactions
			// 		frm.refresh_field("erp_transaction");			
			// 		// Add custom button for Allocate
			// 		frm.add_custom_button(__("Allocate"), () => frm.trigger("allocate"));
			// 		frm.change_custom_button_type(__("Allocate"), null, "primary");
			// 		frm.change_custom_button_type(__("Get Unreconciled Entries"), null, "default");
			// 	},
			// });
		});
	},
	get_account_opening_balance(frm) {
		if (frm.doc.bank_account && frm.doc.from_date && frm.doc.to_date) {
			frappe.call({
				method: "erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.get_account_balance",
				args: {
					bank_account: frm.doc.bank_account,
					till_date: frappe.datetime.add_days(frm.doc.from_date, -1),
					company: frm.doc.company
				},
				callback: (response) => {
					frm.set_value("opening_balance", response.message);
				},
			});
		}
	},

	onload: function (frm) {
		// Set default filter dates
		let today = frappe.datetime.get_today();
		frm.doc.from_date = frappe.datetime.add_months(today, -1);
		frm.doc.to_date = today;
		frm.doc.from_statement_date = frappe.datetime.add_months(today, -1);
		frm.doc.to_statement_date = today;
		frm.doc.from_erp_date = frappe.datetime.add_months(today, -1);
		frm.doc.to_erp_date = today;
		frm.trigger("bank_account");
	},

	opening_balance(frm) {
		// frm.set_value("closing_balance_as_per_erp", frm.doc.opening_balance);
		// console.log("CLOSING BAL")
		frappe.call({
			method: "erpnext.accounts.doctype.bank_reconciliation_tool_erpnext.bank_reconciliation_tool_erpnext.get_closing_bal_bnk",
			args: {
				bank_account: frm.doc.bank_account,
			},
			callback: function (r) {
				// console.log('GHJJHJHJHJBBJ', r)
				if (!r.exc) {
					if (r.message) {
						frm.doc.closing_balance_as_per_bank_statement = r.message;
					}
				}
				frm.refresh_field("closing_balance_as_per_bank_statement");
			},
		});

		frappe.call({
			method: "erpnext.accounts.doctype.bank_reconciliation_tool_erpnext.bank_reconciliation_tool_erpnext.get_closing_bal_erp",
			args: {
				opening_balance: frm.doc.opening_balance,
				bank_account: frm.doc.bank_account,
				from_date: frm.doc.from_date,
				to_date: frm.doc.to_date
			},
			callback: function (r) {
				// console.log('GHJJHJHJHJBBJ', r)
				if (!r.exc) {
					if (r.message) {
						frm.doc.closing_balance_as_per_erp = r.message;
					}
				}
				frm.refresh_field("closing_balance_as_per_erp");
			},
		});
	},

	closing_balance_as_per_erp(frm) {
		if (frm.doc.closing_balance_as_per_bank_statement) {
			frm.set_value(
				"difference_amount",
				(frm.doc.closing_balance_as_per_bank_statement - frm.doc.closing_balance_as_per_erp)
			);
		}
	},
	closing_balance_as_per_bank_statement(frm) {
		if (frm.doc.closing_balance_as_per_bank_statement) {
			frm.set_value(
				"difference_amount",
				(frm.doc.closing_balance_as_per_bank_statement - frm.doc.closing_balance_as_per_erp)
			);
		}
	},
	from_date: function (frm) {
		frm.trigger("get_account_opening_balance");
		frm.doc.from_statement_date = frm.doc.from_date;
		// frm.doc.to_statement_date = today;
		frm.doc.from_erp_date = frm.doc.from_date;
		// frm.doc.to_erp_date = today;
		frm.refresh_field("from_statement_date")
		frm.refresh_field("from_erp_date")

	},
	to_date: function (frm) {
		frm.trigger("get_account_opening_balance");
		frm.doc.to_statement_date = frm.doc.to_date;
		frm.doc.to_erp_date = frm.doc.to_date;;
		frm.refresh_field("to_statement_date")
		frm.refresh_field("to_erp_date")
	},
	// make_reconciliation_tool(frm) {
	// 	frm.get_field("reconciliation_tool_cards").$wrapper.empty();
	// 	if (frm.doc.bank_account && frm.doc.bank_statement_to_date) {
	// 		frm.trigger("get_cleared_balance").then(() => {
	// 			if (
	// 				frm.doc.bank_account &&
	// 				frm.doc.from_date &&
	// 				frm.doc.to_date
	// 			) {
	// 				frm.trigger("render_chart");
	// 				frm.trigger("render");
	// 				frappe.utils.scroll_to(frm.get_field("reconciliation_tool_cards").$wrapper, true, 30);
	// 			}
	// 		});
	// 	}
	// },
	// render_chart(frm) {
	// 	frm.cards_manager = new erpnext.accounts.bank_reconciliation.NumberCardManager({
	// 		$reconciliation_tool_cards: frm.get_field("reconciliation_tool_cards").$wrapper,
	// 		bank_statement_closing_balance: frm.doc.closing_balance_as_per_bank_statement,
	// 		cleared_balance: frm.doc.difference_amount,
	// 		currency: frm.doc.account_currency,
	// 	});
	// },
	allocate(frm) {
		let bank_statement = frm.fields_dict.bank_statement.grid.get_selected_children();
		if (!bank_statement.length) {
			bank_statement = frm.doc.bank_statement;
		}
		let erp_transaction = frm.fields_dict.erp_transaction.grid.get_selected_children();
		if (!erp_transaction.length) {
			erp_transaction = frm.doc.erp_transaction;
		}
		bank_statement.map((i)=>{
			erp_transaction.map((j)=>{
				if ((i.deposit > 0 && j.deposit > 0) || (j.withdraw >0 && i.withdraw >0)) {
					return frm.call({
						doc: frm.doc,
						method: "allocate_entries",
						args: {
							bank_statement: bank_statement,
							erp_transaction: erp_transaction,
						},
						callback: () => {
							frm.refresh();
						},
					});
				}
				else {
					frappe.msgprint("Cannot allocate Deposit entries with Withdraw Entries")
				}
			})
		})
	},

	reconcile(frm) {
		// frm.trigger("update_bal");
		// frm.doc.matching_table.map((i) => {
		frm.call({
			method: "erpnext.accounts.doctype.bank_reconciliation_tool_erpnext.bank_reconciliation_tool_erpnext.reconcile_bnk_transaction",
			args: {
				matching_table: frm.doc.matching_table,
				// amount: i.matched_amount,
				// name: i.reference_id,
				// payment_document: i.reference_to,
			},
			callback: function (r) {
				frm.clear_table("bank_statement");
				frm.clear_table("erp_transaction");
				frm.clear_table("matching_table");
				frm.trigger("unreconcile_entries");
				// frm.refresh();
				// console.log('GHJJHJHJHJBBJ')
				if (!r.exc) {
					if (r.message) {
						frappe.msgprint("done");
					}
				}
			},
		});
		// });
	},

	// render_chart(frm) {
	// 	frm.cards_manager = new erpnext.accounts.bank_reconciliation.NumberCardManager({
	// 		$reconciliation_tool_cards: frm.get_field("reconciliation_tool_cards").$wrapper,
	// 		bank_statement_closing_balance: frm.doc.closing_balance_as_per_bank_statement,
	// 		cleared_balance: frm.cleared_balance,
	// 		currency: frm.doc.account_currency,
	// 	});
	// },

	// render(frm) {
	// 	if (frm.doc.bank_account) {
	// 		frm.bank_reconciliation_data_table_manager =
	// 			new erpnext.accounts.bank_reconciliation.DataTableManager({
	// 				company: frm.doc.company,
	// 				bank_account: frm.doc.bank_account,
	// 				$reconciliation_tool_dt: frm.get_field("reconciliation_tool_dt").$wrapper,
	// 				$no_bank_transactions: frm.get_field("no_bank_transactions").$wrapper,
	// 				bank_statement_from_date: frm.doc.from_date,
	// 				bank_statement_to_date: frm.doc.to_date,
	// 				filter_by_reference_date: frm.doc.from_statement_date,
	// 				from_reference_date: frm.doc.from_statement_date,
	// 				to_reference_date: frm.doc.to_statement_date,
	// 				bank_statement_closing_balance: frm.doc.closing_balance_as_per_bank_statement,
	// 				cards_manager: frm.cards_manager,
	// 			});
	// 	}
	// },

	// get_cleared_balance(frm) {
	// 	if (frm.doc.bank_account && frm.doc.bank_statement_to_date) {
	// 		return frappe.call({
	// 			method: "erpnext.accounts.doctype.bank_reconciliation_tool.bank_reconciliation_tool.get_account_balance",
	// 			args: {
	// 				bank_account: frm.doc.bank_account,
	// 				till_date: frm.doc.bank_statement_to_date,
	// 			},
	// 			callback: (response) => {
	// 				frm.cleared_balance = response.message;
	// 			},
	// 		});
	// 	}
	// },
	unreconcile_entries(frm) {
		frappe.call({
			method: "erpnext.accounts.doctype.bank_reconciliation_tool_erpnext.bank_reconciliation_tool_erpnext.get_bank_transaction",
			args: {
				bank_account: frm.doc.bank_account,
				company: frm.doc.company,
				from_statement_date: frm.doc.from_statement_date,
				to_statement_date: frm.doc.to_statement_date,
			},
			callback: (response) => {
				let existingTransactionIds = new Set(
					frm.doc.bank_statement.map((row) => row.bank_transaction_id) // Collect existing IDs
				);
				if (Array.isArray(response.message)) {
					response.message.forEach((transaction) => {
						if (!existingTransactionIds.has(transaction.name)) {
							if (transaction.deposit || transaction.withdrawal) {
								// Add a new child row to the bank_statement table
								let bankTransaction = frm.add_child("bank_statement");
								bankTransaction.date = transaction.date;
								bankTransaction.bank_transaction_id = transaction.name;
								bankTransaction.description = transaction.description;
								bankTransaction.deposit = transaction.deposit;
								bankTransaction.withdraw = transaction.withdrawal;
								bankTransaction.reference_no = transaction.reference_number;
								bankTransaction.unallocated_amount = transaction.unallocated_amount;

								// Track added transaction IDs
								existingTransactionIds.add(transaction.name);
							}
						}
					});
				} else {
					console.error("Invalid response.message:", response.message);
				}

				frm.refresh_field("bank_statement");
			},
		});
		frappe.call({
			method: "erpnext.accounts.doctype.bank_reconciliation_tool_erpnext.bank_reconciliation_tool_erpnext.get_erp_transaction",
			args: {
				bank_account: frm.doc.bank_account,
				company: frm.doc.company,
				from_statement_date: frm.doc.from_erp_date,
				to_statement_date: frm.doc.to_erp_date,
			},
			callback: async (response) => {
				// Create a Set of existing reference IDs in the `erp_transaction` table
				let existingReferenceIds = new Set(
					frm.doc.erp_transaction.map((row) => row.reference_id)
				);
			
				for (const i of response.message) {
					if (i.paid_amount > 0 && !existingReferenceIds.has(i.name)) {
						// Add the transaction if it does not already exist
						let bnk_tr = frm.add_child("erp_transaction");
						bnk_tr.date = i.posting_date;
						bnk_tr.reference_id = i.name; // Unique reference ID
						bnk_tr.reference_number = i.reference_no;
						bnk_tr.reference_doc = i.doctype;
			
						if (i.doctype === "Payment Entry") {
							const payment_type = await frappe.db.get_value(
								"Payment Entry",
								i.name,
								"payment_type"
							);
			
							if (payment_type.message.payment_type === "Pay") {
								bnk_tr.withdraw = i.amount;
								bnk_tr.remaining_amount = i.paid_amount;
								bnk_tr.deposit = 0;
							} else if (payment_type.message.payment_type === "Receive") {
								bnk_tr.deposit = i.amount;
								bnk_tr.remaining_amount = i.paid_amount;
								bnk_tr.withdraw = 0;
							} else {
								bnk_tr.withdraw = i.amount;
								bnk_tr.remaining_amount = i.paid_amount;
								bnk_tr.deposit = 0;
							}
						} else if (i.doctype === "Journal Entry") {
							if (i.bank == 'Credit'){
								bnk_tr.deposit = 0;
								bnk_tr.withdraw = i.amount; // Confirm logic here.
								bnk_tr.remaining_amount = i.paid_amount;
							}
							else if (i.bank == 'Debit'){
								bnk_tr.deposit = i.amount;
								bnk_tr.remaining_amount = i.paid_amount;
								bnk_tr.withdraw = 0; // Confirm logic here.
							}
						}
			
						// Add the reference ID to the Set to track it
						existingReferenceIds.add(i.name);
					}
				}
			
				// Refresh field after processing all transactions
				frm.refresh_field("erp_transaction");			
				// Add custom button for Allocate
				frm.add_custom_button(__("Allocate"), () => frm.trigger("allocate"));
				frm.change_custom_button_type(__("Allocate"), null, "primary");
				frm.change_custom_button_type(__("Get Unreconciled Entries"), null, "default");
			},
		});
		setTimeout(() => {
			if (!(frm.doc.bank_statement.length) && !(frm.doc.erp_transaction.length)) {
				frappe.throw("No records found")
			}
		}, 700);
	},

	update_bal(frm) {
		console.log("Update BAl")
		frm.doc.matching_table.map((i) => {
			frm.doc.erp_transaction.map((j) => {
				if (i.reference_id == j.reference_id) {
					frm.doc.bank_statement.map((k) => {
						if (k.bank_transaction_id == i.bank_transaction_id) {
							if ((j.withdraw || j.deposit) - (k.withdraw || k.deposit) >= 0) {
								j.remaining_amount =
									(j.withdraw || j.deposit) - (k.withdraw || k.deposit);
							} else {
								j.remaining_amount = 0;
							}
						}
					});
				}
			});
		});
	}
});
