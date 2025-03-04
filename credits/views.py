from django.db import connection
from rest_framework.response import Response
from rest_framework import viewsets
from django.http import Http404
from datetime import date
from .serializers import ClosedCreditSerializer, OpenCreditSerializer


class UserCreditsRawSQLView(viewsets.ViewSet):
    """
    -- This is not the best practice because it hardcodes dictionary values ('Тіло', 'Відсотки') in the query.
    -- Ideally, we should reference type_id directly instead of querying by name.
    -- However, since the dictionary table already has fixed values, this is more of a structural issue rather than just a query optimization concern.
    -- A better long-term solution would be to store and use predefined type IDs in application logic rather than relying on text-based matching.
    """

    def list(self, request, user_id):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    c.id, 
                    c.issuance_date, 
                    c.return_date, 
                    CAST(c.body AS DECIMAL(10,2)) AS body, 
                    CAST(c.percent AS DECIMAL(10,2)) AS percent,
                    c.actual_return_date IS NOT NULL AS is_closed,
                    c.actual_return_date,
                    CAST(COALESCE(SUM(p.sum), 0.00) AS DECIMAL(10,2)) AS total_payments,
                    CAST(COALESCE(SUM(CASE WHEN d.name = 'Тіло' THEN p.sum ELSE 0.00 END), 0.00) AS DECIMAL(10,2)) AS principal_payments,
                    CAST(COALESCE(SUM(CASE WHEN d.name = 'Відсотки' THEN p.sum ELSE 0.00 END), 0.00) AS DECIMAL(10,2)) AS interest_payments
                FROM credits_credit c
                LEFT JOIN payments_payment p ON c.id = p.credit_id
                LEFT JOIN dictionary_dictionary d ON p.type_id = d.id
                WHERE c.user_id = %s
                GROUP BY c.id, c.issuance_date, c.return_date, c.body, c.percent, c.actual_return_date;
            """,
                [user_id],
            )

            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        if not results:
            raise Http404("No credits found for this user.")

        serialized_data = []
        today = date.today()

        for credit in results:
            if credit["is_closed"]:
                serializer = ClosedCreditSerializer(credit)
            else:
                credit["overdue_days"] = (
                    max((today - credit["return_date"]).days, 0)
                    if credit["return_date"]
                    else 0
                )
                serializer = OpenCreditSerializer(credit)

            serialized_data.append(serializer.data)

        return Response(serialized_data)
