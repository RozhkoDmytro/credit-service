from django.urls import path
from .views import PlansInsertView

urlpatterns = [
    path("plans_insert/", PlansInsertView.as_view(), name="plans_insert"),
]
