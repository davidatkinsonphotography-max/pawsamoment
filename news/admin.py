from django.contrib import admin
from .models import NewsArticle
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


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('title', 'category', 'published', 'expiry_date', 'view_count', 'date_entered')
    list_filter = ('category', 'published', 'date_entered', 'expiry_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('date_entered', 'view_count')
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'category', 'content', 'image')
        }),
        ('Publishing', {
            'fields': ('published', 'expiry_date', 'date_entered', 'view_count')
        }),
    )
    actions = ['export_as_csv']
