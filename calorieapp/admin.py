from django.contrib import admin
from .models import UserLog

@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    list_display = ('search_term', 'ip_address', 'timestamp')
    search_fields = ('search_term',)

