from django.contrib import admin
from .models import SiteVisit, AnimalView
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


@admin.register(SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('path', 'ip_address', 'timestamp')
    list_filter = ('timestamp', 'path')
    search_fields = ('path', 'ip_address')
    readonly_fields = ('ip_address', 'user_agent', 'path', 'referer', 'timestamp', 'session_id')
    actions = ['export_as_csv']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(AnimalView)
class AnimalViewAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('animal', 'ip_address', 'timestamp')
    list_filter = ('timestamp', 'animal')
    search_fields = ('animal__animal_name', 'ip_address')
    readonly_fields = ('animal', 'ip_address', 'user_agent', 'timestamp', 'session_id')
    actions = ['export_as_csv']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
