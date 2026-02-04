# Survey Review URL Fix

## Issue
When clicking "View Survey" from the survey form, users encountered a `NoReverseMatch` error:
```
Reverse for 'survey_form_entry' with arguments '(3,)' not found. 1 pattern(s) tried: ['survey/form\\-entry/\\Z']
```

## Root Cause
The issue was caused by using the wrong URL name in the survey review template. The template was trying to use:
- `survey_process:survey_form_entry` with a survey ID parameter

But the correct URL pattern for editing an existing survey is:
- `survey_process:survey_form_edit` with a survey ID parameter

## URL Patterns
From `survey_process/urls.py`:
```python
# For creating new survey (no ID)
path('form-entry/', views.survey_form_entry, name='survey_form_entry'),

# For editing existing survey (with ID)
path('form-entry/<int:survey_id>/', views.survey_form_entry, name='survey_form_edit'),
```

## Files Fixed

### 1. survey_process/templates/survey_process/survey_review.html
**Changed:**
```html
<a class="dropdown-item" href="{% url 'survey_process:survey_form_entry' survey.id %}">
```

**To:**
```html
<a class="dropdown-item" href="{% url 'survey_process:survey_form_edit' survey.id %}">
```

### 2. survey_process/views.py
**Changed:**
```python
return redirect('survey_process:survey_form_entry', survey_id=survey.id)
```

**To:**
```python
return redirect('survey_process:survey_form_edit', survey_id=survey.id)
```

## Solution Summary
- Updated the URL name from `survey_form_entry` to `survey_form_edit` when passing a survey ID
- This ensures the correct URL pattern is matched when editing existing surveys
- The fix applies to both the template and the view redirect

## Testing
- Server starts without errors: ✅
- System check passes: ✅
- URL patterns are correctly defined: ✅

The survey review feature should now work correctly without the NoReverseMatch error.