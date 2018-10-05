from django.conf.urls import url
from tickets.views import TicketView

urlpatterns = [
    url(r'^$', TicketView.as_view())
]