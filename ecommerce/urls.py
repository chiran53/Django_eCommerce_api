from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as drf_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('shop.urls')), 
    path('api/auth/', include('rest_framework.urls')), 
    path('api/token-auth/', drf_views.obtain_auth_token, name='api_token_auth'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)