# Manual Dropdown Updates Guide

## Overview
This document contains all the changes needed to update the dropdown options as requested. All dropdown fields now have "Select" as the first option, and service number and unique key are fully optional.

## Changes Made to Models

### 1. Survey Model (models.py)
**Make service_no and unique_key optional:**
```python
# Change these lines in the Survey model:
service_no = models.CharField(max_length=50, blank=True, null=True, verbose_name="Service Number")
unique_key = models.CharField(max_length=100, blank=True, null=True, verbose_name="Unique Key")
```

**Add "Select" options to all Survey choices:**
```python
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
```

### 2. PropertyOwner Model (models.py)
**Add "Select" options to all PropertyOwner choices:**
```python
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
```

### 3. PropertyDetails Model (models.py)
**Add "Select" options to all PropertyDetails choices:**
```python
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
```

### 4. FloorDetails Model (models.py)
**Add "Select" options to FloorDetails choices:**
```python
USE_TYPE_CHOICES = [
    ('', 'Select Use Type'),
    ('residential', 'Residential'),
    ('commercial', 'Commercial'),
    ('industrial', 'Industrial'),
    ('institution', 'INSTITUTION'),
]

# Floor choices and Usage type choices already have "Select" options
```

### 5. PropertyAmenities Model (models.py)
**Add "Select" options to PropertyAmenities choices:**
```python
AMENITY_CHOICES = [
    ('', 'Select Status'),
    ('available', 'Available'),
    ('not_available', 'Not Available'),
    ('partial', 'Partial'),
]
```

## Changes Made to Forms

### 1. SurveyBasicForm (forms.py)
**Make service_no and unique_key not required:**
```python
class SurveyBasicForm(forms.ModelForm):
    """
    Basic Survey Information Form
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make service_no and unique_key not required
        self.fields['service_no'].required = False
        self.fields['unique_key'].required = False
    
    class Meta:
        model = Survey
        fields = ['service_no', 'unique_key', 'tax_paid', 'one_time_paid', 
                 'multi_storage_complex', 'is_ex_party', 'surveyor_notes']
        widgets = {
            'service_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Service Number (Optional)'}),
            'unique_key': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Unique Key (Optional)'}),
            # ... rest of widgets remain the same
        }
```

## Migration Steps

### Step 1: Apply Model Changes
1. All model changes have been applied to models.py
2. All form changes have been applied to forms.py

### Step 2: Run Migrations
```bash
# In a fresh command prompt/terminal:
cd project_municipal
python manage.py migrate
```

### Step 3: Test the Changes
```bash
python manage.py runserver
```

## Expected Results

After applying these changes, you should see:

### All Dropdown Fields:
- **First Option**: "Select [Field Name]" (e.g., "Select Gender", "Select Area", etc.)
- **Service Number**: Optional field (can be left blank)
- **Unique Key**: Optional field (can be left blank)

### Survey Basic Form:
- **Tax Paid**: Select Tax Status, Yes, No, Partial
- **One Time Paid**: Select One Time Payment, Yes, No
- **Multi Storage Complex**: Select Multi Storage, Yes, No
- **Ex Party**: Select Ex Party, Yes, No

### Property Owner Form:
- **Gender**: Select Gender, Male, Female, Other
- **Profession**: Select Profession, Business, Service, etc.
- **Relation**: Select Relation, Self, Father, Mother, etc.

### Property Details Form:
- **Area Name**: Select Area, Area 1, Area 2, etc.
- **Ward Number**: Select Ward, Ward 1, Ward 2, etc.
- **Road Type**: Select Road Type, Interior, Exterior
- **Ownership Type**: Select Ownership Type, Allotment Land/House, etc.
- **Use of Property**: Select Use of Property, Residential - Individual House, etc.

### Floor Details Form:
- **Floor Name**: Select Floor, Basement, Ground Floor, etc.
- **Use Type**: Select Use Type, Residential, Commercial, etc.
- **Usage Type**: Select, 4/5 Star Hotel, etc.
- **From Year**: Select Year, 2007-2008, 2008-2009, etc.
- **Upto Year**: Select Year, 2007-2008, 2008-2009, etc.

### Property Amenities Form:
- **All Amenities**: Select Status, Available, Not Available, Partial

## Files Modified

1. `survey_process/models.py` - Added "Select" options to all dropdown choices and made service_no/unique_key optional
2. `survey_process/forms.py` - Updated SurveyBasicForm to make fields not required
3. `survey_process/migrations/0004_update_dropdown_select_options.py` - New migration file

## Notes

- All dropdown options now have "Select" as the first option
- Service number and unique key are completely optional (can be blank/null)
- No unique constraints on service_no and unique_key when they are blank
- All existing functionality remains intact
- Migration file created to update database schema

## Next Steps

1. Run the migration: `python manage.py migrate`
2. Test all dropdown options in the forms
3. Verify that optional fields work correctly
4. Test the survey creation and review process