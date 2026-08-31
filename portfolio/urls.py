from django.urls import path

from . import views

app_name = 'portfolio'

urlpatterns = [
    path('projects/', views.projects_list, name='projects_list'),
    path('certifications/', views.certifications_list, name='certifications_list'),
]
