from django.contrib import admin
from .models import AnimalProfile, AnimalImage


class AnimalImageInline(admin.TabularInline):
    model = AnimalImage
    extra = 1
    fields = ('image', 'order')


@admin.register(AnimalProfile)
class AnimalProfileAdmin(admin.ModelAdmin):
    list_display = ('animal_name', 'species', 'breed', 'status', 'archived', 'view_count', 'date_entered')
    list_filter = ('species', 'status', 'archived', 'sex', 'size', 'date_entered')
    search_fields = ('animal_name', 'breed', 'description')
    prepopulated_fields = {'slug': ('animal_name',)}
    inlines = [AnimalImageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('animal_name', 'slug', 'species', 'breed', 'sex', 'blurb', 'description')
        }),
        ('Details', {
            'fields': ('dob', 'approximate_dob', 'size', 'adoption_fee', 'status')
        }),
        ('Health & Care', {
            'fields': ('microchip_number', 'microchipped', 'vaccinated', 'desexed', 'is_wormed', 'heartworm_preventative', 'special_needs')
        }),
        ('Compatibility', {
            # Removed 'good_with_kids' from here because it was a duplicate
            'fields': ('good_with_dogs', 'good_with_cats', 'kids_under_5', 'kids_5_to_12')
        }),
        ('Location & Interstate', {
            'fields': ('location', 'interstate_adoption', 'act', 'nsw', 'vic', 'qld', 'sa', 'wa', 'tas')
        }),
        ('Media', {
            'fields': ('primary_image',)
        }),
        ('Administrative', {
            'fields': ('archived', 'view_count', 'date_entered')
        }),
    )
    readonly_fields = ('date_entered', 'view_count')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    actions = ['archive_animals', 'unarchive_animals']

    def archive_animals(self, request, queryset):
        queryset.update(archived=True)
    archive_animals.short_description = "Archive selected animals"

    def unarchive_animals(self, request, queryset):
        queryset.update(archived=False)
    unarchive_animals.short_description = "Unarchive selected animals"


@admin.register(AnimalImage)
class AnimalImageAdmin(admin.ModelAdmin):
    list_display = ('animal', 'order', 'date_added')
    list_filter = ('date_added',)
    search_fields = ('animal__animal_name',)
