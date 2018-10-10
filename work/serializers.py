from rest_framework import serializers
from .models import Log

class LogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Log
        fields = ('ticket_id','user_id','date','hours')

class LogCustomSerializer(serializers.ModelSerializer):
    ticket_type = serializers.ReadOnlyField(source='ticket.subject.name',read_only=True)
    ticket_name = serializers.ReadOnlyField(source='ticket.name', read_only=True)
    ticket_status = serializers.ReadOnlyField(source='ticket.status', read_only=True)

    class Meta:
        model = Log
        fields = ('ticket_id','user_id','date','hours','ticket_type','ticket_name','ticket_status')

class LogCustomTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ('user_id','date','hours')