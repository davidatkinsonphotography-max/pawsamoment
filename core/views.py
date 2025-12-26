from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import SurrenderForm

# --- RESTORE MISSING CLASSES ---
class HomeView(TemplateView):
    template_name = 'core/home.html'

class DonateView(TemplateView):
    template_name = 'core/donate.html'

class GuidesView(TemplateView):
    template_name = 'core/guides.html'

def surrender_view(request):
    if request.method == 'POST':
        form = SurrenderForm(request.POST)
        if form.is_valid():
            # 1. Save to the database
            form.save()
            
            # 2. Add a success message for the user
            messages.success(request, "Application submitted successfully! We will review it in our dashboard.")
            
            # 3. Redirect to the success page
            return redirect('core:application_success')
        else:
            # If form has errors (like a missing field), it falls through to render the errors
            messages.error(request, "There were errors in your form. Please check the red fields below.")
    else:
        form = SurrenderForm()
    
    return render(request, 'core/surrender.html', {'form': form})

    return render(request, 'core/surrender.html', {'form': form})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been saved.')
            return redirect('core:contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})
    

def adoption_policy(request):
    return render(request, 'core/adoptionpolicy.html')

def terms_of_use(request):
    return render(request, 'core/termsofuse.html')

def privacy_policy(request):
    return render(request, 'core/privacypolicy.html')

def success_stories(request):
    return render(request, 'core/success_stories.html')

def about_us(request):
    return render(request, 'core/about.html')

def surrender_info(request):
    return surrender_view(request, 'core/surrender.html')

def ways_to_help(request):
    return render(request, 'core/ways_to_help.html')

def application_success_view(request):
    return render(request, 'core/application_success.html')
