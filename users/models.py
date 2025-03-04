from django.db import models


class User(models.Model):
    login = models.CharField(max_length=255, unique=True)
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.login
