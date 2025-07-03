from django.urls import path
from . import views

urlpatterns = [
    path('uploadDoc/', views.uploadDocument, name = 'uploadDocument'),
    path('getDoc/', views.getDocument, name = 'getDocument')
]