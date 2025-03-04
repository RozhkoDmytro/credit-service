from django.urls import path
from .views import UserCreditsView

urlpatterns = [
    path("user_credits/<int:user_id>/", UserCreditsView.as_view(), name="user_credits"),
]
