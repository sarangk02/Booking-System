from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),  # URL for the admin site
    path('', include('booking.urls')),  # Include URLs from the 'booking' app
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # URL for obtaining JWT token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # URL for refreshing JWT token
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files in development mode
