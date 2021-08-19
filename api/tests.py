from rest_framework import status
from rest_framework.test import APISimpleTestCase
import logging
from .serializers import CreditCheckSerializer
from django.urls import reverse
import json


logger = logging.getLogger(__name__)


class CreditTestCase(APISimpleTestCase):
    def setUp(self):
        logging.disable(logging.DEBUG)
        self.credit_check_url = '/api/v1/credit-check/'
        self.valid_credit_data = {
                'user_age': 19,
                'credit_value': 50000
                }
        
    def test_credit_check_valid_payload(self):
        logger.info("Tests are running, it may takes until 40 seconds to complete...")
        response = self.client.post(self.credit_check_url, data=self.valid_credit_data)
        content = json.loads(response.content)
        ticket_id = content["ticket_id"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert ticket_id

        response = self.client.get(reverse("results", args=[ticket_id]))
        content = json.loads(response.content)
        if content["ticket_status"] == "STARTED":
            assert content == {'ticket_id': ticket_id, 'ticket_status': 'STARTED',
                               'result': 'The credit is being checked right now, please try again in a few seconds.'}
        if content["ticket_status"] == "PENDING":
            assert content == {'ticket_id': ticket_id, 'ticket_status': 'PENDING',
                               'result': 'The credit check task is enqueued or ticket does not exist.'}
        while content["ticket_status"] not in ["SUCCESS", "FAILURE"]:
            response = self.client.get(reverse("results", args=[ticket_id]))
            content = json.loads(response.content)
            if content["ticket_status"] == "SUCCESS":
                assert content == {'ticket_id': ticket_id, 'ticket_status': 'SUCCESS',
                                   'result': 'Credit approved: All values match the requirements.'}
                assert response.status_code == 200
            if content["ticket_status"] == "FAILURE":
                assert content == {'ticket_id': ticket_id, 'ticket_status': 'FAILURE',
                                   'result': 'There was a failure in the credit check.'}
                assert response.status_code == 500

    def test_serializer(self):
        serializer = CreditCheckSerializer()
        data = serializer.validate(self.valid_credit_data)

        self.assertEqual(data, self.valid_credit_data)

