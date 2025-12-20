from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q
from animals.models import AnimalProfile
from applications.models import CatApplication, DogApplication, FosterApplication, ContactMessage
from news.models import NewsArticle
from core.models import SiteVisit, AnimalView
import csv
from django.http import HttpResponse


@staff_member_required
def dashboard_view(request):
    # Time ranges
    today = timezone.now().date()
    this_month_start = today.replace(day=1)
    last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
    last_month_end = this_month_start - timedelta(days=1)
    
    # Animal statistics
    total_animals = AnimalProfile.objects.count()
    available_animals = AnimalProfile.objects.filter(status='AVAILABLE', archived=False).count()
    adopted_animals = AnimalProfile.objects.filter(status='ADOPTED').count()
    adopted_this_month = AnimalProfile.objects.filter(
        status='ADOPTED',
        date_entered__gte=this_month_start
    ).count()
    most_viewed = AnimalProfile.objects.filter(archived=False).order_by('-view_count')[:10]
    
    # Application statistics
# UPDATED Application statistics
    # We now sum Cats + Dogs to get the totals
    total_cat_apps = CatApplication.objects.count()
    total_dog_apps = DogApplication.objects.count()
    total_adoption_apps = total_cat_apps + total_dog_apps

    cat_apps_this_month = CatApplication.objects.filter(date_submitted__gte=this_month_start).count()
    dog_apps_this_month = DogApplication.objects.filter(date_submitted__gte=this_month_start).count()
    adoption_apps_this_month = cat_apps_this_month + dog_apps_this_month

    unprocessed_cat = CatApplication.objects.filter(processed=False).count()
    unprocessed_dog = DogApplication.objects.filter(processed=False).count()
    unprocessed_adoption_apps = unprocessed_cat + unprocessed_dog
    
    total_foster_apps = FosterApplication.objects.count()
    foster_apps_this_month = FosterApplication.objects.filter(
        date_submitted__gte=this_month_start
    ).count()
    unprocessed_foster_apps = FosterApplication.objects.filter(processed=False).count()
    
    # Contact messages
    total_contacts = ContactMessage.objects.count()
    unprocessed_contacts = ContactMessage.objects.filter(processed=False).count()
    
    # Site statistics
    total_visits = SiteVisit.objects.count()
    visits_this_month = SiteVisit.objects.filter(
        timestamp__gte=this_month_start
    ).count()
    unique_visitors_this_month = SiteVisit.objects.filter(
        timestamp__gte=this_month_start
    ).values('ip_address').distinct().count()
    
    # News statistics
    total_news = NewsArticle.objects.count()
    published_news = NewsArticle.objects.filter(published=True).count()
    
    context = {
        'total_animals': total_animals,
        'available_animals': available_animals,
        'adopted_animals': adopted_animals,
        'adopted_this_month': adopted_this_month,
        'most_viewed': most_viewed,
        'total_adoption_apps': total_adoption_apps,
        'adoption_apps_this_month': adoption_apps_this_month,
        'unprocessed_adoption_apps': unprocessed_adoption_apps,
        'total_foster_apps': total_foster_apps,
        'foster_apps_this_month': foster_apps_this_month,
        'unprocessed_foster_apps': unprocessed_foster_apps,
        'total_contacts': total_contacts,
        'unprocessed_contacts': unprocessed_contacts,
        'total_visits': total_visits,
        'visits_this_month': visits_this_month,
        'unique_visitors_this_month': unique_visitors_this_month,
        'total_news': total_news,
        'published_news': published_news,
    }
    
    return render(request, 'dashboard/dashboard.html', context)


@staff_member_required
def export_csv_view(request, model_type):
    """Export CSV for various models"""
    response = HttpResponse(content_type='text/csv')
    
    if model_type == 'animals':
        response['Content-Disposition'] = 'attachment; filename="animals.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Animal Name', 'Species', 'Breed', 'Sex', 'Size', 'Status', 
            'Adoption Fee', 'Location', 'View Count', 'Date Entered'
        ])
        for animal in AnimalProfile.objects.all():
            writer.writerow([
                animal.animal_name, animal.species, animal.breed, animal.sex,
                animal.size, animal.status, animal.adoption_fee, animal.location,
                animal.view_count, animal.date_entered
            ])
    
    elif model_type == 'cat_applications':
        response['Content-Disposition'] = 'attachment; filename="cat_applications.csv"'
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Email', 'Pet Name', 'Coat Pref', 'Date Submitted'])
        for app in CatApplication.objects.all():
            writer.writerow([app.first_name, app.last_name, app.email, app.pet_name, app.coat_pref, app.date_submitted])

    elif model_type == 'dog_applications':
        response['Content-Disposition'] = 'attachment; filename="dog_applications.csv"'
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Email', 'Pet Name', 'Yard Size', 'Fence Details', 'Date Submitted'])
        for app in DogApplication.objects.all():
            writer.writerow([app.first_name, app.last_name, app.email, app.pet_name, app.yard_size, app.fence_details, app.date_submitted])
    
    elif model_type == 'foster_applications':
        response['Content-Disposition'] = 'attachment; filename="foster_applications.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'First Name', 'Last Name', 'Email', 'Mobile', 'Foster Type',
            'Date Submitted', 'Processed'
        ])
        for app in FosterApplication.objects.all():
            writer.writerow([
                app.first_name, app.last_name, app.email, app.mobile,
                app.foster_type, app.date_submitted, app.processed
            ])
    
    elif model_type == 'contact_messages':
        response['Content-Disposition'] = 'attachment; filename="contact_messages.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Message', 'Date Submitted', 'Processed'])
        for msg in ContactMessage.objects.all():
            writer.writerow([
                msg.name, msg.email, msg.message, msg.date_submitted, msg.processed
            ])
    
    elif model_type == 'news':
        response['Content-Disposition'] = 'attachment; filename="news_articles.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Title', 'Category', 'Published', 'Expiry Date', 'View Count', 'Date Entered'
        ])
        for article in NewsArticle.objects.all():
            writer.writerow([
                article.title, article.category, article.published,
                article.expiry_date, article.view_count, article.date_entered
            ])
    
    return response
