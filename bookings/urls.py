from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_booking, name='create_booking'),
]
