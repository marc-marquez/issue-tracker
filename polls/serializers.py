from rest_framework import serializers
from .models import PollOption, Vote, Poll
from tickets.serializers import TicketSerializer
from tickets.models import Ticket

class PollOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollOption
        fields = ('poll_id','ticket_id')

class VoteSerializer(serializers.ModelSerializer):

    ticket_name = serializers.ReadOnlyField(source='option.ticket.name',read_only=True)
    status = serializers.ReadOnlyField(source='option.ticket.status',read_only=True)

    class Meta:
        model = Vote
        fields = ('option_id','poll_id','user_id','ticket_name','status')



class OptionSerializer(serializers.ModelSerializer):
    ticket_name = serializers.ReadOnlyField(source='ticket.name',read_only=True)
    ticket_status = serializers.ReadOnlyField(source='ticket.status', read_only=True)
    #feature_donations_goal = serializers.ReadOnlyField(source='ticket.feature.donation_goal', read_only=True)
    vote_count = serializers.SerializerMethodField()

    class Meta:
        model = PollOption
        fields = ('poll_id','ticket_id','ticket_name','vote_count','ticket_status')

    def get_vote_count(self,obj):
        return obj.votes.count()
