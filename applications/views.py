from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CatApplication, DogApplication, FosterApplication, FosterApplicationImage

# --- 1. THE ADOPTION PORTAL (Choice Page) ---
def adoption_landing(request):
    return render(request, 'applications/adoptionlanding.html')

# --- 2. CAT ADOPTION VIEW ---
def cat_application_view(request):
    if request.method == 'POST':
        # You can keep using your Form here or manual create. 
        # Since you have the logic in your manual Foster view, let's stick to the manual style for consistency:
        app = CatApplication.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            mobile=request.POST.get('mobile'),
            address_street=request.POST.get('address_street'),
            address_city=request.POST.get('address_city'),
            pet_name=request.POST.get('pet_name'),
            # ... add any other cat fields you need saved manually here ...
        )
        return redirect('applications:application_success')
    return render(request, 'applications/catadoption.html')

# --- 3. DOG ADOPTION VIEW ---
def dog_application_view(request):
    if request.method == 'POST':
        app = DogApplication.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            mobile=request.POST.get('mobile'),
            pet_name=request.POST.get('pet_name'),
            # ... add any other dog fields you need saved manually here ...
        )
        return redirect('applications:application_success')
    return render(request, 'applications/dogadoption.html')

# --- 4. FOSTER SYSTEM (The Long Logic You Wrote) ---

def foster_info_view(request):
    """The 'Heartstrings' page"""
    return render(request, 'applications/fosterinfo.html')

def foster_application_view(request):
    """The full manual save logic for Foster data + multiple images"""
    if request.method == 'POST':
        # Create the main application record manually from POST data
        app = FosterApplication.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            mobile=request.POST.get('mobile'),
            address_street=request.POST.get('address_street'),
            address_street2=request.POST.get('address_street2'),
            address_city=request.POST.get('address_city'),
            address_state=request.POST.get('address_state'),
            address_zip=request.POST.get('address_zip'),
            age=request.POST.get('age') or 18,
            
            foster_type=request.POST.get('foster_type'),
            start_date=request.POST.get('start_date'),
            work_schedule=request.POST.get('work_schedule'),
            work_other=request.POST.get('work_other'),
            alone_hours=request.POST.get('alone_hours'),
            medical_condition=request.POST.get('medical_condition'),
            residence_status=request.POST.get('residence_status'),
            residence_other=request.POST.get('residence_other'),
            rental_dogs=request.POST.get('rental_dogs') or 0,
            children_status=request.POST.get('children_status'),
            occupants_list=request.POST.get('occupants_list'),
            dog_size=request.POST.get('dog_size'),
            specific_pet=request.POST.get('specific_pet'),
            past_breeds=request.POST.get('past_breeds'),
            yard_description=request.POST.get('yard_description'),
            fence_height=request.POST.get('fence_height'),
            yard_separated=request.POST.get('yard_separated'),
            foster_inside=request.POST.get('foster_inside'),
            sleep_location=request.POST.get('sleep_location'),
            other_pets=request.POST.get('other_pets'),
            other_pets_list=request.POST.get('other_pets_list'),
            dog_sex=request.POST.get('dog_sex'),
            dog_desexed=request.POST.get('dog_desexed'),
            dog_friendly=request.POST.get('dog_friendly'),
            dog_vax=request.POST.get('dog_vax'),
            dog_personality=request.POST.get('dog_personality'),
            final_comment=request.POST.get('final_comment'),
            agreement=request.POST.get('agreement')
        )

        # Handle Multiple Yard Photos
        yard_photos = request.FILES.getlist('yard_photos')
        for f in yard_photos:
            FosterApplicationImage.objects.create(application=app, image=f, image_type='yard')

        # Handle Multiple Vaccination Photos
        vax_photos = request.FILES.getlist('vax_photos')
        for f in vax_photos:
            FosterApplicationImage.objects.create(application=app, image=f, image_type='vax')

        return redirect('applications:foster_success')

    return render(request, 'applications/foster_application.html')

# --- 5. SUCCESS VIEWS (Crucial: These fix your AttributeError crash) ---

def application_success_view(request):
    """View for Adoption Success"""
    return render(request, 'applications/application_success.html')

def foster_success_view(request):
    """View for Foster Success"""
    return render(request, 'applications/application_received.html')