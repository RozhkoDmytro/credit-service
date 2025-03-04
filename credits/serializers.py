from rest_framework import serializers
from .models import Credit
from payments.models import Payment
from django.db.models import Sum
from datetime import date


class ClosedCreditSerializer(serializers.ModelSerializer):
    is_closed = serializers.SerializerMethodField()
    total_payments = serializers.SerializerMethodField()

    class Meta:
        model = Credit
        fields = [
            "issuance_date",
            "is_closed",
            "return_date",
            "body",
            "percent",
            "total_payments",
        ]

    def get_is_closed(self, obj):
        return True

    def get_total_payments(self, obj):
        return (
            # TODO: Optimize this query
            Payment.objects.filter(credit_id=obj.id).aggregate(total=Sum("sum"))[
                "total"
            ]
            or 0
        )


class OpenCreditSerializer(serializers.ModelSerializer):
    is_closed = serializers.SerializerMethodField()
    overdue_days = serializers.SerializerMethodField()
    principal_payments = serializers.SerializerMethodField()
    interest_payments = serializers.SerializerMethodField()

    class Meta:
        model = Credit
        fields = [
            "issuance_date",
            "is_closed",
            "return_date",
            "overdue_days",
            "body",
            "percent",
            "principal_payments",
            "interest_payments",
        ]

    def get_is_closed(self, obj):
        return False

    def get_overdue_days(self, obj):
        return (
            (date.today() - obj.return_date).days
            if date.today() > obj.return_date
            else 0
        )

    def get_principal_payments(self, obj):
        return (
            # TODO: Optimize this query
            Payment.objects.filter(credit_id=obj.id, type__name="Тіло").aggregate(
                total=Sum("sum")
            )["total"]
            or 0
        )

    def get_interest_payments(self, obj):
        return (
            # TODO: Optimize this query
            Payment.objects.filter(credit_id=obj.id, type__name="Відсотки").aggregate(
                total=Sum("sum")
            )["total"]
            or 0
        )
