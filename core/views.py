from django.shortcuts import render
from django.views.generic import TemplateView
from applications.forms import ContactForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


class HomeView(TemplateView):
    template_name = 'core/home.html'


class DonateView(TemplateView):
    template_name = 'core/donate.html'


class GuidesView(TemplateView):
    template_name = 'core/guides.html'


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Send email to admin
            try:
                send_mail(
                    subject=f'Contact Form: {contact.name}',
                    message=f'Name: {contact.name}\nEmail: {contact.email}\n\nMessage:\n{contact.message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Thank you for your message! We will get back to you soon.')
            except Exception as e:
                messages.error(request, 'There was an error sending your message. Please try again later.')
            
            return render(request, 'core/contact.html', {'form': ContactForm()})
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
    return render(request, 'core/surrender.html')

def ways_to_help(request):
    return render(request, 'core/ways_to_help.html')