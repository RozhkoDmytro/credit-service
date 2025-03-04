import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime

from users.models import User
from credits.models import Credit
from dictionary.models import Dictionary
from plans.models import Plan
from payments.models import Payment


class Command(BaseCommand):
    help = "Import CSV data into the database"

    def handle(self, *args, **kwargs):

        if User.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Database already contains data. Skipping CSV import."
                )
            )
            return

        csv_folder = os.path.join(settings.BASE_DIR, "static/csv_files/")
        self.stdout.write(self.style.SUCCESS("Folder with CSV files: " + csv_folder))

        self.import_users(os.path.join(csv_folder, "users.csv"))
        self.import_credits(os.path.join(csv_folder, "credits.csv"))
        self.import_dictionary(os.path.join(csv_folder, "dictionary.csv"))
        self.import_plans(os.path.join(csv_folder, "plans.csv"))
        self.import_payments(os.path.join(csv_folder, "payments.csv"))

    def import_users(self, file_path):
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, sep="\t", dtype=str)
            df.columns = df.columns.str.strip().str.lower()
            print("Columns in CSV:", df.columns.tolist())

            for _, row in df.iterrows():
                User.objects.update_or_create(
                    id=row["id"],
                    defaults={
                        "login": row["login"],
                        "registration_date": convert_date(row["registration_date"]),
                    },
                )
            self.stdout.write(self.style.SUCCESS("Successfully imported users.csv"))
        else:
            self.stdout.write(self.style.WARNING("users.csv not found"))

    def import_credits(self, file_path):
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, sep="\t", dtype=str)
            df.columns = df.columns.str.strip().str.lower()
            for _, row in df.iterrows():
                Credit.objects.update_or_create(
                    id=row["id"],
                    defaults={
                        "user_id": row["user_id"],
                        "issuance_date": convert_date(row["issuance_date"]),
                        "return_date": convert_date(row["return_date"]),
                        "actual_return_date": convert_date(row["actual_return_date"]),
                        "body": row["body"],
                        "percent": row["percent"],
                    },
                )
            self.stdout.write(self.style.SUCCESS("Successfully imported credits.csv"))
        else:
            self.stdout.write(self.style.WARNING("credits.csv not found"))

    def import_dictionary(self, file_path):
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, sep="\t", dtype=str)
            df.columns = df.columns.str.strip().str.lower()
            for _, row in df.iterrows():
                Dictionary.objects.update_or_create(
                    id=row["id"], defaults={"name": row["name"]}
                )
            self.stdout.write(
                self.style.SUCCESS("Successfully imported dictionary.csv")
            )
        else:
            self.stdout.write(self.style.WARNING("dictionary.csv not found"))

    def import_plans(self, file_path):
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, sep="\t", dtype=str)
            df.columns = df.columns.str.strip().str.lower()
            for _, row in df.iterrows():
                Plan.objects.update_or_create(
                    id=row["id"],
                    defaults={
                        "period": convert_date(row["period"]),
                        "sum": row["sum"],
                        "category_id": row["category_id"],
                    },
                )
            self.stdout.write(self.style.SUCCESS("Successfully imported plans.csv"))
        else:
            self.stdout.write(self.style.WARNING("plans.csv not found"))

    def import_payments(self, file_path):
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, sep="\t", dtype=str)
            df.columns = df.columns.str.strip().str.lower()
            for _, row in df.iterrows():
                Payment.objects.update_or_create(
                    id=row["id"],
                    defaults={
                        "sum": row["sum"],
                        "payment_date": convert_date(row["payment_date"]),
                        "credit_id": row["credit_id"],
                        "type_id": row["type_id"],
                    },
                )
            self.stdout.write(self.style.SUCCESS("Successfully imported payments.csv"))
        else:
            self.stdout.write(self.style.WARNING("payments.csv not found"))


def convert_date(date_str):
    if pd.isna(date_str) or date_str in ["", "nan", "None"]:
        return None
    try:
        return datetime.strptime(str(date_str), "%d.%m.%Y").strftime("%Y-%m-%d")
    except ValueError:
        print(f"⚠ Warning: Invalid date format: {date_str}")
        return None
