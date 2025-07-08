from django.contrib import admin
from django.urls import path, include  # Used to include URLs from the documents app
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('documents.urls')),  # Assuming 'documents' is the name of your app
    # You can include other apps here as well
]

# Serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serving static files during development (if not handled by another service like WhiteNoise)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
