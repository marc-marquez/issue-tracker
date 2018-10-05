from rest_framework import serializers
from .models import PollOption, Vote

class PollOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollOption
        fields = ('poll_id','ticket_id')

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('option_id','poll_id','user_id')