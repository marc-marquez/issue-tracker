from rest_framework import serializers
from tickets.models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('name','subject','user','status')