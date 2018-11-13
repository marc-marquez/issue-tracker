from django.conf.urls import url
from .views import LogCustomView

urlpatterns = [
    url(r'^log/custom/$', LogCustomView.as_view()),
]