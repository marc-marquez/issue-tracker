from django.conf.urls import url
from .views import PollOptionView, VoteView

urlpatterns = [
    url(r'^polloptions/$', PollOptionView.as_view()),
    url(r'^votes/$', VoteView.as_view()),
]