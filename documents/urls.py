from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='home'),
    path('upload/', views.main, name='upload_file'),
    path('photos/', views.photos, name='photos'),
    path('videos/', views.videos, name='videos'),
    path('others/', views.others, name='others'),
    # In your urls.py
    path('documents/<int:document_id>/', views.document_detail, name='document_detail'),
]
