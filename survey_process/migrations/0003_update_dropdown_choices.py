# Generated manually for dropdown choices update

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey_process', '0002_survey_survey_number'),
    ]

    operations = [
        # Update Survey model fields
        migrations.AlterField(
            model_name='survey',
            name='service_no',
            field=models.CharField(blank=True, max_length=50, unique=True, verbose_name='Service Number'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='unique_key',
            field=models.CharField(blank=True, max_length=100, unique=True, verbose_name='Unique Key'),
        ),
        
        # Update PropertyDetails model fields
        migrations.AlterField(
            model_name='propertydetails',
            name='road_type',
            field=models.CharField(choices=[('interior', 'Interior'), ('exterior', 'Exterior')], max_length=50, verbose_name='Road Type'),
        ),
        migrations.AlterField(
            model_name='propertydetails',
            name='ownership_type',
            field=models.CharField(choices=[('allotment_land_house', 'Allotment Land/House'), ('ancestral', 'Ancestral'), ('possession', 'Possession')], max_length=50, verbose_name='Ownership Type'),
        ),
        migrations.AlterField(
            model_name='propertydetails',
            name='use_of_property',
            field=models.CharField(choices=[('residential_individual_house', 'Residential - Individual House'), ('residential_apartment', 'Residential - Apartment'), ('residential_cum_commercial', 'Residential cum Commercial'), ('school', 'School'), ('professional_college', 'Professional College'), ('general_degree_college', 'General Degree College'), ('coaching_institute', 'Coaching Institute'), ('private_hospital_clinic', 'Private Hospital/Clinic'), ('beauty_parlor', 'Beauty Parlor'), ('cinema_hall_multiplex', 'Cinema Hall/Multiplex'), ('marriage_garden_hall', 'Marriage Garden/Hall'), ('hotel_restaurant', 'Hotel/Restaurant'), ('private_office', 'Private Office'), ('semi_govt_institute', 'Semi Govt. Institute'), ('central_govt_property_office', 'Central Govt. Property Office'), ('state_govt_autonomous_board', 'State Govt. Autonomous Board'), ('state_govt_company', 'State Govt. Company'), ('corporation', 'Corporation'), ('completely_religious_property', 'Completely Religious Property'), ('situated_in_riico_area', 'Situated in RIICO Area'), ('out_of_riico_industries', 'Out of RIICO Industries'), ('exempted_under_clause_107', 'Exempted Under clause 107 of RM Act 2009'), ('dharmshala_community_society', 'Dharmshala of Community society'), ('temple', 'Temple'), ('mosque', 'Mosque'), ('gurudwara', 'Gurudwara'), ('others', 'Others')], max_length=100, verbose_name='Use of Property'),
        ),
        
        # Update FloorDetails model fields
        migrations.AlterField(
            model_name='floordetails',
            name='floor_name',
            field=models.CharField(choices=[('', 'Select Floor'), ('basement', 'Basement'), ('ground', 'Ground Floor'), ('1st', '1st Floor'), ('2nd', '2nd Floor'), ('3rd', '3rd Floor'), ('4th', '4th Floor'), ('5th', '5th Floor'), ('6th', '6th Floor'), ('7th', '7th Floor'), ('8th', '8th Floor'), ('9th', '9th Floor'), ('10th', '10th Floor'), ('11th', '11th Floor'), ('12th', '12th Floor'), ('13th', '13th Floor'), ('14th', '14th Floor'), ('15th', '15th Floor'), ('16th', '16th Floor'), ('17th', '17th Floor'), ('18th', '18th Floor'), ('19th', '19th Floor'), ('20th', '20th Floor'), ('21st', '21st Floor'), ('22nd', '22nd Floor'), ('23rd', '23rd Floor'), ('24th', '24th Floor'), ('25th', '25th Floor'), ('vacant_land', 'Vacant Land'), ('basement_2', 'Basement 2'), ('basement_3', 'Basement 3'), ('lower_ground', 'Lower Ground')], max_length=50, verbose_name='Floor Name'),
        ),
        migrations.AlterField(
            model_name='floordetails',
            name='use_type',
            field=models.CharField(choices=[('residential', 'Residential'), ('commercial', 'Commercial'), ('industrial', 'Industrial'), ('institution', 'INSTITUTION')], max_length=50, verbose_name='Use Type'),
        ),
        migrations.AlterField(
            model_name='floordetails',
            name='usage_type',
            field=models.CharField(choices=[('', 'Select'), ('4_5_star_hotel', '4/5 Star Hotel'), ('agri_dept', 'Agri.Dept.'), ('airport', 'AirPort'), ('bank', 'Bank'), ('beauty_parlour', 'Beauty Parlour'), ('bhandar_nigam', 'Bhandar Nigam'), ('bsnl', 'Bsnl'), ('central_govt_oth_nigams', 'Central Govt.(oth.nigams)'), ('central_govt_building', 'Central Govt.Building'), ('cinema_multiplex', 'Cinema(Multiplex)'), ('clubs', 'Clubs'), ('corporate_building', 'Corporate Building'), ('coaching_inst', 'Coaching Inst.'), ('comm_center', 'Comm.Center'), ('jda', 'JDA'), ('dharamsala_sarai_musafirkhana', 'Dharamsala/Sarai/Musafirkhana'), ('ex_army_service', 'Ex-Army Service'), ('fci', 'F.C.I'), ('ex_army_fighter', 'Ex-Army Fighter'), ('govt_hospital', 'Govt. Hospital'), ('govt_school', 'Govt. School'), ('gen_oth', 'Gen.Oth.'), ('general', 'General'), ('guest_house', 'Guest House'), ('gurudwara', 'Gurudwara'), ('heritage_hotel', 'Heritage Hotel'), ('housing_board', 'Housing Board'), ('host_lib', 'Host./Lib.'), ('budget_1_2_3_star_hotel', 'Budget/1,2,3 Star Hotel'), ('hotel_50', 'Hotel/50'), ('jvvnl', 'JVVNL'), ('lic', 'LIC'), ('marriage_garden', 'Marriage Garden'), ('minor_prop', 'Minor Prop'), ('mosque', 'Mosque'), ('old_cinema', 'Old Cinema'), ('petrol_pump', 'Petrol Pump'), ('post_tel_dept', 'Post& Tel. Dept'), ('rppn', 'RPPN'), ('press', 'Press'), ('pvt_hospi_clinic', 'Pvt.Hospi./Clinic'), ('pvt_office', 'Pvt. Office'), ('pwd', 'PWD'), ('ra_poddar_inst_mgmt', 'R A Poddar Inst of Mgmt'), ('railways', 'Railways'), ('religious_property', 'Religious Property'), ('restaurant_cafeteria', 'Restaurant/cafeteria'), ('rfc', 'RFC'), ('riico_area', 'RIICO(Area)'), ('riico_exempted', 'RIICO(EXCEMPTED)'), ('riico_general', 'RIICO(General)'), ('roadways', 'Roadways'), ('rtdc', 'RTDC'), ('rvpnl', 'RVPNL'), ('sg_building', 'SG Building'), ('school', 'School'), ('semi_govt_oth_nig', 'Semi Govt.(oth.Nig)'), ('tp_college', 'T.P.College'), ('temple', 'Temple'), ('trust', 'Trust'), ('prof_tech_university', 'Prof/Tech University'), ('agricultural_land', 'Agricultural Land'), ('medal_awarded_police', 'Medal Awarded Police'), ('government_exempted', 'Government(Exempted)'), ('resort', 'Resort'), ('f_fighter', 'F Fighter'), ('college', 'College')], max_length=100, verbose_name='Usage Type'),
        ),
        migrations.AlterField(
            model_name='floordetails',
            name='from_year',
            field=models.CharField(default='2024-2025', max_length=20, verbose_name='From Year'),
        ),
        migrations.AlterField(
            model_name='floordetails',
            name='upto_year',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Upto Year'),
        ),
    ]