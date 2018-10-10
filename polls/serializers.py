from rest_framework import serializers
from .models import PollOption, Vote, Poll
from work.serializers import LogSerializer

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('subject_id')

class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('option_id','poll_id','user_id')

class VoteCustomSerializer(serializers.ModelSerializer):

    ticket_name = serializers.ReadOnlyField(source='option.ticket.name',read_only=True)
    status = serializers.ReadOnlyField(source='option.ticket.status',read_only=True)

    class Meta:
        model = Vote
        fields = ('option_id','poll_id','user_id','ticket_name','status')


class PollOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PollOption
        fields = ('poll_id','ticket_id')


class PollOptionCustomSerializer(serializers.ModelSerializer):
    ticket_name = serializers.ReadOnlyField(source='ticket.name',read_only=True)
    ticket_status = serializers.ReadOnlyField(source='ticket.status', read_only=True)
    vote_count = serializers.SerializerMethodField()

    #logs = LogSerializer(many=True,read_only=True)
    #logs = serializers.RelatedField(many=True,read_only=True)

    class Meta:
        model = PollOption
        fields = ('poll_id','ticket_id','ticket_name','vote_count','ticket_status')

    def get_vote_count(self,obj):
        return obj.votes.count()

class PollOptionVotesSerializer(serializers.ModelSerializer):
    vote_count = serializers.SerializerMethodField()

    class Meta:
        model = PollOption
        fields = ('vote_count','poll_id')

    def get_vote_count(self,obj):
        return obj.votes.count()