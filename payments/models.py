from django.db import models
from credits.models import Credit
from plans.models import Dictionary


class Payment(models.Model):
    credit = models.ForeignKey(
        Credit, on_delete=models.CASCADE, related_name="payments"
    )
    sum = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    type = models.ForeignKey(Dictionary, on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment {self.id} - {self.sum}"
