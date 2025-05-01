from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('webhook/', views.whatsapp_webhook),
    path('ai-model/', views.AI_model),
]
