from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('donate/', views.DonateView.as_view(), name='donate'),
    path('guides/', views.GuidesView.as_view(), name='guides'),
    path('contact/', views.contact_view, name='contact'),
    path('applications/', include('applications.urls')),
]

