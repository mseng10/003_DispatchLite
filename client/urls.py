from django.urls import path
from client import views

urlpatterns = [
    path('client/', views.client),
    path('templates/', views.templates),
    path('templates/<int:id>', views.template)
]