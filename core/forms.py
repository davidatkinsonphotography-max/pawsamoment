from django import forms
from django.core.validators import RegexValidator
from applications.models import SurrenderApplication

class SurrenderForm(forms.ModelForm):
    # 1. Validators
    micro_val = RegexValidator(r'^\d{15}$', "Microchip must be 15 digits.")
    phone_val = RegexValidator(r'^\d{1,10}$', "Phone number must be up to 10 digits.")

    # Mapping the specific names Django expects from BaseApplication
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(attrs={'autocomplete': 'given-name'}))
    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(attrs={'autocomplete': 'family-name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autocomplete': 'email'}))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'tel'}))

    # --- Pet Basics ---
    pet_name = forms.CharField(label="Pet Name", max_length=100)
    breed = forms.CharField(label="Breed", max_length=100)
    size = forms.ChoiceField(label="Size", choices=[('Small','Small'),('Medium','Medium'),('Large','Large'),('XL','Extra Large')], widget=forms.RadioSelect)
    
    # Pet DOB
    dob = forms.DateField(
        label="Pet's Date of Birth",
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    approximate_dob = forms.BooleanField(label="Approximate?", required=False)

    # --- Health & Ownership ---
    legal_owner = forms.ChoiceField(label="Are you the legal owner?", choices=[('Yes','Yes'),('No','No'),('Other','Other')], widget=forms.RadioSelect)
    legal_owner_details = forms.CharField(label="Please provide details regarding ownership", widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Please explain...'}), required=False)
    microchip_number = forms.CharField(label="Microchip Number", validators=[micro_val])
    last_vaccination = forms.DateField(label="Date of last Vaccination", widget=forms.DateInput(attrs={'type': 'date'}))
    desexed = forms.ChoiceField(label="Desexed?", choices=[('Yes','Yes'),('No','No'),('Unsure','Unsure')], widget=forms.RadioSelect)

    # --- Compatibility ---
    living_with_dogs = forms.ChoiceField(label="Currently living with other dogs?", choices=[('Yes','Yes'),('No','No'),('Other','Other')], widget=forms.RadioSelect)
    dog_sizes_exposed = forms.MultipleChoiceField(choices=[('Small','Small'),('Medium','Medium'),('Large','Large'),('XL','Extra Large'),('None','None')], widget=forms.CheckboxSelectMultiple)
    dog_friendly = forms.MultipleChoiceField(choices=[('Great','Great with all'),('Small','Small only'),('Medium','Medium only'),('Large','Large only'),('Males','Males only'),('Females','Females only'),('Unsure','Unsure')], widget=forms.CheckboxSelectMultiple)
    cat_friendly = forms.ChoiceField(label="Is he/she Cat friendly?", choices=[('Yes','Yes'),('No','No'),('Unsure','Unsure')], widget=forms.RadioSelect)
    living_with_children = forms.ChoiceField(label="Living with Children?", choices=[('Yes','Yes'),('No','No')], widget=forms.RadioSelect)
    child_ages = forms.MultipleChoiceField(choices=[('Under 5','Under 5 years'),('6-12','6-12 years'),('13+','13 years +')], widget=forms.CheckboxSelectMultiple, required=False)

    # --- Behavior & Lifestyle ---
    living_arrangements = forms.MultipleChoiceField(choices=[('Outside','Outside only'),('Both','Inside/Outside'),('Inside','Sleeps indoors'),('SleepsOut','Sleeps outside')], widget=forms.CheckboxSelectMultiple)
    toilet_trained = forms.ChoiceField(label="Toilet Trained?", choices=[('Yes','Yes'),('No','No'),('Unsure','Unsure')], widget=forms.RadioSelect)
    behavioral_issues = forms.MultipleChoiceField(choices=[('Barking','Nuisance barking'),('Jumper','Fence jumper'),('Digging','Digging'),('Escape','Escape artist'),('Washing','Pulls washing off line'),('Chewing','Chewing'),('None','None')], widget=forms.CheckboxSelectMultiple)
    food_aggression = forms.ChoiceField(label="Any food aggression?", choices=[('Yes','Yes'),('No','No'),('Unsure','Unsure')], widget=forms.RadioSelect)
    fear_triggers = forms.MultipleChoiceField(choices=[('Mower','Lawn Mower'),('Vacuum','Vacuum'),('Brooms','Brooms'),('None','None')], widget=forms.CheckboxSelectMultiple)
    commands = forms.MultipleChoiceField(choices=[('Recall','Recall'),('Sit','Sit'),('Stay','Stay'),('Drop','Drop'),('Come','Come'),('Shake','Shake hands')], widget=forms.CheckboxSelectMultiple)
    meeting_strangers = forms.MultipleChoiceField(choices=[('Friendly','Tail wag'),('Nervous','Nervous'),('Hiding','Will hide'),('Barking','Will bark')], widget=forms.CheckboxSelectMultiple)
    travel_well = forms.ChoiceField(label="Travels well in car?", choices=[('Yes','Yes'),('No','No'),('Unsure','Unsure')], widget=forms.RadioSelect)
    walks_well = forms.ChoiceField(label="Walks well on lead?", choices=[('Yes','Yes'),('No','No'),('Unsure','Unsure')], widget=forms.RadioSelect)

    # --- Environment & Diet ---
    yard_type = forms.ChoiceField(label="Current yard type", choices=[('Courtyard','Courtyard'),('Average','Average yard'),('Large','Large yard'),('Farm','Acreage/Farm')], widget=forms.RadioSelect)
    fencing_details = forms.CharField(label="Fencing Description", widget=forms.Textarea(attrs={'rows': 3}))
    current_diet = forms.MultipleChoiceField(choices=[('Supermarket','Supermarket Dry'),('Premium','Premium Dry'),('Raw','Raw'),('Tinned','Tinned'),('Scraps','Table scraps'),('Other','Other')], widget=forms.CheckboxSelectMultiple)
    diet_other_details = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Please specify diet...'}))

    # --- Personal Details ---
    # --- Address (Matching BaseApplication field names) ---
    address_street = forms.CharField(label="Street Address", widget=forms.TextInput(attrs={'placeholder': 'Street Address'}))
    address_city = forms.CharField(label="Suburb", widget=forms.TextInput(attrs={'placeholder': 'Suburb'}))
    address_state = forms.ChoiceField(label="State", choices=[('NSW','NSW'),('ACT','ACT'),('QLD','QLD'),('VIC','VIC'),('SA','SA'),('TAS','TAS'),('WA','WA'),('NT','NT')])
    address_zip = forms.CharField(label="Postcode", widget=forms.TextInput(attrs={'placeholder': 'Postcode'}))
    phone = forms.CharField(label="Primary Contact Number", validators=[phone_val])
    reason = forms.CharField(label="Reason for Rehoming", widget=forms.Textarea(attrs={'rows': 3}))
    time_in_care = forms.ChoiceField(label="How long in your care?", choices=[('6m','< 6 months'),('2y','< 2 years'),('3y','3 years +')], widget=forms.RadioSelect)
    urgency = forms.ChoiceField(choices=[('ASAP','ASAP'),('2w','2 weeks'),('1m','1 month'),('Other','Other')], widget=forms.RadioSelect)
    urgency_other_details = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Please specify timing...'}))
    preference = forms.ChoiceField(label="Which would you prefer?", choices=[('Surrender','Surrender to Rescue'),('Assisted','Assisted Rehome')], widget=forms.RadioSelect)

    class Meta:
        model = SurrenderApplication
        # We hide 'age' (human) and admin fields from the user
        exclude = ['age', 'processed', 'notes', 'date_submitted', 'address_street2', 'is_wormed', 'heartworm_preventative', 'blurb']

    def clean(self):
        """Custom cleaning to convert lists from CheckboxSelectMultiple into strings for the model"""
        cleaned_data = super().clean()
        for field, value in cleaned_data.items():
            if isinstance(value, list):
                # Joins list items with a comma so they fit in CharField/TextField
                cleaned_data[field] = ", ".join(value)
        return cleaned_data