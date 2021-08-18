import json
from rest_framework import status
from rest_framework.test import APISimpleTestCase


class CreditTestCase(APISimpleTestCase):
    def setUp(self):
        self.credit_check_url = '/api/v1/credit/'

    def test_credit_check_valid_payload(self):
        valid_credit_data = {
            'user_age': 19,
            'credit_value': 50000
        }
        response = self.client.post(self.credit_check_url, data=valid_credit_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

