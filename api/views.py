from django.db import connections
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# check db health view
@api_view(["GET"])
def check_db_health(request):
    # try to execute simple script in db
    try:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1")

        return Response("Database is healthy", status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            f"Database is not working: {str(e)}",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
