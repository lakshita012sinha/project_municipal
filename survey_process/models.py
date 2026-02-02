from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()


class Survey(models.Model):
    """
    Main Survey model that combines form data and geotagging
    """
    SURVEY_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('form_completed', 'Form Completed'),
        ('geotagged', 'Geotagged'),
        ('completed', 'Completed'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    # Basic Survey Information
    survey_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    service_no = models.CharField(max_length=50, unique=True, verbose_name="Service Number")
    unique_key = models.CharField(max_length=100, unique=True, verbose_name="Unique Key")
    
    # Survey Status and Assignment
    status = models.CharField(max_length=20, choices=SURVEY_STATUS_CHOICES, default='draft')
    surveyor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='surveys')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Tax Information
    TAX_PAID_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('partial', 'Partial'),
    ]
    
    ONE_TIME_PAID_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    tax_paid = models.CharField(max_length=10, choices=TAX_PAID_CHOICES, blank=True)
    one_time_paid = models.CharField(max_length=10, choices=ONE_TIME_PAID_CHOICES, blank=True)
    
    # Multi Storage/Complex Information
    MULTI_STORAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    EX_PARTY_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    multi_storage_complex = models.CharField(max_length=10, choices=MULTI_STORAGE_CHOICES, blank=True)
    is_ex_party = models.CharField(max_length=10, choices=EX_PARTY_CHOICES, blank=True)
    
    # Notes and Comments
    surveyor_notes = models.TextField(blank=True, verbose_name="Surveyor Notes")
    verification_notes = models.TextField(blank=True, verbose_name="Verification Notes")
    
    def __str__(self):
        return f"Survey {self.service_no} - {self.get_status_display()}"
    
    class Meta:
        verbose_name = "Survey"
        verbose_name_plural = "Surveys"
        ordering = ['-created_at']


class PropertyOwner(models.Model):
    """
    Property Owner Details
    """
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    RELATION_CHOICES = [
        ('self', 'Self'),
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('spouse', 'Spouse'),
        ('son', 'Son'),
        ('daughter', 'Daughter'),
        ('brother', 'Brother'),
        ('sister', 'Sister'),
        ('other', 'Other'),
    ]
    
    PROFESSION_CHOICES = [
        ('business', 'Business'),
        ('service', 'Service'),
        ('agriculture', 'Agriculture'),
        ('retired', 'Retired'),
        ('housewife', 'Housewife'),
        ('student', 'Student'),
        ('unemployed', 'Unemployed'),
        ('other', 'Other'),
    ]
    
    survey = models.OneToOneField(Survey, on_delete=models.CASCADE, related_name='owner')
    
    # Owner Details
    owner_name = models.CharField(max_length=100, verbose_name="Owner Name")
    guardian_name = models.CharField(max_length=100, verbose_name="Guardian Name")
    age = models.PositiveIntegerField(verbose_name="Age")
    mobile_no = models.CharField(max_length=15, verbose_name="Mobile Number")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    profession = models.CharField(max_length=20, choices=PROFESSION_CHOICES)
    relation = models.CharField(max_length=20, choices=RELATION_CHOICES)
    
    def __str__(self):
        return f"{self.owner_name} - {self.survey.service_no}"
    
    class Meta:
        verbose_name = "Property Owner"
        verbose_name_plural = "Property Owners"


class PropertyAddress(models.Model):
    """
    Property Address Details
    """
    survey = models.OneToOneField(Survey, on_delete=models.CASCADE, related_name='address')
    
    # Address Details
    house_no = models.CharField(max_length=50, verbose_name="House Number")
    mohalla_colony_name = models.CharField(max_length=100, verbose_name="Mohalla/Colony Name")
    building_name = models.CharField(max_length=100, blank=True, verbose_name="Building Name")
    road_name = models.CharField(max_length=100, verbose_name="Road Name")
    sector = models.CharField(max_length=50, verbose_name="Sector")
    mobile_no = models.CharField(max_length=15, verbose_name="Mobile Number")
    phone_no = models.CharField(max_length=15, blank=True, verbose_name="Phone Number")
    email_id = models.EmailField(blank=True, verbose_name="Email ID")
    landmark = models.CharField(max_length=100, blank=True, verbose_name="Landmark")
    pincode = models.CharField(max_length=10, verbose_name="Pincode")
    
    # Address Types
    permanent_address = models.TextField(verbose_name="Permanent Address")
    same_as_permanent = models.BooleanField(default=False, verbose_name="Same as Permanent Address")
    communication_address = models.TextField(blank=True, verbose_name="Communication Address")
    
    def __str__(self):
        return f"{self.house_no}, {self.mohalla_colony_name} - {self.survey.service_no}"
    
    class Meta:
        verbose_name = "Property Address"
        verbose_name_plural = "Property Addresses"


class PropertyDetails(models.Model):
    """
    Property Details and Specifications
    """
    AREA_CHOICES = [
        ('area1', 'Area 1'),
        ('area2', 'Area 2'),
        ('area3', 'Area 3'),
        ('area4', 'Area 4'),
    ]
    
    WARD_CHOICES = [
        ('ward1', 'Ward 1'),
        ('ward2', 'Ward 2'),
        ('ward3', 'Ward 3'),
        ('ward4', 'Ward 4'),
    ]
    
    ROAD_TYPE_CHOICES = [
        ('paved', 'Paved Road'),
        ('unpaved', 'Unpaved Road'),
        ('concrete', 'Concrete Road'),
        ('gravel', 'Gravel Road'),
    ]
    
    OWNERSHIP_TYPE_CHOICES = [
        ('freehold', 'Freehold'),
        ('leasehold', 'Leasehold'),
        ('rental', 'Rental'),
        ('government', 'Government'),
    ]
    
    PROPERTY_USAGE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('mixed', 'Mixed Use'),
        ('institutional', 'Institutional'),
    ]
    
    survey = models.OneToOneField(Survey, on_delete=models.CASCADE, related_name='property')
    
    # Property Location
    area_name = models.CharField(max_length=20, choices=AREA_CHOICES, verbose_name="Area Name")
    ward_no = models.CharField(max_length=20, choices=WARD_CHOICES, verbose_name="Ward Number")
    road_type = models.CharField(max_length=20, choices=ROAD_TYPE_CHOICES, verbose_name="Road Type")
    ownership_type = models.CharField(max_length=20, choices=OWNERSHIP_TYPE_CHOICES, verbose_name="Ownership Type")
    use_of_property = models.CharField(max_length=20, choices=PROPERTY_USAGE_CHOICES, verbose_name="Use of Property")
    
    # Property Measurements
    plot_area_sq_yd = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Plot Area (Sq Yd)")
    plinth_area_sq_yd = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Plinth Area (Sq Yd)")
    vacant_area_sq_yd = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Vacant Area (Sq Yd)")
    no_of_floors = models.PositiveIntegerField(verbose_name="Number of Floors")
    
    def __str__(self):
        return f"Property {self.survey.service_no} - {self.area_name}"
    
    class Meta:
        verbose_name = "Property Details"
        verbose_name_plural = "Property Details"


class FloorDetails(models.Model):
    """
    Individual Floor Details
    """
    FLOOR_CHOICES = [
        ('ground', 'Ground Floor'),
        ('first', 'First Floor'),
        ('second', 'Second Floor'),
        ('third', 'Third Floor'),
        ('fourth', 'Fourth Floor'),
        ('basement', 'Basement'),
    ]
    
    USE_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('office', 'Office'),
        ('shop', 'Shop'),
        ('godown', 'Godown'),
        ('parking', 'Parking'),
    ]
    
    USAGE_TYPE_CHOICES = [
        ('self_occupied', 'Self Occupied'),
        ('rented', 'Rented'),
        ('vacant', 'Vacant'),
        ('under_construction', 'Under Construction'),
    ]
    
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='floors')
    
    # Floor Information
    floor_name = models.CharField(max_length=20, choices=FLOOR_CHOICES, verbose_name="Floor Name")
    use_type = models.CharField(max_length=20, choices=USE_TYPE_CHOICES, verbose_name="Use Type")
    usage_type = models.CharField(max_length=20, choices=USAGE_TYPE_CHOICES, verbose_name="Usage Type")
    from_year = models.PositiveIntegerField(verbose_name="From Year")
    upto_year = models.PositiveIntegerField(blank=True, null=True, verbose_name="Upto Year")
    built_up_area_sq_ft = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Built Up Area (Sq Ft)")
    
    def __str__(self):
        return f"{self.get_floor_name_display()} - {self.survey.service_no}"
    
    class Meta:
        verbose_name = "Floor Details"
        verbose_name_plural = "Floor Details"
        unique_together = ['survey', 'floor_name']


class PropertyAmenities(models.Model):
    """
    Property Amenities and Infrastructure
    """
    AMENITY_CHOICES = [
        ('available', 'Available'),
        ('not_available', 'Not Available'),
        ('partial', 'Partial'),
    ]
    
    survey = models.OneToOneField(Survey, on_delete=models.CASCADE, related_name='amenities')
    
    # Infrastructure Amenities
    parking = models.CharField(max_length=15, choices=AMENITY_CHOICES, default='not_available')
    street_light = models.CharField(max_length=15, choices=AMENITY_CHOICES, default='not_available')
    sewer_line = models.CharField(max_length=15, choices=AMENITY_CHOICES, default='not_available')
    electricity_connection = models.CharField(max_length=15, choices=AMENITY_CHOICES, default='not_available')
    private_toilet = models.CharField(max_length=15, choices=AMENITY_CHOICES, default='not_available')
    sewer_connection = models.CharField(max_length=15, choices=AMENITY_CHOICES, default='not_available')
    septic_tank = models.CharField(max_length=15, choices=AMENITY_CHOICES, default='not_available')
    open_toilet = models.CharField(max_length=15, choices=AMENITY_CHOICES, default='not_available')
    piped_water_connection = models.CharField(max_length=15, choices=AMENITY_CHOICES, default='not_available')
    fire_fighting_system = models.CharField(max_length=15, choices=AMENITY_CHOICES, default='not_available')
    boring = models.CharField(max_length=15, choices=AMENITY_CHOICES, default='not_available')
    mobile_tower = models.CharField(max_length=15, choices=AMENITY_CHOICES, default='not_available')
    advertising_hoarding = models.CharField(max_length=15, choices=AMENITY_CHOICES, default='not_available')
    
    def __str__(self):
        return f"Amenities - {self.survey.service_no}"
    
    class Meta:
        verbose_name = "Property Amenities"
        verbose_name_plural = "Property Amenities"


class SurveyGeotagging(models.Model):
    """
    Geotagging information for the survey
    """
    survey = models.OneToOneField(Survey, on_delete=models.CASCADE, related_name='geotagging')
    
    # Location Coordinates
    latitude = models.DecimalField(max_digits=10, decimal_places=8, verbose_name="Latitude")
    longitude = models.DecimalField(max_digits=11, decimal_places=8, verbose_name="Longitude")
    accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="GPS Accuracy (meters)")
    
    # Photos
    front_photo = models.ImageField(upload_to='survey_photos/front/', verbose_name="Front Photo")
    side_photo_1 = models.ImageField(upload_to='survey_photos/side/', verbose_name="Side Photo 1")
    side_photo_2 = models.ImageField(upload_to='survey_photos/side/', verbose_name="Side Photo 2")
    
    # Geotagging Metadata
    geotagged_at = models.DateTimeField(auto_now_add=True)
    geotagged_by = models.ForeignKey(User, on_delete=models.CASCADE)
    device_info = models.CharField(max_length=200, blank=True, verbose_name="Device Information")
    
    def __str__(self):
        return f"Geotagging - {self.survey.service_no}"
    
    class Meta:
        verbose_name = "Survey Geotagging"
        verbose_name_plural = "Survey Geotagging"


class SurveyHistory(models.Model):
    """
    Track survey status changes and history
    """
    ACTION_CHOICES = [
        ('created', 'Survey Created'),
        ('form_filled', 'Form Filled'),
        ('geotagged', 'Geotagged'),
        ('completed', 'Completed'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('updated', 'Updated'),
    ]
    
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    performed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    performed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.get_action_display()} - {self.survey.service_no}"
    
    class Meta:
        verbose_name = "Survey History"
        verbose_name_plural = "Survey History"
        ordering = ['-performed_at']