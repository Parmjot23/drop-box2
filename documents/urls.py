from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='home'),
    path('upload/', views.main, name='upload_file'),
    path('photos/', views.photos, name='photos'),
    path('videos/', views.videos, name='videos'),
    path('others/', views.others, name='others'),
    path('documents/<int:document_id>/', views.document_detail, name='document_detail'),
    path('search/', views.search, name='search'),
    path('documents/<int:document_id>/delete/', views.delete_document, name='delete_document'),
    path('documents/<int:document_id>/rename/', views.rename_document, name='rename_document'),
]
