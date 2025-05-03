from django.urls import path
from . import views

app_name = 'retell_agent'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_agent, name='create_agent'),
    path('edit/<int:agent_id>/', views.edit_agent, name='edit_agent'),
    path('delete/<int:agent_id>/', views.delete_agent, name='delete_agent'),
]
