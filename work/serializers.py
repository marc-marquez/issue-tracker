"""
Serialize work logs for use in work dashboard graphs (dashboard_graph.js)
"""
from rest_framework import serializers
from .models import Log


class LogCustomSerializer(serializers.ModelSerializer):
    """
    Serialize work log data
    """
    ticket_type = serializers.ReadOnlyField(source='ticket.subject.name', read_only=True)
    ticket_name = serializers.ReadOnlyField(source='ticket.name', read_only=True)
    ticket_status = serializers.ReadOnlyField(source='ticket.status', read_only=True)

    class Meta:
        """
        Fields that are included in the serialized data
        """
        model = Log
        fields = ('ticket_id', 'user_id', 'date', 'hours', 'ticket_type',
                  'ticket_name', 'ticket_status')
