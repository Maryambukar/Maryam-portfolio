from django.contrib import admin

from .models import AcademicFact, AdminLoginAttempt, EducationEntry, SiteOwner


@admin.register(SiteOwner)
class SiteOwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'headline', 'email')

    def has_add_permission(self, request):
        # Singleton: block adding a second row once one exists.
        return not SiteOwner.objects.exists()


@admin.register(AcademicFact)
class AcademicFactAdmin(admin.ModelAdmin):
    list_display = ('owner', 'degree_program', 'cgpa', 'deans_list')


@admin.register(EducationEntry)
class EducationEntryAdmin(admin.ModelAdmin):
    list_display = ('institution', 'program', 'period', 'order')
    list_editable = ('order',)
    ordering = ('order',)


@admin.register(AdminLoginAttempt)
class AdminLoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('username_tried', 'ip_address', 'was_successful', 'timestamp')
    list_filter = ('was_successful',)
    readonly_fields = [f.name for f in AdminLoginAttempt._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
