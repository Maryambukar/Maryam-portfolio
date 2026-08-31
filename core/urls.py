from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('download-cv/', views.download_cv, name='download_cv'),
    path('control/login/', views.secure_admin_login, name='admin_login'),
]
