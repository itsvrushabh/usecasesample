import unittest
from unittest.mock import patch
from flask import json
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_customer_registration_valid_data(self):
        data = {
            "name": "John Doe",
            "dob": "1990-01-01",
            "email": "john@example.com",
            "adharNumber": "123456789012",
            "assignedMobileNumber": "9876543210",
            "plan": "Basic"
        }
        response = self.app.post('/api/customers', json=data)
        self.assertEqual(response.status_code, 201)

    def test_customer_registration_missing_fields(self):
        data = {
            "name": "John Doe",
            "dob": "1990-01-01",
            "email": "john@example.com"
            # Missing fields: 'adharNumber', 'assignedMobileNumber', 'plan'
        }
        response = self.app.post('/api/customers', json=data)
        self.assertEqual(response.status_code, 400)

    def test_customer_registration_invalid_plan(self):
        data = {
            "name": "John Doe",
            "dob": "1990-01-01",
            "email": "john@example.com",
            "adharNumber": "123456789012",
            "assignedMobileNumber": "9876543210",
            "plan": "InvalidPlan"
        }
        response = self.app.post('/api/customers', json=data)
        self.assertEqual(response.status_code, 400)

    @patch('app.customers', [])
    def test_update_plan_non_existing_customer(self):
        data = {"plan": "Basic"}
        response = self.app.put('/api/customers/1/update_plan', json=data)
        self.assertEqual(response.status_code, 404)

    # Add more test cases for other endpoints and scenarios...

if __name__ == '__main__':
    unittest.main()

