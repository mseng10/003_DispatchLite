from django.urls import path
from client import views

urlpatterns = [
    path('client/', views.client),
    path('templates/', views.templates),
    path('templates/<int:id>', views.template),
    path('campaigns/', views.campaign),
    path('populations/', views.population),
    path('batches/<int:id>/', views.batches),
    path('messages/<str:member_id>/', views.messages),

]
