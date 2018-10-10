from django.conf.urls import url
from .views import LogView, LogCustomView,LogCustomTicketView

urlpatterns = [
    url(r'^log/$', LogView.as_view()),
    url(r'^log/custom/$', LogCustomView.as_view()),
    url(r'^log/custom_t/$', LogCustomTicketView.as_view()),
]