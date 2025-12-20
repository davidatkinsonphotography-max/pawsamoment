from django.urls import path
from . import views

app_name = 'animals'

urlpatterns = [
    path('', views.adoption_list_view, name='adoption_list'),
    path('<slug:slug>/', views.animal_detail_view, name='animal_detail'),
]

