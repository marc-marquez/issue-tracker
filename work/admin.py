from django.contrib import admin
from .models import Log
from .forms import LogForm


admin.site.register(Log)
