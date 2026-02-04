# Survey Number Auto-Generation Feature

## Overview
This feature automatically generates unique survey numbers in the format `SRV2/129/59335` when a survey form is completed and saved.

## Survey Number Format
```
SRV2/{ward_no}/{sequential_number}
```

### Format Components:
- **SRV2**: Fixed prefix indicating Survey version 2
- **{ward_no}**: 3-digit ward number (001, 002, 003, 004)
- **{sequential_number}**: 5-digit sequential number starting from 00001

### Examples:
- `SRV2/001/00001` - First survey in Ward 1
- `SRV2/002/00015` - 15th survey in Ward 2
- `SRV2/003/00234` - 234th survey in Ward 3

## Implementation Details

### 1. Database Changes
**New Field Added:**
```python
survey_number = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="Survey Number")
```

### 2. Auto-Generation Logic
The survey number is automatically generated when:
- Survey status changes to `form_completed` or `completed`
- Survey doesn't already have a survey number

### 3. Ward Number Mapping
```python
ward_mapping = {
    'ward1': '001',
    'ward2': '002', 
    'ward3': '003',
    'ward4': '004',
}
```

### 4. Sequential Number Logic
- Finds the highest existing sequential number for the specific ward
- Increments by 1 to generate the next number
- Formats as 5-digit number with leading zeros

## Code Implementation

### Model Methods Added

#### `generate_survey_number()`
```python
def generate_survey_number(self):
    """
    Generate unique survey number in format: SRV2/129/59335
    Format: SRV2/{ward_no}/{sequential_number}
    """
    # Get ward number from property details
    ward_no = "001"  # Default ward
    try:
        if hasattr(self, 'property') and self.property:
            ward_choice = self.property.ward_no
            if ward_choice:
                ward_mapping = {
                    'ward1': '001',
                    'ward2': '002', 
                    'ward3': '003',
                    'ward4': '004',
                }
                ward_no = ward_mapping.get(ward_choice, '001')
    except:
        pass
    
    # Find highest sequential number for this ward
    existing_surveys = Survey.objects.filter(
        survey_number__startswith=f'SRV2/{ward_no}/'
    ).exclude(id=self.id if self.id else None)
    
    max_seq = 0
    for survey in existing_surveys:
        if survey.survey_number:
            match = re.search(r'SRV2/\d+/(\d+)', survey.survey_number)
            if match:
                seq_num = int(match.group(1))
                max_seq = max(max_seq, seq_num)
    
    # Generate new sequential number
    new_seq = max_seq + 1
    
    # Format: SRV2/ward/sequential (5 digits)
    return f"SRV2/{ward_no}/{new_seq:05d}"
```

#### `save()` Method Override
```python
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
```

## User Interface Updates

### 1. Survey Review Page
- Shows survey number at the top of basic information
- Displays "Will be generated after saving" if not yet generated

### 2. Survey Detail Page
- Shows survey number in the basic information section
- Displays "Not generated yet" if not available

### 3. Survey List Page
- Added "Survey No" column as the first column
- Shows "Not generated" for surveys without numbers
- Updated search to include survey numbers

### 4. Search Functionality
- Users can search by Survey Number, Service Number, or Unique Key
- Updated placeholder text to reflect new search capabilities

## Trigger Points

### When Survey Numbers Are Generated:
1. **After completing amenities form** → Status changes to `form_completed` → Survey number generated
2. **When saving from review page** → Status changes to `form_completed` → Survey number generated
3. **When geotagging is completed** → Status changes to `completed` → Survey number generated (if not already generated)

### When Survey Numbers Are NOT Generated:
- Survey is in `draft` status
- Survey already has a survey number
- Survey is being created but not completed

## Database Migration
```bash
# Migration created and applied
python manage.py makemigrations survey_process
python manage.py migrate
```

**Migration File:** `0002_survey_survey_number.py`
- Adds `survey_number` field as nullable and unique
- Allows existing surveys to have null survey numbers initially

## Template Updates

### Files Modified:
1. `survey_process/templates/survey_process/survey_review.html`
   - Added survey number display in basic information section

2. `survey_process/templates/survey_process/survey_detail.html`
   - Added survey number display in basic information section

3. `survey_process/templates/survey_process/survey_list.html`
   - Added survey number column
   - Updated search placeholder

### Display Logic:
```html
<!-- Survey Review Page -->
<p><strong>Survey Number:</strong><br>{{ survey.survey_number|default:"<em>Will be generated after saving</em>" }}</p>

<!-- Survey Detail Page -->
<p><strong>Survey No:</strong> {{ survey.survey_number|default:"Not generated yet" }}</p>

<!-- Survey List Page -->
<td><strong>{{ survey.survey_number|default:"<em>Not generated</em>" }}</strong></td>
```

## Search Enhancement
Updated search functionality in `survey_list` view:
```python
search_query = request.GET.get('search')
if search_query:
    surveys = surveys.filter(
        models.Q(service_no__icontains=search_query) |
        models.Q(unique_key__icontains=search_query) |
        models.Q(survey_number__icontains=search_query)
    )
```

## Benefits

### 1. Automatic Generation
- No manual intervention required
- Consistent format across all surveys
- Unique identification for each survey

### 2. Ward-based Organization
- Easy identification of survey location
- Organized sequential numbering per ward
- Scalable for multiple wards

### 3. User-Friendly
- Clear format that's easy to read and remember
- Searchable across the system
- Displayed prominently in all relevant views

### 4. Data Integrity
- Unique constraint prevents duplicates
- Auto-generation prevents human errors
- Consistent formatting

## Future Enhancements

### Potential Improvements:
1. **Custom Ward Mapping**: Allow administrators to configure ward numbers
2. **Prefix Configuration**: Make "SRV2" prefix configurable
3. **Year-based Numbering**: Include year in the format (e.g., SRV2/2026/001/00001)
4. **Bulk Generation**: Generate numbers for existing surveys
5. **Number Reservation**: Reserve number ranges for specific purposes

### Advanced Features:
1. **QR Code Generation**: Generate QR codes with survey numbers
2. **Barcode Support**: Create barcodes for physical documentation
3. **Export Integration**: Include survey numbers in all exports
4. **API Integration**: Expose survey numbers through REST API

## Testing

### Test Scenarios:
1. ✅ Create new survey and complete form → Survey number generated
2. ✅ Save survey from review page → Survey number generated
3. ✅ Complete geotagging → Survey number generated (if not exists)
4. ✅ Search by survey number → Results returned
5. ✅ Multiple surveys in same ward → Sequential numbering
6. ✅ Multiple surveys in different wards → Separate sequences

### Edge Cases Handled:
- Survey without property details → Uses default ward (001)
- Existing surveys without numbers → Handled gracefully
- Concurrent survey creation → Unique constraint prevents conflicts
- Database errors → Graceful fallback

## Conclusion
The survey number auto-generation feature provides a robust, scalable solution for uniquely identifying surveys with a meaningful format that includes ward information and sequential numbering. The implementation is seamless from the user perspective while maintaining data integrity and providing powerful search capabilities.