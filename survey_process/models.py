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
    survey_number = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="Survey Number")
    service_no = models.CharField(max_length=50, blank=True, null=True, verbose_name="Service Number")
    unique_key = models.CharField(max_length=100, blank=True, null=True, verbose_name="Unique Key")
    
    # Survey Status and Assignment
    status = models.CharField(max_length=20, choices=SURVEY_STATUS_CHOICES, default='draft')
    surveyor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='surveys')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Tax Information
    TAX_PAID_CHOICES = [
        ('', 'Select Tax Status'),
        ('yes', 'Yes'),
        ('no', 'No'),
        ('partial', 'Partial'),
    ]
    
    ONE_TIME_PAID_CHOICES = [
        ('', 'Select One Time Payment'),
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    tax_paid = models.CharField(max_length=10, choices=TAX_PAID_CHOICES, blank=True)
    one_time_paid = models.CharField(max_length=10, choices=ONE_TIME_PAID_CHOICES, blank=True)
    
    # Multi Storage/Complex Information
    MULTI_STORAGE_CHOICES = [
        ('', 'Select Multi Storage'),
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    EX_PARTY_CHOICES = [
        ('', 'Select Ex Party'),
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    multi_storage_complex = models.CharField(max_length=10, choices=MULTI_STORAGE_CHOICES, blank=True)
    is_ex_party = models.CharField(max_length=10, choices=EX_PARTY_CHOICES, blank=True)
    
    # Notes and Comments
    surveyor_notes = models.TextField(blank=True, verbose_name="Surveyor Notes")
    verification_notes = models.TextField(blank=True, verbose_name="Verification Notes")
    
    def generate_survey_number(self):
        """
        Generate unique survey number in format: SRV2/129/59335
        Format: SRV2/{ward_no}/{sequential_number}
        """
        # Get ward number from property details if available
        ward_no = "001"  # Default ward
        try:
            if hasattr(self, 'property') and self.property:
                # Extract numeric part from ward choice
                ward_choice = self.property.ward_no
                if ward_choice:
                    # Map ward choices to numbers (you can customize this mapping)
                    ward_mapping = {
                        'ward1': '001',
                        'ward2': '002', 
                        'ward3': '003',
                        'ward4': '004',
                    }
                    ward_no = ward_mapping.get(ward_choice, '001')
        except:
            pass
        
        # Get the next sequential number for this ward
        from django.db.models import Max
        import re
        
        # Find the highest sequential number for this ward
        existing_surveys = Survey.objects.filter(
            survey_number__startswith=f'SRV2/{ward_no}/'
        ).exclude(id=self.id if self.id else None)
        
        max_seq = 0
        for survey in existing_surveys:
            if survey.survey_number:
                # Extract the sequential number from format SRV2/ward/seq
                match = re.search(r'SRV2/\d+/(\d+)', survey.survey_number)
                if match:
                    seq_num = int(match.group(1))
                    max_seq = max(max_seq, seq_num)
        
        # Generate new sequential number
        new_seq = max_seq + 1
        
        # Format: SRV2/ward/sequential (5 digits)
        return f"SRV2/{ward_no}/{new_seq:05d}"
    
    def save(self, *args, **kwargs):
        """
        Override save to auto-generate survey number when survey is completed
        """
        # Generate survey number when status changes to form_completed or completed
        if (self.status in ['form_completed', 'completed'] and not self.survey_number):
            self.survey_number = self.generate_survey_number()
        
        # Set completed_at timestamp when status becomes completed
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        if self.survey_number:
            return f"Survey {self.survey_number} - {self.get_status_display()}"
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
        ('', 'Select Gender'),
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    RELATION_CHOICES = [
        ('', 'Select Relation'),
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
        ('', 'Select Profession'),
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
        ('', 'Select Area'),
        ('area1', 'Area 1'),
        ('area2', 'Area 2'),
        ('area3', 'Area 3'),
        ('area4', 'Area 4'),
    ]
    
    WARD_CHOICES = [
        ('', 'Select Ward'),
        ('ward1', 'Ward 1'),
        ('ward2', 'Ward 2'),
        ('ward3', 'Ward 3'),
        ('ward4', 'Ward 4'),
    ]
    
    ROAD_TYPE_CHOICES = [
        ('', 'Select Road Type'),
        ('interior', 'Interior'),
        ('exterior', 'Exterior'),
    ]
    
    OWNERSHIP_TYPE_CHOICES = [
        ('', 'Select Ownership Type'),
        ('allotment_land_house', 'Allotment Land/House'),
        ('ancestral', 'Ancestral'),
        ('possession', 'Possession'),
    ]
    
    PROPERTY_USAGE_CHOICES = [
        ('', 'Select Use of Property'),
        ('residential_individual_house', 'Residential - Individual House'),
        ('residential_apartment', 'Residential - Apartment'),
        ('residential_cum_commercial', 'Residential cum Commercial'),
        ('school', 'School'),
        ('professional_college', 'Professional College'),
        ('general_degree_college', 'General Degree College'),
        ('coaching_institute', 'Coaching Institute'),
        ('private_hospital_clinic', 'Private Hospital/Clinic'),
        ('beauty_parlor', 'Beauty Parlor'),
        ('cinema_hall_multiplex', 'Cinema Hall/Multiplex'),
        ('marriage_garden_hall', 'Marriage Garden/Hall'),
        ('hotel_restaurant', 'Hotel/Restaurant'),
        ('private_office', 'Private Office'),
        ('semi_govt_institute', 'Semi Govt. Institute'),
        ('central_govt_property_office', 'Central Govt. Property Office'),
        ('state_govt_autonomous_board', 'State Govt. Autonomous Board'),
        ('state_govt_company', 'State Govt. Company'),
        ('corporation', 'Corporation'),
        ('completely_religious_property', 'Completely Religious Property'),
        ('situated_in_riico_area', 'Situated in RIICO Area'),
        ('out_of_riico_industries', 'Out of RIICO Industries'),
        ('exempted_under_clause_107', 'Exempted Under clause 107 of RM Act 2009'),
        ('dharmshala_community_society', 'Dharmshala of Community society'),
        ('temple', 'Temple'),
        ('mosque', 'Mosque'),
        ('gurudwara', 'Gurudwara'),
        ('others', 'Others'),
    ]
    
    survey = models.OneToOneField(Survey, on_delete=models.CASCADE, related_name='property')
    
    # Property Location
    area_name = models.CharField(max_length=20, choices=AREA_CHOICES, verbose_name="Area Name")
    ward_no = models.CharField(max_length=20, choices=WARD_CHOICES, verbose_name="Ward Number")
    road_type = models.CharField(max_length=50, choices=ROAD_TYPE_CHOICES, verbose_name="Road Type")
    ownership_type = models.CharField(max_length=50, choices=OWNERSHIP_TYPE_CHOICES, verbose_name="Ownership Type")
    use_of_property = models.CharField(max_length=100, choices=PROPERTY_USAGE_CHOICES, verbose_name="Use of Property")
    
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
        ('', 'Select Floor'),
        ('basement', 'Basement'),
        ('ground', 'Ground Floor'),
        ('1st', '1st Floor'),
        ('2nd', '2nd Floor'),
        ('3rd', '3rd Floor'),
        ('4th', '4th Floor'),
        ('5th', '5th Floor'),
        ('6th', '6th Floor'),
        ('7th', '7th Floor'),
        ('8th', '8th Floor'),
        ('9th', '9th Floor'),
        ('10th', '10th Floor'),
        ('11th', '11th Floor'),
        ('12th', '12th Floor'),
        ('13th', '13th Floor'),
        ('14th', '14th Floor'),
        ('15th', '15th Floor'),
        ('16th', '16th Floor'),
        ('17th', '17th Floor'),
        ('18th', '18th Floor'),
        ('19th', '19th Floor'),
        ('20th', '20th Floor'),
        ('21st', '21st Floor'),
        ('22nd', '22nd Floor'),
        ('23rd', '23rd Floor'),
        ('24th', '24th Floor'),
        ('25th', '25th Floor'),
        ('vacant_land', 'Vacant Land'),
        ('basement_2', 'Basement 2'),
        ('basement_3', 'Basement 3'),
        ('lower_ground', 'Lower Ground'),
    ]
    
    USE_TYPE_CHOICES = [
        ('', 'Select Use Type'),
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('institution', 'INSTITUTION'),
    ]
    
    USAGE_TYPE_CHOICES = [
        ('', 'Select'),
        ('4_5_star_hotel', '4/5 Star Hotel'),
        ('agri_dept', 'Agri.Dept.'),
        ('airport', 'AirPort'),
        ('bank', 'Bank'),
        ('beauty_parlour', 'Beauty Parlour'),
        ('bhandar_nigam', 'Bhandar Nigam'),
        ('bsnl', 'Bsnl'),
        ('central_govt_oth_nigams', 'Central Govt.(oth.nigams)'),
        ('central_govt_building', 'Central Govt.Building'),
        ('cinema_multiplex', 'Cinema(Multiplex)'),
        ('clubs', 'Clubs'),
        ('corporate_building', 'Corporate Building'),
        ('coaching_inst', 'Coaching Inst.'),
        ('comm_center', 'Comm.Center'),
        ('jda', 'JDA'),
        ('dharamsala_sarai_musafirkhana', 'Dharamsala/Sarai/Musafirkhana'),
        ('ex_army_service', 'Ex-Army Service'),
        ('fci', 'F.C.I'),
        ('ex_army_fighter', 'Ex-Army Fighter'),
        ('govt_hospital', 'Govt. Hospital'),
        ('govt_school', 'Govt. School'),
        ('gen_oth', 'Gen.Oth.'),
        ('general', 'General'),
        ('guest_house', 'Guest House'),
        ('gurudwara', 'Gurudwara'),
        ('heritage_hotel', 'Heritage Hotel'),
        ('housing_board', 'Housing Board'),
        ('host_lib', 'Host./Lib.'),
        ('budget_1_2_3_star_hotel', 'Budget/1,2,3 Star Hotel'),
        ('hotel_50', 'Hotel/50'),
        ('jvvnl', 'JVVNL'),
        ('lic', 'LIC'),
        ('marriage_garden', 'Marriage Garden'),
        ('minor_prop', 'Minor Prop'),
        ('mosque', 'Mosque'),
        ('old_cinema', 'Old Cinema'),
        ('petrol_pump', 'Petrol Pump'),
        ('post_tel_dept', 'Post& Tel. Dept'),
        ('rppn', 'RPPN'),
        ('press', 'Press'),
        ('pvt_hospi_clinic', 'Pvt.Hospi./Clinic'),
        ('pvt_office', 'Pvt. Office'),
        ('pwd', 'PWD'),
        ('ra_poddar_inst_mgmt', 'R A Poddar Inst of Mgmt'),
        ('railways', 'Railways'),
        ('religious_property', 'Religious Property'),
        ('restaurant_cafeteria', 'Restaurant/cafeteria'),
        ('rfc', 'RFC'),
        ('riico_area', 'RIICO(Area)'),
        ('riico_exempted', 'RIICO(EXCEMPTED)'),
        ('riico_general', 'RIICO(General)'),
        ('roadways', 'Roadways'),
        ('rtdc', 'RTDC'),
        ('rvpnl', 'RVPNL'),
        ('sg_building', 'SG Building'),
        ('school', 'School'),
        ('semi_govt_oth_nig', 'Semi Govt.(oth.Nig)'),
        ('tp_college', 'T.P.College'),
        ('temple', 'Temple'),
        ('trust', 'Trust'),
        ('prof_tech_university', 'Prof/Tech University'),
        ('agricultural_land', 'Agricultural Land'),
        ('medal_awarded_police', 'Medal Awarded Police'),
        ('government_exempted', 'Government(Exempted)'),
        ('resort', 'Resort'),
        ('f_fighter', 'F Fighter'),
        ('college', 'College'),
    ]
    
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='floors')
    
    # Floor Information
    floor_name = models.CharField(max_length=50, choices=FLOOR_CHOICES, verbose_name="Floor Name")
    use_type = models.CharField(max_length=50, choices=USE_TYPE_CHOICES, verbose_name="Use Type")
    usage_type = models.CharField(max_length=100, choices=USAGE_TYPE_CHOICES, verbose_name="Usage Type")
    from_year = models.CharField(max_length=20, default='2024-2025', verbose_name="From Year")
    upto_year = models.CharField(max_length=20, blank=True, null=True, verbose_name="Upto Year")
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
        ('', 'Select Status'),
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