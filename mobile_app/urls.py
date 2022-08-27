from django.urls import path

from mobile_app import views
urlpatterns = [
    path('login/', views.login),
    path('sync/', views.sync),
    path('getdata/', views.get_data),
    path('getshifts/', views.get_shifts_list)
]
