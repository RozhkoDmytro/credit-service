from rest_framework import serializers


class ClosedCreditSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    issuance_date = serializers.DateField()
    is_closed = serializers.BooleanField(default=True)
    return_date = serializers.DateField()
    body = serializers.DecimalField(max_digits=10, decimal_places=2)
    percent = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_payments = serializers.DecimalField(max_digits=10, decimal_places=2)


class OpenCreditSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    issuance_date = serializers.DateField()
    is_closed = serializers.BooleanField(default=False)
    return_date = serializers.DateField()
    overdue_days = serializers.IntegerField()
    body = serializers.DecimalField(max_digits=10, decimal_places=2)
    percent = serializers.DecimalField(max_digits=10, decimal_places=2)
    principal_payments = serializers.DecimalField(max_digits=10, decimal_places=2)
    interest_payments = serializers.DecimalField(max_digits=10, decimal_places=2)
