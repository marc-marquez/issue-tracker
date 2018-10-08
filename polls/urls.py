from django.conf.urls import url
from .views import PollOptionView, VoteView, OptionView

urlpatterns = [
    url(r'^polloptions/$', PollOptionView.as_view()),
    url(r'^votes/$', VoteView.as_view()),
    url(r'^options/$', OptionView.as_view()),
]