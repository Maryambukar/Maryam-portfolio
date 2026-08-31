from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('logout/', LogoutView.as_view(next_page='core:home'), name='logout'),
]
