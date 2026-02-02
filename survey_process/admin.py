from django.contrib import admin
from .models import (
    Survey, PropertyOwner, PropertyAddress, PropertyDetails, 
    FloorDetails, PropertyAmenities, SurveyGeotagging, SurveyHistory
)


class PropertyOwnerInline(admin.StackedInline):
    model = PropertyOwner
    extra = 0


class PropertyAddressInline(admin.StackedInline):
    model = PropertyAddress
    extra = 0


class PropertyDetailsInline(admin.StackedInline):
    model = PropertyDetails
    extra = 0


class FloorDetailsInline(admin.TabularInline):
    model = FloorDetails
    extra = 1


class PropertyAmenitiesInline(admin.StackedInline):
    model = PropertyAmenities
    extra = 0


class SurveyGeotaggingInline(admin.StackedInline):
    model = SurveyGeotagging
    extra = 0


class SurveyHistoryInline(admin.TabularInline):
    model = SurveyHistory
    extra = 0
    readonly_fields = ['performed_at']


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['service_no', 'unique_key', 'status', 'surveyor', 'created_at', 'updated_at']
    list_filter = ['status', 'surveyor', 'created_at', 'tax_paid', 'multi_storage_complex']
    search_fields = ['service_no', 'unique_key', 'surveyor__username', 'surveyor__emp_name']
    readonly_fields = ['survey_id', 'created_at', 'updated_at']
    
    inlines = [
        PropertyOwnerInline,
        PropertyAddressInline,
        PropertyDetailsInline,
        FloorDetailsInline,
        PropertyAmenitiesInline,
        SurveyGeotaggingInline,
        SurveyHistoryInline,
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('survey_id', 'service_no', 'unique_key', 'status', 'surveyor')
        }),
        ('Tax Information', {
            'fields': ('tax_paid', 'one_time_paid', 'multi_storage_complex', 'is_ex_party')
        }),
        ('Notes', {
            'fields': ('surveyor_notes', 'verification_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PropertyOwner)
class PropertyOwnerAdmin(admin.ModelAdmin):
    list_display = ['owner_name', 'survey', 'mobile_no', 'gender', 'profession']
    list_filter = ['gender', 'profession', 'relation']
    search_fields = ['owner_name', 'guardian_name', 'mobile_no', 'survey__service_no']


@admin.register(PropertyAddress)
class PropertyAddressAdmin(admin.ModelAdmin):
    list_display = ['house_no', 'mohalla_colony_name', 'sector', 'survey']
    search_fields = ['house_no', 'mohalla_colony_name', 'building_name', 'survey__service_no']


@admin.register(PropertyDetails)
class PropertyDetailsAdmin(admin.ModelAdmin):
    list_display = ['survey', 'area_name', 'ward_no', 'ownership_type', 'use_of_property', 'no_of_floors']
    list_filter = ['area_name', 'ward_no', 'ownership_type', 'use_of_property']
    search_fields = ['survey__service_no']


@admin.register(FloorDetails)
class FloorDetailsAdmin(admin.ModelAdmin):
    list_display = ['survey', 'floor_name', 'use_type', 'usage_type', 'built_up_area_sq_ft']
    list_filter = ['floor_name', 'use_type', 'usage_type']
    search_fields = ['survey__service_no']


@admin.register(PropertyAmenities)
class PropertyAmenitiesAdmin(admin.ModelAdmin):
    list_display = ['survey', 'parking', 'electricity_connection', 'piped_water_connection']
    list_filter = ['parking', 'electricity_connection', 'piped_water_connection']
    search_fields = ['survey__service_no']


@admin.register(SurveyGeotagging)
class SurveyGeotaggingAdmin(admin.ModelAdmin):
    list_display = ['survey', 'latitude', 'longitude', 'geotagged_at', 'geotagged_by']
    readonly_fields = ['geotagged_at']
    search_fields = ['survey__service_no', 'geotagged_by__username']


@admin.register(SurveyHistory)
class SurveyHistoryAdmin(admin.ModelAdmin):
    list_display = ['survey', 'action', 'performed_by', 'performed_at']
    list_filter = ['action', 'performed_at']
    readonly_fields = ['performed_at']
    search_fields = ['survey__service_no', 'performed_by__username']