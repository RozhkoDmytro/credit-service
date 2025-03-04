from rest_framework import serializers
from .models import Plan
from dictionary.serializers import DictionarySerializer


class PlanSerializer(serializers.ModelSerializer):
    category = DictionarySerializer()

    class Meta:
        model = Plan
        fields = ["id", "period", "sum", "categor_id"]


class PlanUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
