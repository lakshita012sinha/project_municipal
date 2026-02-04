from django.urls import path
from . import views

app_name = 'survey_process'

urlpatterns = [
    # Dashboard and Main Views
    path('', views.survey_dashboard, name='dashboard'),
    path('create/', views.create_survey, name='create_survey'),
    path('list/', views.survey_list, name='survey_list'),
    
    # Survey Form Entry Process
    path('form-entry/', views.survey_form_entry, name='survey_form_entry'),
    path('form-entry/<int:survey_id>/', views.survey_form_entry, name='survey_form_edit'),
    path('<int:survey_id>/owner-details/', views.survey_owner_details, name='survey_owner_details'),
    path('<int:survey_id>/address-details/', views.survey_address_details, name='survey_address_details'),
    path('<int:survey_id>/property-details/', views.survey_property_details, name='survey_property_details'),
    path('<int:survey_id>/floor-details/', views.survey_floor_details, name='survey_floor_details'),
    path('<int:survey_id>/amenities/', views.survey_amenities, name='survey_amenities'),
    
    # Geotagging
    path('<int:survey_id>/geotagging/', views.survey_geotagging, name='survey_geotagging'),
    
    # Survey Management
    path('<int:survey_id>/', views.survey_detail, name='survey_detail'),
    path('<int:survey_id>/review/', views.survey_review, name='survey_review'),
    path('<int:survey_id>/save-final/', views.survey_save_final, name='survey_save_final'),
    path('<int:survey_id>/delete/', views.delete_survey, name='delete_survey'),
    
    # Export functionality
    path('export/', views.export_survey_data, name='export_survey_data'),
    
    # AJAX Endpoints
    path('get-location/', views.get_location, name='get_location'),
]