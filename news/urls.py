from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_list_view, name='news_list'),
    path('<slug:slug>/', views.news_detail_view, name='news_detail'),
    path('guide/dog/', views.guide_dog, name='guide_dog'),
    path('guide/puppy/', views.guide_puppy, name='guide_puppy'),
    path('guide/cat/', views.guide_cat, name='guide_cat'),
    path('guide/kitten/', views.guide_kitten, name='guide_kitten'),
]

