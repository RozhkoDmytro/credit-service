from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from io import BytesIO
import pandas as pd
from datetime import date
from plans.models import Plan
from dictionary.models import Dictionary
from parameterized import parameterized
from plans.views import refresh_category_map  # Import the refresh function


class PlansInsertAPITest(TestCase):
    def setUp(self):
        """Set up test data before each test"""
        self.url = reverse("plans_insert")
        Dictionary.objects.create(id=1, name="Видача")  # Ukrainian category name
        refresh_category_map()  # Update CATEGORY_MAP to ensure correct test execution

    def create_test_excel(self, data):
        """Helper method to create an in-memory Excel file"""
        excel_file = BytesIO()
        df = pd.DataFrame(data)
        df.to_excel(excel_file, index=False)
        excel_file.seek(0)
        return excel_file

    @parameterized.expand(
        [
            # ✅ 1. Valid plan upload
            (
                "valid_plan",
                [{"period": "2024-03-01", "category_name": "Видача", "sum": 1000}],
                status.HTTP_201_CREATED,
                1,
                None,
            ),
            # ✅ 2. Invalid file format
            (
                "invalid_file_format",
                None,  # No data, simulating a non-Excel file
                status.HTTP_400_BAD_REQUEST,
                0,
                "Invalid file format",
            ),
            # ✅ 3. Missing required columns
            (
                "missing_columns",
                [{"period": "2024-03-01", "sum": 1000}],  # Missing `category_name`
                status.HTTP_400_BAD_REQUEST,
                0,
                "Invalid data format",
            ),
            # ✅ 4. Invalid period format (not first day of month)
            (
                "invalid_period_format",
                [{"period": "2024-03-15", "category_name": "Видача", "sum": 1000}],
                status.HTTP_400_BAD_REQUEST,
                0,
                "Plan month must be the first day",
            ),
            # ✅ 5. Nonexistent category
            (
                "nonexistent_category",
                [
                    {
                        "period": "2024-03-01",
                        "category_name": "Unknown Category",
                        "sum": 1000,
                    }
                ],
                status.HTTP_400_BAD_REQUEST,
                0,
                "Category Unknown Category does not exist",
            ),
            # ✅ 6. Negative sum
            (
                "negative_sum",
                [{"period": "2024-03-01", "category_name": "Видача", "sum": -100}],
                status.HTTP_400_BAD_REQUEST,
                0,
                "Column 'sum' cannot contain negative values",
            ),
            # ✅ 7. Empty sum
            (
                "empty_sum",
                [{"period": "2024-03-01", "category_name": "Видача", "sum": None}],
                status.HTTP_400_BAD_REQUEST,
                0,
                "Column 'sum' cannot contain empty values",
            ),
            # ✅ 8. Duplicate plan
            (
                "duplicate_plan",
                [{"period": "2024-03-01", "category_name": "Видача", "sum": 1000}],
                status.HTTP_400_BAD_REQUEST,
                1,
                "Plan for Видача in 2024-03-01 already exists",
            ),
            # ✅ 9. Future period is allowed
            (
                "future_period",
                [{"period": "2025-06-01", "category_name": "Видача", "sum": 1500}],
                status.HTTP_201_CREATED,
                1,
                None,
            ),
            # ✅ 10. Invalid sum format (string instead of number)
            (
                "invalid_sum_format",
                [
                    {
                        "period": "2024-03-01",
                        "category_name": "Видача",
                        "sum": "one thousand",
                    }
                ],
                status.HTTP_400_BAD_REQUEST,
                0,
                "Column 'sum' must be a numeric value",
            ),
            # ✅ 11. Empty file
            (
                "empty_file",
                [],
                status.HTTP_400_BAD_REQUEST,
                0,
                "The uploaded file is empty",
            ),
            # ✅ 12. Incorrect column names
            (
                "incorrect_columns",
                [
                    {"date": "2024-03-01", "category": "Видача", "amount": 1000}
                ],  # Wrong column names
                status.HTTP_400_BAD_REQUEST,
                0,
                "Invalid data format",
            ),
        ]
    )
    def test_plan_upload(
        self, name, data, expected_status, expected_count, expected_error
    ):
        """Parameterized test for various plan upload scenarios"""
        refresh_category_map()  # Ensure CATEGORY_MAP is updated before each test

        if name == "duplicate_plan":
            category_id = Dictionary.objects.get(name="Видача").id
            Plan.objects.create(
                period=date(2024, 3, 1), category_id=category_id, sum=1000
            )

        if name == "invalid_file_format":
            response = self.client.post(
                self.url, {"file": BytesIO(b"invalid data")}, format="multipart"
            )
        elif name == "empty_file":
            response = self.client.post(
                self.url, {"file": self.create_test_excel([])}, format="multipart"
            )
        else:
            excel_file = self.create_test_excel(data)
            response = self.client.post(
                self.url, {"file": excel_file}, format="multipart"
            )

        print(f"DEBUG Response for {name}:", response.json())  # Debugging output

        self.assertEqual(response.status_code, expected_status)

        if expected_error:
            self.assertIn(expected_error, str(response.json()))
