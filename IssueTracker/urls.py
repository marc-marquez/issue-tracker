"""IssueTracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from main import views as main_views
from accounts import views as accounts_views
from tickets import views as forum_views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', main_views.get_index, name='index'),
    url(r'^register/$', accounts_views.register, name='register'),
    url(r'^profile/$', accounts_views.profile, name='profile'),
    url(r'^login/$', accounts_views.login, name='login'),
    url(r'^logout/$', accounts_views.logout, name='logout'),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^forum/$', forum_views.forum),
    url(r'^tickets/(?P<subject_id>\d+)/$', forum_views.tickets, name='tickets'),
    url(r'^ticket/new/(?P<subject_id>\d+)/$',  forum_views.new_ticket, name='new_ticket'),
    url(r'^ticket/edit/(?P<ticket_id>\d+)/$',  forum_views.edit_ticket, name='edit_ticket'),
    url(r'^ticket/(?P<ticket_id>\d+)/$', forum_views.ticket, name='ticket'),
    url(r'^post/new/(?P<ticket_id>\d+)/$', forum_views.new_post, name='new_post'),
    url(r'^post/edit/(?P<ticket_id>\d+)/(?P<post_id>\d+)/$',forum_views.edit_post, name='edit_post'),
    url(r'^post/delete/(?P<ticket_id>\d+)/(?P<post_id>\d+)/$', forum_views.delete_post, name='delete_post'),
    url(r'^ticket/vote/(?P<ticket_id>\d+)/(?P<subject_id>\d+)/$', forum_views.ticket_vote, name='cast_vote'),
    url(r'^profile/cards/add/$', accounts_views.add_card, name='add_card'),
    url(r'^ticket/donate/(?P<ticket_id>\d+)/(?P<subject_id>\d+)/$', forum_views.ticket_donate, name='donate'),
    #url(r'^profile/cards/$', accounts_views.get_cards, name='cards'),
    url(r'^profile/cards/delete/(?P<card_id>card_.*)/$', accounts_views.delete_card, name='delete_card'),
    url(r'^profile/cards/default/(?P<card_id>card_.*)/$', accounts_views.set_default_card, name='set_default_card'),
    url(r'^report/(?P<subject_id>\d+)/$', forum_views.report, name='report'),
    url(r'^ticket/customdonate/(?P<ticket_id>\d+)/(?P<subject_id>\d+)/$', forum_views.custom_donate, name='custom_donate'),
    url(r'^ticket_serial/', include('tickets.urls')),
    url(r'^polls/', include('polls.urls')),
    url(r'^report/dashboard/$', forum_views.dashboard, name='dashboard'),
]
