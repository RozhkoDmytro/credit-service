from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Credit
from .serializers import ClosedCreditSerializer, OpenCreditSerializer


class UserCreditsView(APIView):
    def get(self, request, user_id):
        credits = Credit.objects.filter(user_id=user_id)
        if not credits.exists():
            return Response(
                {"detail": "No credits found for this user"},
                status=status.HTTP_404_NOT_FOUND,
            )

        result = []
        for credit in credits:
            if credit.actual_return_date:
                serializer = ClosedCreditSerializer(credit)
            else:
                serializer = OpenCreditSerializer(credit)
            result.append(serializer.data)

        return Response(result, status=status.HTTP_200_OK)
