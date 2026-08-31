from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at', 'email_sent')
    list_filter = ('email_sent',)
    readonly_fields = ('name', 'email', 'subject', 'message', 'submitted_at', 'email_sent')

    def has_add_permission(self, request):
        return False
