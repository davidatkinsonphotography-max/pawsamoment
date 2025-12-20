# applications/urls.py
from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    # Adoption URLs
    path('adopt/', views.adoption_landing, name='adoption_landing_page'),
    path('adopt/cat/', views.cat_application_view, name='cat_adoption'), # Ensure this matches views.py
    path('adopt/dog/', views.dog_application_view, name='dog_adoption'),
    path('adopt/success/', views.application_success_view, name='application_success'),

    # Foster URLs
    path('foster/info/', views.foster_info_view, name='foster_info'),
    path('foster/apply/', views.foster_application_view, name='foster_application'),
    path('foster/success/', views.foster_success_view, name='foster_success'),
]