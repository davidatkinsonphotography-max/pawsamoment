from django.db import models
from django.core.validators import MinValueValidator
import json


class BaseApplication(models.Model):
    """Shared fields for adoption and foster applications"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=20)
    address_street = models.CharField(max_length=200)
    address_street2 = models.CharField(max_length=200, blank=True)
    address_city = models.CharField(max_length=100)
    address_state = models.CharField(max_length=50)
    address_zip = models.CharField(max_length=20)
    age = models.IntegerField(validators=[MinValueValidator(18)])
    date_submitted = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        abstract = True

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_address(self):
        addr = self.address_street
        if self.address_street2:
            addr += f", {self.address_street2}"
        addr += f", {self.address_city}, {self.address_state} {self.address_zip}"
        return addr


class CatApplication(BaseApplication):
    """Specific questionnaire for Cat Adoptions"""
    # Interest & Details
    age_confirm = models.CharField(max_length=10, blank=True, verbose_name="18 years or older?")
    pet_name = models.CharField(max_length=100, verbose_name="Cat/Kitten Name")
    coat_pref = models.CharField(max_length=100, blank=True)
    coat_other = models.CharField(max_length=200, blank=True)

    # Contact (home_phone added to BaseApplication fields)
    home_phone = models.CharField(max_length=20, blank=True)

    # Home & Family
    household_members = models.TextField(blank=True, verbose_name="Names and ages of household members")
    home_status = models.CharField(max_length=200, verbose_name="Rent or Own")
    home_other = models.CharField(max_length=200, blank=True)
    property_type = models.CharField(max_length=100)
    property_other = models.CharField(max_length=200, blank=True)
    residence_length = models.CharField(max_length=50, blank=True, verbose_name="How long lived in current home")
    provide_pictures = models.CharField(max_length=10, blank=True, verbose_name="Happy to provide pictures")
    other_pets = models.TextField(blank=True, verbose_name="Details of current pets")
    other_animals_desexed = models.CharField(max_length=20, blank=True)
    confinement = models.CharField(max_length=255, verbose_name="Where will cat be kept?")
    confinement_other = models.CharField(max_length=200, blank=True)
    food_plan = models.CharField(max_length=200, blank=True, verbose_name="Food plan")

    # Lifestyle & Work
    work_status = models.CharField(max_length=100, blank=True)
    work_other = models.CharField(max_length=200, blank=True)
    employment_length = models.CharField(max_length=50, blank=True)
    adoption_reason = models.TextField(blank=True)
    reason_other = models.CharField(max_length=200, blank=True)
    allow_inside = models.CharField(max_length=50, blank=True)
    allergies = models.CharField(max_length=20, blank=True)
    main_caregiver = models.CharField(max_length=200, blank=True)
    introducing_to_existing = models.CharField(max_length=200, blank=True)
    vet_care_importance = models.CharField(max_length=20, blank=True)
    children_education = models.CharField(max_length=100, blank=True)

    # Commitment
    rehomed_before = models.CharField(max_length=100, blank=True)
    rehome_other = models.TextField(blank=True)
    household_agreement = models.CharField(max_length=200, blank=True)
    heard_about = models.CharField(max_length=100, blank=True)
    heard_other = models.CharField(max_length=200, blank=True)
    considered_fostering = models.CharField(max_length=200, blank=True)
    reference_details = models.TextField(blank=True)
    readiness = models.CharField(max_length=50, blank=True)
    readiness_other = models.CharField(max_length=200, blank=True)
    additional_info = models.TextField(blank=True)

    class Meta:
        verbose_name = "Cat Adoption Application"
        verbose_name_plural = "Cat Adoption Applications"
        ordering = ['-date_submitted']

    def __str__(self):
        return f"Cat: {self.full_name} - {self.pet_name}"


class DogApplication(BaseApplication):
    """Specific questionnaire for Dog Adoptions"""
    # Interest & Experience
    age_confirm = models.CharField(max_length=10, blank=True, verbose_name="18 years or older?")
    pet_name = models.CharField(max_length=100, verbose_name="Dog/Puppy Name")
    dog_size_pref = models.CharField(max_length=100, verbose_name="Preferred Adult Size")
    size_other = models.CharField(max_length=200, blank=True)
    breed_experience = models.TextField(verbose_name="Experience with this breed")

    # Contact (home_phone added to BaseApplication fields)
    home_phone = models.CharField(max_length=20, blank=True)

    # Home & Family
    household_members = models.TextField(blank=True, verbose_name="Names and ages of household members")
    home_status = models.CharField(max_length=200, verbose_name="Rent or Own")
    home_other = models.CharField(max_length=200, blank=True)
    property_type = models.CharField(max_length=100)
    property_other = models.CharField(max_length=200, blank=True)
    residence_length = models.CharField(max_length=50, blank=True, verbose_name="How long lived in current home")

    # Yard & Fencing
    yard_size = models.CharField(max_length=100)
    yard_other = models.CharField(max_length=200, blank=True)
    fencing_secure = models.CharField(max_length=20, verbose_name="Fully fenced and secure?")
    fencing_other = models.CharField(max_length=200, blank=True)
    fence_details = models.CharField(max_length=255, verbose_name="Fence height/material")
    home_check_ok = models.CharField(max_length=10, blank=True, verbose_name="Happy for home check?")
    other_pets_list = models.TextField(blank=True, verbose_name="Other pets list")
    other_animals_desexed = models.CharField(max_length=20, blank=True)

    # Lifestyle & Work
    work_status = models.CharField(max_length=100)
    work_other = models.CharField(max_length=200, blank=True)
    employment_length = models.CharField(max_length=50, blank=True)
    work_location = models.CharField(max_length=200, blank=True, verbose_name="Where dog while at work")
    hours_alone = models.CharField(max_length=100)
    adoption_reason = models.CharField(max_length=200, blank=True)
    reason_other = models.CharField(max_length=200, blank=True)
    allergies = models.CharField(max_length=20, blank=True)
    inside_outside = models.CharField(max_length=100, blank=True)
    personality_type = models.CharField(max_length=50, blank=True, verbose_name="Indoors/outdoors person")
    main_caregiver = models.CharField(max_length=200, blank=True)
    food_plan = models.CharField(max_length=200, blank=True)
    food_other = models.CharField(max_length=200, blank=True)
    training_plan = models.CharField(max_length=200)
    training_other = models.CharField(max_length=200, blank=True)
    walking_frequency = models.CharField(max_length=100, blank=True)
    daily_time = models.CharField(max_length=100, blank=True, verbose_name="Daily time with dog")
    command_experience = models.CharField(max_length=200, blank=True)
    sleeping_location = models.CharField(max_length=255)
    toilet_training_experience = models.CharField(max_length=20, blank=True)
    entertainment_plan = models.TextField(blank=True)
    adjustment_plan = models.TextField(blank=True, verbose_name="Plan for adjustment period")
    vet_care_importance = models.CharField(max_length=20, blank=True)
    children_education = models.CharField(max_length=100, blank=True)

    # Commitment
    rehomed_before = models.CharField(max_length=100, blank=True)
    rehome_history = models.TextField(blank=True, verbose_name="Previous rehoming history")
    household_agreement = models.CharField(max_length=200, blank=True)
    heard_about = models.CharField(max_length=100, blank=True)
    heard_other = models.CharField(max_length=200, blank=True)
    considered_fostering = models.CharField(max_length=200, blank=True)
    reference_details = models.TextField(blank=True)
    readiness = models.CharField(max_length=50, blank=True)
    readiness_other = models.CharField(max_length=200, blank=True)
    additional_info = models.TextField(blank=True)

    class Meta:
        verbose_name = "Dog Adoption Application"
        verbose_name_plural = "Dog Adoption Applications"
        ordering = ['-date_submitted']

    def __str__(self):
        return f"Dog: {self.full_name} - {self.pet_name}"


class FosterApplication(BaseApplication):
    # 2. Fostering Requirements & Availability
    foster_type = models.CharField(max_length=50, blank=True)
    start_date = models.CharField(max_length=200, blank=True)
    work_schedule = models.CharField(max_length=100)
    work_other = models.CharField(max_length=200, blank=True) # For the "Other" JS trigger
    alone_hours = models.CharField(max_length=200, blank=True)
    medical_condition = models.CharField(max_length=10) # "Yes" or "No"
    residence_status = models.CharField(max_length=50)
    residence_other = models.CharField(max_length=200, blank=True) # For the "Other" JS trigger
    rental_dogs = models.IntegerField(null=True, blank=True)
    children_status = models.CharField(max_length=50) # "Yes", "No", "Visit"
    occupants_list = models.TextField()

    # 3. Pet Preferences & Home Security
    dog_size = models.CharField(max_length=50, blank=True)
    specific_pet = models.CharField(max_length=200, blank=True)
    past_breeds = models.CharField(max_length=200, blank=True)
    yard_description = models.TextField()
    fence_height = models.CharField(max_length=200)
    yard_separated = models.TextField()
    foster_inside = models.CharField(max_length=50)
    sleep_location = models.CharField(max_length=200)

    # 4. Existing Pets
    other_pets = models.CharField(max_length=10) # "Yes" or "No"
    other_pets_list = models.TextField(blank=True)
    dog_sex = models.CharField(max_length=50, blank=True)
    dog_desexed = models.CharField(max_length=50, blank=True)
    dog_friendly = models.CharField(max_length=50, blank=True)
    dog_vax = models.CharField(max_length=50, blank=True)
    dog_personality = models.TextField(blank=True)

    # 5. Final Commitment
    final_comment = models.TextField(blank=True)
    agreement = models.CharField(max_length=10) # "Yes"

    class Meta:
        verbose_name = "Foster Application"
        verbose_name_plural = "Foster Applications"
        ordering = ['-date_submitted']

    def __str__(self):
        return f"Foster App: {self.full_name}"

class FosterApplicationImage(models.Model):
    """Storage for multiple photos uploaded per foster application"""
    application = models.ForeignKey(FosterApplication, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='foster_uploads/%Y/%m/')
    image_type = models.CharField(max_length=20, choices=[('yard', 'Yard'), ('vax', 'Vaccination')])

    def __str__(self):
        return f"{self.image_type} photo for {self.application.full_name}"


class ContactMessage(models.Model):
    """Contact form messages"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-date_submitted']

    def __str__(self):
        return f"Contact from {self.name} - {self.date_submitted.strftime('%Y-%m-%d')}"

class SurrenderApplication(BaseApplication):
    age = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(18)])
    """Specific questionnaire for Rehoming/Surrender Inquiries"""
    # 1. The Basics (first_name, last_name, email, age are in BaseApplication)
    pet_name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    # Matching the Animal Listing logic exactly
    dob = models.DateField(null=True, blank=True, verbose_name="Animal Date of Birth")
    approximate_dob = models.BooleanField(default=False)

    # 2. Health & Ownership
    legal_owner = models.CharField(max_length=50)
    legal_owner_details = models.TextField(blank=True)
    microchip_number = models.CharField(max_length=50)
    last_vaccination = models.CharField(max_length=100)
    desexed = models.CharField(max_length=20)
    is_wormed = models.BooleanField(default=True)
    heartworm_preventative = models.BooleanField(default=False)

    # 3. Compatibility
    living_with_dogs = models.CharField(max_length=20)
    dog_sizes_exposed = models.CharField(max_length=100)
    dog_friendly = models.CharField(max_length=100)
    cat_friendly = models.CharField(max_length=100)
    living_with_children = models.CharField(max_length=20)
    child_ages = models.CharField(max_length=100, blank=True)

    # 4. Behavior & Lifestyle
    living_arrangements = models.TextField()
    toilet_trained = models.CharField(max_length=50)
    behavioral_issues = models.TextField()
    food_aggression = models.CharField(max_length=100)
    fear_triggers = models.TextField()
    commands = models.TextField()
    meeting_strangers = models.TextField()
    travel_well = models.CharField(max_length=100)
    walks_well = models.CharField(max_length=100)

    # 5. Environment & Diet
    yard_type = models.CharField(max_length=100)
    fencing_details = models.TextField()
    current_diet = models.CharField(max_length=255)
    diet_other_details = models.TextField(blank=True)

    # 6. Personal Details (address/phone in BaseApplication)
    contact_name = models.CharField(max_length=200) # Full name of person filling form
    phone = models.CharField(max_length=20)
    reason = models.TextField()
    time_in_care = models.CharField(max_length=100)
    urgency = models.CharField(max_length=100)
    urgency_other_details = models.TextField(blank=True)
    preference = models.TextField(verbose_name="Preference for new home")
    blurb = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Surrender Application"
        verbose_name_plural = "Surrender Applications"
        ordering = ['-date_submitted']

    def __str__(self):
        return f"Surrender: {self.pet_name} ({self.contact_name})"
