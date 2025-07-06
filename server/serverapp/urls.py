from django.urls import path
from . import views

urlpatterns = [
    path('uploadDoc/', views.uploadDocument, name = 'uploadDocument'),
    path('getResponse/', views.getLLMResponse, name = 'getLLMResponse'),
    path('getDocs/', views.getDocumentList, name = 'getDocumentList')
]