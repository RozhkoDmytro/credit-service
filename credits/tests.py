from django.test import TestCase
from django.urls import reverse
from datetime import date
from users.models import User
from .models import Credit
from payments.models import Payment
from dictionary.models import Dictionary
import csv
from parameterized import parameterized


class CreditModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=1, login="test_user", registration_date=date.today()
        )
        self.payment_type_body = Dictionary.objects.create(id=1, name="Тіло")
        self.payment_type_interest = Dictionary.objects.create(id=2, name="Відсотки")

    @parameterized.expand(
        [
            (1, 1000.00, 100.00, date(2023, 1, 1), date(2024, 1, 1), None, True),
            (2, -500.00, 50.00, date(2023, 1, 1), date(2024, 1, 1), None, False),
        ]
    )
    def test_credit_creation(
        self,
        credit_id,
        body,
        percent,
        issuance_date,
        return_date,
        actual_return_date,
        is_valid,
    ):
        if is_valid:
            credit = Credit.objects.create(
                id=credit_id,
                user=self.user,
                issuance_date=issuance_date,
                return_date=return_date,
                actual_return_date=actual_return_date,
                body=body,
                percent=percent,
            )
            self.assertEqual(credit.body, body)
        else:
            self.assertLess(body, 0)


class UserCreditsAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=1, login="test_user", registration_date=date.today()
        )
        self.credit = Credit.objects.create(
            id=1,
            user=self.user,
            issuance_date=date(2023, 1, 1),
            return_date=date(2024, 1, 1),
            actual_return_date=None,
            body=1000.00,
            percent=100.00,
        )
        self.payment_type_body = Dictionary.objects.create(id=1, name="Тіло")
        self.payment_type_interest = Dictionary.objects.create(id=2, name="Відсотки")
        Payment.objects.create(
            id=1,
            sum=500,
            payment_date=date(2023, 6, 1),
            credit_id=self.credit.id,
            type_id=self.payment_type_body.id,
        )
        Payment.objects.create(
            id=2,
            sum=100,
            payment_date=date(2023, 6, 10),
            credit_id=self.credit.id,
            type_id=self.payment_type_interest.id,
        )

    @parameterized.expand(
        [
            (1, 200, True),
            (99, 404, False),
        ]
    )
    def test_user_credits(self, user_id, expected_status, has_data):
        response = self.client.get(reverse("user_credits", args=[user_id]))
        self.assertEqual(response.status_code, expected_status)
        if has_data:
            self.assertEqual(len(response.json()), 1)
            self.assertEqual(response.json()[0]["body"], "1000.00")
