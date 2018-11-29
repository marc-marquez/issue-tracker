from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    fields = ('username','email','is_staff','is_superuser','is_active')

# Register your models here.
admin.site.register(User,UserAdmin)
