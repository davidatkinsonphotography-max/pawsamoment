from django import forms
from .models import CatApplication, DogApplication, FosterApplication, ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Your Message'}),
        }


class CatAdoptionForm(forms.ModelForm):
    class Meta:
        model = CatApplication
        # We exclude fields the user shouldn't edit (like notes or processed status)
        exclude = ['processed', 'notes', 'date_submitted']
        widgets = {
            'adoption_reason': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Why do you want to adopt a cat?'}),
            'other_pets': forms.Textarea(attrs={'rows': 3}),
            'household_members': forms.Textarea(attrs={'rows': 3}),
            'rehome_other': forms.Textarea(attrs={'rows': 3}),
            'reference_details': forms.Textarea(attrs={'rows': 2}),
            'additional_info': forms.Textarea(attrs={'rows': 4}),
        }

class DogAdoptionForm(forms.ModelForm):
    class Meta:
        model = DogApplication
        exclude = ['processed', 'notes', 'date_submitted']
        widgets = {
            'breed_experience': forms.Textarea(attrs={'rows': 4}),
            'adjustment_plan': forms.Textarea(attrs={'rows': 4}),
            'rehome_history': forms.Textarea(attrs={'rows': 3}),
            'household_members': forms.Textarea(attrs={'rows': 3}),
            'other_pets_list': forms.Textarea(attrs={'rows': 3}),
            'entertainment_plan': forms.Textarea(attrs={'rows': 3}),
            'reference_details': forms.Textarea(attrs={'rows': 2}),
            'additional_info': forms.Textarea(attrs={'rows': 4}),
        }


class FosterApplicationForm(forms.ModelForm):
    class Meta:
        model = FosterApplication
        exclude = ['date_submitted', 'processed', 'notes']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 18}),
            'address_street': forms.TextInput(attrs={'class': 'form-control'}),
            'address_street2': forms.TextInput(attrs={'class': 'form-control'}),
            'address_city': forms.TextInput(attrs={'class': 'form-control'}),
            'address_state': forms.TextInput(attrs={'class': 'form-control'}),
            'address_zip': forms.TextInput(attrs={'class': 'form-control'}),
        }

