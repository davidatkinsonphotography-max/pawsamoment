from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import AnimalProfile


def adoption_list_view(request):
    animals = AnimalProfile.objects.filter(archived=False)
    
    # Filtering
    search_query = request.GET.get('q', '')
    species_filter = request.GET.getlist('species')
    size_filter = request.GET.getlist('size')
    sex_filter = request.GET.getlist('sex')
    
    if search_query:
        animals = animals.filter(
            Q(animal_name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(breed__icontains=search_query)
        )
    
    if species_filter:
        animals = animals.filter(species__in=species_filter)
    
    if size_filter:
        animals = animals.filter(size__in=size_filter)
    
    if sex_filter:
        animals = animals.filter(sex__in=sex_filter)
    
    # Only show available/pending/soon animals
    animals = animals.filter(status__in=['AVAILABLE', 'SOON', 'PENDING'])
    
    context = {
        'animals': animals,
        'search_query': search_query,
        'species_filter': species_filter,
        'size_filter': size_filter,
        'sex_filter': sex_filter,
        'species_choices': AnimalProfile.SPECIES_CHOICES,
        'size_choices': AnimalProfile.SIZE_CHOICES,
        'sex_choices': AnimalProfile.SEX_CHOICES,
    }
    
    return render(request, 'animals/adoption_list.html', context)


def animal_detail_view(request, slug):
    animal = get_object_or_404(AnimalProfile, slug=slug, archived=False)
    gallery_images = animal.gallery_images.all()
    
    context = {
        'animal': animal,
        'gallery_images': gallery_images,
    }
    
    return render(request, 'animals/animal_detail.html', context)
