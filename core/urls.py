from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('donate/', views.DonateView.as_view(), name='donate'),
    path('guides/', views.GuidesView.as_view(), name='guides'),
    path('contact/', views.contact_view, name='contact'),
    path('applications/', include('applications.urls')),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-use/', views.terms_of_use, name='terms_of_use'),
    path('adoption-policy/', views.adoption_policy, name='adoption_policy'),
    path('success-stories/', views.success_stories, name='success_stories'),
    path('about-us/', views.about_us, name='about_us'),
    path('surrender/', views.surrender_view, name='surrender'),
    path('ways-to-help/', views.ways_to_help, name='ways_to_help'),
    path('success/', views.application_success_view, name='application_success'),
]

