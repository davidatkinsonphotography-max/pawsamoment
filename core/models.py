from django.db import models
from django.utils import timezone


class SiteVisit(models.Model):
    """Track site visits for analytics"""
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    path = models.CharField(max_length=500)
    referer = models.CharField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Site Visit"
        verbose_name_plural = "Site Visits"
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['path']),
        ]
    
    def __str__(self):
        return f"{self.path} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class AnimalView(models.Model):
    """Track individual animal profile views"""
    animal = models.ForeignKey('animals.AnimalProfile', on_delete=models.CASCADE, related_name='views')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Animal View"
        verbose_name_plural = "Animal Views"
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['animal']),
        ]
    
    def __str__(self):
        return f"{self.animal.animal_name} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
