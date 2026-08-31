from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django's built-in admin stays put but is only ever reachable by
    # someone who already authenticated through the secured gate below.
    path('django-admin/', admin.site.urls),

    path('', include('core.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('contact/', include('contact.urls', namespace='contact')),
    path('chatbot/', include('chatbot.urls')),
    path('control/', include('dashboard.urls')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
