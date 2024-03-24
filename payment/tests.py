import json

from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from unittest.mock import patch
from orders.models import Order
from .webhooks import stripe_webhook

class WebhookTestCase(TestCase):
    def setUp(self):
        # Создание заказа
        self.order = Order.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            address='123 Main St',
            postal_code='12345',
            city='New York',
        )

    @patch('payment.webhooks.stripe')
    def test_stripe_webhook(self, stripe_mock):
        # Создание тестового запроса
        request = HttpRequest()
        request.method = 'POST'
        request.META['HTTP_STRIPE_SIGNATURE'] = 'fake_signature'

        # Моделирование данных в теле запроса
        payload = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "mode": "payment",
                    "payment_status": "paid",
                    "client_reference_id": self.order.id
                }
            }
        }
        request.body = json.dumps(payload).encode('utf-8')

        # Вызов функции вебхука
        response = stripe_webhook(request)

        # Проверка ответа
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)

        # Проверка, что заказ помечен как оплаченный
        self.order.refresh_from_db()
        self.assertTrue(self.order.paid)

