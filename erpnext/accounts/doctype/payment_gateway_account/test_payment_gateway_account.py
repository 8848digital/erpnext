# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

import unittest

# test_records = frappe.get_test_records('Payment Gateway Account')

# "Payment Gateway" doctype ships with the separate `payments` app, which is not
# installed in this bench; skip it so test record generation doesn't fail here.
test_ignore = ["Payment Gateway"]


class TestPaymentGatewayAccount(unittest.TestCase):
	pass
