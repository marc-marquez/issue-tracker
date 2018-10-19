from __future__ import unicode_literals
from rest_framework.response import Response
from rest_framework.views import APIView
#from .serializers import PollSerializer,VoteSerializer,PollOptionSerializer,VoteCustomSerializer,\
#    PollOptionCustomSerializer,PollOptionVotesSerializer
#from .models import PollOption,Vote
from django.shortcuts import render

'''
class PollView(APIView):
    def get(self,request):
        polloption_items = PollOption.objects.all()
        serializer = PollOptionSerializer(polloption_items,many=True)
        serialized_data = serializer.data
        return Response(serialized_data)

class VoteView(APIView):
    def get(self,request):
        vote_items = Vote.objects.all()
        serializer = VoteSerializer(vote_items,many=True)
        serialized_data = serializer.data
        return Response(serialized_data)

class VoteCustomView(APIView):
    def get(self,request):
        vote_items = Vote.objects.all()
        serializer = VoteCustomSerializer(vote_items,many=True)
        serialized_data = serializer.data
        return Response(serialized_data)

class PollOptionView(APIView):
    def get(self,request):
        option_items = PollOption.objects.all()
        serializer = PollOptionSerializer(option_items,many=True)
        serialized_data = serializer.data
        return Response(serialized_data)

class PollOptionCustomView(APIView):
    def get(self,request):
        option_items = PollOption.objects.all()
        serializer = PollOptionCustomSerializer(option_items,many=True)
        serialized_data = serializer.data
        return Response(serialized_data)

class PollOptionVotesCustomView(APIView):
    def get(self,request):
        option_items = PollOption.objects.all()
        serializer = PollOptionVotesSerializer(option_items,many=True)
        serialized_data = serializer.data
        return Response(serialized_data)
'''


