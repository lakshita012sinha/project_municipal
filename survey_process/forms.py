from django import forms
from datetime import datetime
from .models import (
    Survey, PropertyOwner, PropertyAddress, PropertyDetails, 
    FloorDetails, PropertyAmenities, SurveyGeotagging
)


def get_year_choices():
    """Generate year choices in format 2007-2008, 2008-2009, etc."""
    current_year = datetime.now().year
    choices = [('', 'Select Year')]
    for year in range(2007, current_year + 2):
        year_range = f"{year}-{year + 1}"
        choices.append((year_range, year_range))
    return choices


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
            'tax_paid': forms.Select(attrs={'class': 'form-control'}),
            'one_time_paid': forms.Select(attrs={'class': 'form-control'}),
            'multi_storage_complex': forms.Select(attrs={'class': 'form-control'}),
            'is_ex_party': forms.Select(attrs={'class': 'form-control'}),
            'surveyor_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter any notes or observations'}),
        }


class PropertyOwnerForm(forms.ModelForm):
    """
    Property Owner Details Form
    """
    class Meta:
        model = PropertyOwner
        fields = ['owner_name', 'guardian_name', 'age', 'mobile_no', 'gender', 'profession', 'relation']
        widgets = {
            'owner_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Owner Name'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Guardian Name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Age'}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mobile Number'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'profession': forms.Select(attrs={'class': 'form-control'}),
            'relation': forms.Select(attrs={'class': 'form-control'}),
        }


class PropertyAddressForm(forms.ModelForm):
    """
    Property Address Details Form
    """
    class Meta:
        model = PropertyAddress
        fields = ['house_no', 'mohalla_colony_name', 'building_name', 'road_name', 'sector', 
                 'mobile_no', 'phone_no', 'email_id', 'landmark', 'pincode', 
                 'permanent_address', 'same_as_permanent', 'communication_address']
        widgets = {
            'house_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter House Number'}),
            'mohalla_colony_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mohalla/Colony Name'}),
            'building_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Building Name'}),
            'road_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Road Name'}),
            'sector': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Sector'}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mobile Number'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'email_id': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email ID'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Landmark'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Pincode'}),
            'permanent_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Permanent Address'}),
            'same_as_permanent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'communication_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Communication Address'}),
        }


class PropertyDetailsForm(forms.ModelForm):
    """
    Property Details Form
    """
    class Meta:
        model = PropertyDetails
        fields = ['area_name', 'ward_no', 'road_type', 'ownership_type', 'use_of_property',
                 'plot_area_sq_yd', 'plinth_area_sq_yd', 'vacant_area_sq_yd', 'no_of_floors']
        widgets = {
            'area_name': forms.Select(attrs={'class': 'form-control'}),
            'ward_no': forms.Select(attrs={'class': 'form-control'}),
            'road_type': forms.Select(attrs={'class': 'form-control'}),
            'ownership_type': forms.Select(attrs={'class': 'form-control'}),
            'use_of_property': forms.Select(attrs={'class': 'form-control'}),
            'plot_area_sq_yd': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter Plot Area'}),
            'plinth_area_sq_yd': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter Plinth Area'}),
            'vacant_area_sq_yd': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter Vacant Area'}),
            'no_of_floors': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Number of Floors'}),
        }


class FloorDetailsForm(forms.ModelForm):
    """
    Floor Details Form
    """
    from_year = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))
    upto_year = forms.ChoiceField(choices=[], required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        year_choices = get_year_choices()
        self.fields['from_year'].choices = year_choices
        self.fields['upto_year'].choices = year_choices
    
    class Meta:
        model = FloorDetails
        fields = ['floor_name', 'use_type', 'usage_type', 'from_year', 'upto_year', 'built_up_area_sq_ft']
        widgets = {
            'floor_name': forms.Select(attrs={'class': 'form-control'}),
            'use_type': forms.Select(attrs={'class': 'form-control'}),
            'usage_type': forms.Select(attrs={'class': 'form-control'}),
            'built_up_area_sq_ft': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter Built Up Area'}),
        }


class PropertyAmenitiesForm(forms.ModelForm):
    """
    Property Amenities Form
    """
    class Meta:
        model = PropertyAmenities
        fields = ['parking', 'street_light', 'sewer_line', 'electricity_connection',
                 'private_toilet', 'sewer_connection', 'septic_tank', 'open_toilet',
                 'piped_water_connection', 'fire_fighting_system', 'boring', 
                 'mobile_tower', 'advertising_hoarding']
        widgets = {
            'parking': forms.Select(attrs={'class': 'form-control'}),
            'street_light': forms.Select(attrs={'class': 'form-control'}),
            'sewer_line': forms.Select(attrs={'class': 'form-control'}),
            'electricity_connection': forms.Select(attrs={'class': 'form-control'}),
            'private_toilet': forms.Select(attrs={'class': 'form-control'}),
            'sewer_connection': forms.Select(attrs={'class': 'form-control'}),
            'septic_tank': forms.Select(attrs={'class': 'form-control'}),
            'open_toilet': forms.Select(attrs={'class': 'form-control'}),
            'piped_water_connection': forms.Select(attrs={'class': 'form-control'}),
            'fire_fighting_system': forms.Select(attrs={'class': 'form-control'}),
            'boring': forms.Select(attrs={'class': 'form-control'}),
            'mobile_tower': forms.Select(attrs={'class': 'form-control'}),
            'advertising_hoarding': forms.Select(attrs={'class': 'form-control'}),
        }


class SurveyGeotaggingForm(forms.ModelForm):
    """
    Geotagging Form
    """
    class Meta:
        model = SurveyGeotagging
        fields = ['latitude', 'longitude', 'accuracy', 'front_photo', 'side_photo_1', 'side_photo_2', 'device_info']
        widgets = {
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00000001', 'placeholder': 'Latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00000001', 'placeholder': 'Longitude'}),
            'accuracy': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'GPS Accuracy (meters)'}),
            'front_photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'side_photo_1': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'side_photo_2': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'device_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Device Information'}),
        }


# Formset for handling multiple floors
FloorDetailsFormSet = forms.modelformset_factory(
    FloorDetails,
    form=FloorDetailsForm,
    extra=1,
    can_delete=True
)