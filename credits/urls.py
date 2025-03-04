from django.urls import path
from .views import UserCreditsRawSQLView

urlpatterns = [
    path(
        "user_credits/<int:user_id>/",
        UserCreditsRawSQLView.as_view({"get": "list"}),
        name="user_credits",
    ),
]
