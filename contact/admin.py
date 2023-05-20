from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message', 'sent',)
    search_fields = ['name', 'subject', 'sent', 'email']
    list_filter = ('subject', 'sent',)

    ordering = ('sent',)
