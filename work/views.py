from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LogSerializer, LogCustomSerializer, LogCustomTicketSerializer
from .models import Log

class LogView(APIView):

    def get(self,request):
        log_items = Log.objects.all()
        serializer = LogSerializer(log_items,many=True)
        serialized_data = serializer.data
        return Response(serialized_data)

class LogCustomView(APIView):

    def get(self,request):
        log_items = Log.objects.all()
        serializer = LogCustomSerializer(log_items,many=True)
        serialized_data = serializer.data
        return Response(serialized_data)

class LogCustomTicketView(APIView):

    def get(self,request):
        log_items = Log.objects.all()
        serializer = LogCustomTicketSerializer(log_items,many=True)
        serialized_data = serializer.data
        return Response(serialized_data)

