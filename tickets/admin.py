from django.contrib import admin
from .models import Subject, Ticket, Post

admin.site.register(Subject)
admin.site.register(Ticket)
admin.site.register(Post)