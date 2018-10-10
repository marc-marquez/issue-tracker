from rest_framework import serializers
from tickets.models import Ticket
from polls.serializers import PollOptionVotesSerializer,PollOptionCustomSerializer,PollOptionSerializer,VoteSerializer
from work.serializers import LogCustomTicketSerializer
from work.models import Log
from collections import OrderedDict

class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ('name','subject','user','status')

class TicketCustomSerializer(serializers.ModelSerializer):
    logs = LogCustomTicketSerializer(many=True,read_only=True)
    options = PollOptionVotesSerializer(many=False,read_only=True)

    class Meta:
        model = Ticket
        fields = ('name','subject','user','status','logs','options')

'''
class TicketCustomSerializer(serializers.ModelSerializer):
    logs = LogCustomTicketSerializer(many=True, read_only=True)
    options = PollOptionVotesSerializer(many=False, read_only=True)

    class Meta:
        model = Ticket
        fields = ('name','subject','user','status','logs','options')

    def to_representation(self, obj):
        rep = super().to_representation(obj)
        logs_rep = rep.pop('logs')

        #Store the key names in a dict

        print(logs_rep)
        for log in logs_rep:
            for key,value in log.items():
                print(key, value)
                rep[key] = value

        
        #options_rep = rep.pop('options')
        #print(options_rep)
        #
        #for option in options_rep:
        #    if option is None:
        #        print ("Nothing here!")
        #    else:
        #        print(option)
        #    #for key, value in option.items():
        #    #    print(key,value)
        
        return rep
'''

