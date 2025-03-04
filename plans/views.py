import pandas as pd
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Plan
from dictionary.models import Dictionary
from .serializers import PlanUploadSerializer


CATEGORY_MAP = {
    category.name.lower(): category.id for category in Dictionary.objects.all()
}


def refresh_category_map():
    """Updates CATEGORY_MAP (used in tests when database is recreated)."""
    global CATEGORY_MAP
    CATEGORY_MAP = {
        category.name.lower(): category.id for category in Dictionary.objects.all()
    }


class PlansInsertView(APIView):
    def post(self, request):
        serializer = PlanUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file = serializer.validated_data["file"]
        df, error_response = validate_excel_file(file)
        if error_response:
            return (
                error_response  # Return an error response if the Excel file is invalid
            )

        errors = []
        valid_rows = []

        # Validate all rows before inserting into the database
        for _, row in df.iterrows():
            error = validate_plan_row(row)
            if error:
                errors.append(error)  # Collect errors
            else:
                valid_rows.append(row)  # Collect valid rows

        if errors:
            return Response(
                {"errors": errors}, status=status.HTTP_400_BAD_REQUEST
            )  # Abort if any errors exist

        # Insert data into the database only if all rows are valid
        with transaction.atomic():
            for row in valid_rows:
                insert_plan_row(row)

        return Response(
            {"message": "Data successfully uploaded"}, status=status.HTTP_201_CREATED
        )


def validate_excel_file(file):
    """Validate the structure and format of the uploaded Excel file."""
    try:
        df = pd.read_excel(file)
    except Exception:
        return None, Response(
            {"error": "Invalid file format"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Check if file is completely empty
    if df.empty:
        return None, Response(
            {"error": "The uploaded file is empty"}, status=status.HTTP_400_BAD_REQUEST
        )

    required_columns = ["period", "category_name", "sum"]
    if not all(col in df.columns for col in required_columns):
        return None, Response(
            {
                "error": "Invalid data format in the file. Required columns: period, category_name, sum"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    return df, None


def validate_plan_row(row):
    """Validates a single row against the required rules. Returns an error message or None if valid."""
    period = pd.to_datetime(row["period"], errors="coerce")
    if pd.isna(period) or period.day != 1:
        return f"Plan month must be the first day of the month: {row['period']}"

    category_id = CATEGORY_MAP.get(str(row["category_name"]).strip().lower(), None)
    if not category_id:
        return f"Category {row['category_name']} does not exist"

    if Plan.objects.filter(period=period.date(), category_id=category_id).exists():
        return f"Plan for {row['category_name']} in {period.date()} already exists"

    sum_value = row["sum"]
    if pd.isna(sum_value):
        return "Column 'sum' cannot contain empty values"

    # Convert sum_value to a number (handle strings and NaN)
    try:
        sum_value = float(sum_value)
    except ValueError:
        return "Column 'sum' must be a numeric value"

    if sum_value < 0:
        return "Column 'sum' cannot contain negative values"

    return None  # No errors found


def insert_plan_row(row):
    """Inserts a validated row into the database."""
    period = pd.to_datetime(row["period"]).date()
    category_id = CATEGORY_MAP[row["category_name"].lower()]
    sum_value = row["sum"]

    Plan.objects.create(period=period, category_id=category_id, sum=sum_value)
