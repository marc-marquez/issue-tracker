from rest_framework import serializers
from tickets.models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('name','subject','user','status')

'''
class TicketVotesSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True,read_only=True)

    class Meta:
        model = Ticket
        fields = ('name', 'subject', 'user', 'status','votes')
'''