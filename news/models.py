from django.db import models
from django.utils.text import slugify


class NewsArticle(models.Model):
    CATEGORY_CHOICES = [
        ('Event', 'Event'),
        ('Success Story', 'Success Story'),
        ('Appeal', 'Appeal'),
        ('General', 'General News'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True, verbose_name="Expiry Date")
    date_entered = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-date_entered']
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while NewsArticle.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('news:news_detail', kwargs={'slug': self.slug})
    
    @property
    def is_expired(self):
        if self.expiry_date:
            from django.utils import timezone
            return timezone.now().date() > self.expiry_date
        return False
