"""
View to use the REST framework to serialize the work data
"""
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LogCustomSerializer
from .models import Log


class LogCustomView(APIView):
    """
    Class to process log request types
    """
    def get(self, request):
        """
        Returns a get request of the serialized work data
        :param request: The request type
        :return: serialized data
        """
        log_items = Log.objects.all()
        serializer = LogCustomSerializer(log_items, many=True)
        serialized_data = serializer.data
        return Response(serialized_data)

