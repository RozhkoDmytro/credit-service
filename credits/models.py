from django.db import models
from users.models import User


class Credit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="credits")
    issuance_date = models.DateField()
    return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    body = models.DecimalField(max_digits=10, decimal_places=2)
    percent = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Credit {self.id} for {self.user.login}"
