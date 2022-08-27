from django.urls import path

from . import views

urlpatterns = [
    path('users/', views.users),
    path('get_data/', views.get_data),
    path('' ,views.view_users)
]
