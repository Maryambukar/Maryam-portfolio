from django.contrib import admin

from .models import Achievement, Certification, Experience, Project, Skill, SkillCategory


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'issuer', 'date_earned', 'order')
    list_editable = ('order',)
    ordering = ('order',)


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    inlines = [SkillInline]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'order')
    list_editable = ('is_featured', 'order')
    ordering = ('order',)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role_title', 'organization', 'period', 'order')
    list_editable = ('order',)
    ordering = ('order',)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'detail', 'order')
    list_editable = ('order',)
    ordering = ('order',)
