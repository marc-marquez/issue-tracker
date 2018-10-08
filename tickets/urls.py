from django.conf.urls import url
from tickets.views import TicketView

urlpatterns = [
    url(r'^ticket/$', TicketView.as_view()),
    #url(r'^votes/$', TicketVotesView.as_view()),
]