from rest_framework import serializers
from .models import Credit
from payments.serializers import PaymentSerializer


class CreditSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Credit
        fields = [
            "id",
            "user_id",
            "issuance_date",
            "return_date",
            "actual_return_date",
            "body",
            "percent",
            "payments",
        ]
