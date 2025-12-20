from django.contrib import admin
from django.utils.html import format_html
from .models import CatApplication, DogApplication, FosterApplication, ContactMessage, FosterApplicationImage
import csv
from django.http import HttpResponse


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}.csv'
        writer = csv.writer(response)
        
        writer.writerow(field_names)
        for obj in queryset:
            row = [getattr(obj, field) for field in field_names]
            writer.writerow(row)
        
        return response
    
    export_as_csv.short_description = "Export Selected as CSV"


@admin.register(CatApplication)
class CatApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'pet_name', 'email', 'date_submitted', 'processed')
    list_filter = ('processed', 'property_type')
    search_fields = ('first_name', 'last_name', 'email', 'pet_name')

@admin.register(DogApplication)
class DogApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'pet_name', 'yard_size', 'date_submitted', 'processed')
    list_filter = ('processed', 'yard_size')
    search_fields = ('first_name', 'last_name', 'email', 'pet_name')


class FosterApplicationImageInline(admin.TabularInline):
    model = FosterApplicationImage
    extra = 0
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 200px; max-height: 200px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"


@admin.register(FosterApplication)
class FosterApplicationAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('full_name', 'email', 'mobile', 'foster_type', 'date_submitted', 'processed')
    list_filter = ('foster_type', 'work_schedule', 'residence_status', 'date_submitted', 'processed')
    search_fields = ('first_name', 'last_name', 'email', 'mobile')
    readonly_fields = ('date_submitted',)
    inlines = [FosterApplicationImageInline]
    actions = ['export_as_csv', 'mark_processed', 'mark_unprocessed']
    
    def mark_processed(self, request, queryset):
        queryset.update(processed=True)
    mark_processed.short_description = "Mark selected as processed"
    
    def mark_unprocessed(self, request, queryset):
        queryset.update(processed=False)
    mark_unprocessed.short_description = "Mark selected as unprocessed"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'email', 'date_submitted', 'processed')
    list_filter = ('date_submitted', 'processed')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('date_submitted',)
    actions = ['export_as_csv', 'mark_processed', 'mark_unprocessed']
    
    def mark_processed(self, request, queryset):
        queryset.update(processed=True)
    mark_processed.short_description = "Mark selected as processed"
    
    def mark_unprocessed(self, request, queryset):
        queryset.update(processed=False)
    mark_unprocessed.short_description = "Mark selected as unprocessed"
