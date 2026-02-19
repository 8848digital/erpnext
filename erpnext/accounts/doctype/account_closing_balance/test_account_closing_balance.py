# Import necessary modules
import frappe
from frappe.tests.utils import FrappeTestCase
from erpnext.accounts.utils import get_fiscal_year
from frappe.utils import today, add_months
class TestAccountClosingBalance(FrappeTestCase):
    def setUp(self):
        fiscal_year, fiscal_year_start_date, fiscal_year_end_date = get_fiscal_year(date=today(), company="_Test Company")
        self.period_closing_voucher = frappe.get_doc({
            "doctype": "Period Closing Voucher",
            "transaction_date": today(),
            "company": "_Test Company",
            "fiscal_year": fiscal_year,
            "period_start_date": fiscal_year_start_date,
            "period_end_date": fiscal_year_end_date,
            "closing_account_head": "Opening Balance Equity - _TC",
            "remarks": "Test Period Closing Voucher",
        }).insert(ignore_permissions=True)
        # This runs before each test to set up data
        self.account_closing_balance = frappe.get_doc({
            "doctype": "Account Closing Balance",
            "closing_date": add_months(today(), 1),
            "account": "Opening Balance Equity - _TC",
            "cost_center": "_Test Company - _TC",
            "debit": 1000.0,
            "credit": 500.0,
            "account_currency": "USD",
            "debit_in_account_currency": 1000.0,
            "credit_in_account_currency": 500.0,
            "project": "_T-Project-00001",
            "company": "_Test Company",
            "period_closing_voucher": self.period_closing_voucher.name,
            "is_period_closing_voucher_entry": 1
        })

    def test_create_account_closing_balance(self):
        # Test if the document is created successfully
        self.account_closing_balance.insert()
        self.assertTrue(self.account_closing_balance.name)

    def test_debit_credit_amounts(self):
        # Ensure debit and credit amounts are set correctly
        self.assertEqual(self.account_closing_balance.debit, 1000.0)
        self.assertEqual(self.account_closing_balance.credit, 500.0)

    def test_account_currency(self):
        # Check if account currency is set correctly
        self.assertEqual(self.account_closing_balance.account_currency, "USD")

    def test_company_field(self):
        # Check if company field is populated correctly
        self.assertEqual(self.account_closing_balance.company, "_Test Company")


    def tearDown(self):
        # This runs after each test to clean up data
        if self.account_closing_balance:
            self.account_closing_balance.delete()

