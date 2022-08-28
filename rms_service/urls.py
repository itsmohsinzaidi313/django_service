from django.urls import path
from rms_service import views

urlpatterns = [
    path('config', views.config)
]
