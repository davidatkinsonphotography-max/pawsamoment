from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from PIL import Image, ImageOps  # Added ImageOps for rotation fix
import os

class AnimalProfile(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available Now'),
        ('SOON', 'Available Soon'),
        ('PENDING', 'Pending Adoption'),
        ('ADOPTED', 'Adopted'),
        ('NOT_AVAILABLE', 'Not Available'),
    ]

    SPECIES_CHOICES = [
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
        ('Other', 'Other'),
    ]

    SIZE_CHOICES = [
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
        ('XLarge', 'Extra Large'),
    ]

    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    animal_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, max_length=200)
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    dob = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    approximate_dob = models.BooleanField(default=False, verbose_name="Approximate DOB")
    size = models.CharField(max_length=20, choices=SIZE_CHOICES)
    adoption_fee = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    primary_image = models.ImageField(upload_to='animal_photos/', null=True, blank=True)
    description = models.TextField()
    good_with_kids = models.BooleanField(default=False)
    special_needs = models.BooleanField(default=False)
    microchipped = models.BooleanField(default=True)
    microchip_number = models.CharField(max_length=50, blank=True, null=True, help_text="Enter the 15-digit microchip number")
    vaccinated = models.BooleanField(default=True)
    desexed = models.BooleanField(default=True)
    date_entered = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    # The new Blurb
    blurb = models.CharField(max_length=200, blank=True, help_text="A short catchy line for the top of the page.")

    # Vitals Checkboxes
    is_wormed = models.BooleanField(default=True)
    heartworm_preventative = models.BooleanField(default=False, verbose_name="Heartworm Preventative Received")

    # Social Checkboxes
    good_with_cats = models.BooleanField(default=False, verbose_name="Good with other Cats")
    good_with_dogs = models.BooleanField(default=False, verbose_name="Good with other Dogs")
    kids_under_5 = models.BooleanField(default=False, verbose_name="Suitable for Kids Under 5")
    kids_5_to_12 = models.BooleanField(default=False, verbose_name="Suitable for Kids 5-12")

    # Interstate Logic
    interstate_adoption = models.BooleanField(default=False, help_text="Unchecked means NSW Only")
    act = models.BooleanField(default=False)
    nsw = models.BooleanField(default=True)
    vic = models.BooleanField(default=False)
    qld = models.BooleanField(default=False)
    sa = models.BooleanField(default=False)
    wa = models.BooleanField(default=False)
    tas = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_entered']
        verbose_name = "Animal Profile"
        verbose_name_plural = "Animal Profiles"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.animal_name)
            slug = base_slug
            counter = 1
            while AnimalProfile.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)
        if self.microchip_number and self.microchip_number.strip():
            self.microchipped = True
        super().save(*args, **kwargs)


        # Process primary image to be square if it exists
        if self.primary_image:
            try:
                self.process_image()
            except Exception:
                pass  # Don't break if image processing fails

    def process_image(self):
        """Process image to be square (1000x1000 max) and fix orientation"""
        if not self.primary_image:
            return

        try:
            img_path = self.primary_image.path
            if not os.path.exists(img_path):
                return

            img = Image.open(img_path)

            # FIX: Automatically rotate based on phone orientation sensor data
            img = ImageOps.exif_transpose(img)

            # Convert to RGB if necessary (removes transparency/alpha channels)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Resize to max 1000x1000 while maintaining aspect ratio
            img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)

            # Make square logic
            width, height = img.size
            size = max(width, height)

            # Create square image with #f5f5f5 background to match site
            square_img = Image.new('RGB', (size, size), color='#f5f5f5')

            # Paste image centered
            x_offset = (size - width) // 2
            y_offset = (size - height) // 2
            square_img.paste(img, (x_offset, y_offset))

            # Save optimized JPEG
            square_img.save(img_path, 'JPEG', quality=85, optimize=True)
        except Exception:
            pass  # Fail silently to allow save to complete

    def __str__(self):
        return f"{self.animal_name} ({self.species})"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('animals:animal_detail', kwargs={'slug': self.slug})


class AnimalImage(models.Model):
    """Gallery images for animals"""
    animal = models.ForeignKey(AnimalProfile, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='animal_photos/gallery/')
    order = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    microchip_number = models.CharField(max_length=25, blank=True, null=True)
    microchipped = models.BooleanField(default=False)


    class Meta:
        ordering = ['order', 'date_added']


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Process gallery images to be square as well
        if self.image:
            try:
                img_path = self.image.path
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    img = ImageOps.exif_transpose(img) # Fix rotation for gallery too
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
                    width, height = img.size
                    size = max(width, height)
                    square_img = Image.new('RGB', (size, size), color='#f5f5f5')
                    x_offset = (size - width) // 2
                    y_offset = (size - height) // 2
                    square_img.paste(img, (x_offset, y_offset))
                    square_img.save(img_path, 'JPEG', quality=85, optimize=True)
            except Exception:
                pass
        if self.microchip_number and self.microchip_number.strip():
            self.microchipped = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.animal.animal_name} - Image {self.order}"
