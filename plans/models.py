from django.db import models
from dictionary.models import Dictionary


class Plan(models.Model):
    period = models.DateField()
    sum = models.DecimalField(max_digits=10, decimal_places=2)
    category_id = models.ForeignKey(Dictionary, on_delete=models.CASCADE)

    def __str__(self):
        return f"Plan for {self.period}"
