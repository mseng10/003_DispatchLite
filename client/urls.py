from django.urls import path
from client import views

urlpatterns = [
    path('client/', views.client),
    path('templates/', views.templates),
    path('templates/<int:id>', views.template),
    path('campaigns/', views.campaign),
    path('populations/', views.population),
    path('campaigns/<str:campaign_id>/communications', views.communication)
]
