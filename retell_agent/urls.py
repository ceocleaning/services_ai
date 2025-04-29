from django.urls import path
from . import views

app_name = 'retell_agent'

urlpatterns = [
    path('', views.index, name='index'),
]
