from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('export/<str:model_type>/', views.export_csv_view, name='export_csv'),
]

