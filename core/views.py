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
            # 1. SAVE TO DATABASE (Do this first)
            application = form.save()

            # 2. EXTRACT DATA (Must happen before you use 'data')
            data = form.cleaned_data

            # 3. PREPARE EMAIL
            subject = f"Surrender Inquiry: {data['pet_name']} - {data['first_name']} {data['last_name']}"

            # Format email body
            message_lines = [f"{field.replace('_', ' ').title()}: {value}" for field, value in data.items()]
            message = "\n".join(message_lines)

            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['pawsamomentrescue@gmail.com'],
                    reply_to=[data['email']],
                    fail_silently=False,
                )
                return redirect('applications:application_success')
            except Exception as e:
                print(f"Email error: {e}")
                # Still redirect to success because the record IS saved to Admin
                return redirect('applications:application_success')
        else:
            # If form is invalid, print errors to console to see why
            print(form.errors)
    else:
        form = SurrenderForm()

    return render(request, 'core/surrender.html', {'form': form})

# Keep these helpers as they were
def contact_view(request):
    # ... your existing contact_view code ...
    pass

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
    return render(request, 'applications/application_success.html')