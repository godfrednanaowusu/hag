from django import forms
from django.forms import ModelForm
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from crispy_forms.helper import *
from crispy_forms.layout import *

class NominationsForm(ModelForm):
	class Meta:
			model = Nominations
			fields = ['nominee_photograph', 'nominee_firstname', 'nominee_middlename', 'nominee_lastname', 'nominee_phonenumber', 'nominee_emailaddress', 'nominee_gender', 'nominee_agegroup', 'nominee_bio', 'nominee_deserve_info', 'nominee_reference_links', 'nominee_towncity', 'nominee_region', 'nominee_country', 'company_logo', 'company_name', 'company_industry', 'company_bio', 'nominator_fullname', 'nominator_phonenumber', 'nominator_emailaddress', 'nominator_bio', 'nominator_knownnominee_time', 'nominator_nominee_relationship']

class Covid19NominationsForm(ModelForm):
	class Meta:
			model = Nominations
			fields = ['nominee_photograph', 'nominee_firstname', 'nominee_middlename', 'nominee_lastname', 'nominee_phonenumber', 'nominee_emailaddress', 'nominee_gender', 'nominee_agegroup', 'nominee_bio', 'nominee_deserve_info', 'nominee_reference_links', 'nominee_towncity', 'nominee_region', 'nominee_country', 'company_logo', 'company_name', 'company_industry', 'company_bio']


class NomineeForm(ModelForm):
    '''This Form handles Nominee Operations.'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nominee_photograph', css_class='form-group col-12'),
                css_class='form-row'
            ),
			Row(
                Column('category', css_class='form-group col-12 col-md-3 mb-0'),
				Column('nominee_code', css_class='form-group col-12 col-md-4 mb-0'),
                Column('referencenumber', css_class='form-group col-12 col-md-5 mb-0'),
                css_class='form-row'
            ),
			Row(
                Column('nominee_firstname', css_class='form-group col-12 col-md-4 mb-0'),
                Column('nominee_middlename', css_class='form-group col-12 col-md-4 mb-0'),
				Column('nominee_lastname', css_class='form-group col-12 col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('nominee_phonenumber', css_class='form-group col-12 col-md-5 mb-0'),
                Column('nominee_emailaddress', css_class='form-group col-12 col-md-7 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('nominee_gender', css_class='form-group col-6 col-md-6 mb-0'),
                Column('nominee_agegroup', css_class='form-group col-6 col-md-6 mb-0'),
                css_class='form-row'
            ),
			Row(
                Column('nominee_bio', css_class='form-group col-6 col-md-6 mb-0'),
                Column('nominee_deserve_info', css_class='form-group col-6 col-md-6 mb-0'),
                css_class='form-row'
            ),
			Row(
                Column('nominee_effort_info', css_class='form-group col-6 col-md-6 mb-0'),
                Column('nominee_turning_point', css_class='form-group col-6 col-md-6 mb-0'),
                css_class='form-row'
            ),
			Row(
                Column('nominee_exception', css_class='form-group col-6 col-md-6 mb-0'),
                Column('nominee_reference_links', css_class='form-group col-6 col-md-6 mb-0'),
                css_class='form-row'
            ),
			Row(
                Column('nominee_towncity', css_class='form-group col-6 col-md-4 mb-0'),
                Column('nominee_region', css_class='form-group col-6 col-md-4 mb-0'),
				Column('nominee_country', css_class='form-group col-6 col-md-4 mb-0'),
                css_class='form-row'
            ),
			Row(
                Column('nominee_towncity', css_class='form-group col-6 col-md-4 mb-0'),
                Column('nominee_region', css_class='form-group col-6 col-md-4 mb-0'),
				Column('nominee_country', css_class='form-group col-6 col-md-4 mb-0'),
                css_class='form-row'
            ),
			'hr'
			'nominator_fullname',
			Row(
                Column('nominator_phonenumber', css_class='form-group col-12 col-md-5 mb-0'),
                Column('nominator_emailaddress', css_class='form-group col-12 col-md-7 mb-0'),
                css_class='form-row'
            ),
			'nominator_bio',
			Row(
                Column('nominator_knownnominee_time', css_class='form-group col-12 col-md-6 mb-0'),
                Column('nominator_nominee_relationship', css_class='form-group col-12 col-md-6 mb-0'),
                css_class='form-row'
            ),	
            Row(
                Column('shortlisted', css_class='form-group col-12 col-md-4 mb-0'),
                Column('approved', css_class='form-group col-12 col-md-4 mb-0'),
                css_class='form-row'
            ),		
            # ButtonHolder(
            #     Submit('submit', 'Create New', css_class='btn-success'),
            #     Submit('update', 'Update', css_class='btn-info'),
            #     Button('delete', 'Delete', css_class='btn-danger'),
            #     css_class='btn-group'
            # ),
        )

    class Meta:
        model = Nominations
        exclude = ['deleted', 'datecreated', 'updated']
        widgets = {
            'nominee_code': forms.TextInput(attrs={'readonly': True}),
            'referencenumber': forms.TextInput(attrs={'readonly': True}),
            'nominee_bio': forms.Textarea(attrs={'rows': 2}),
			'nominee_deserve_info': forms.Textarea(attrs={'rows': 2}),
			'nominee_effort_info': forms.Textarea(attrs={'rows': 2}),
			'nominee_turning_point': forms.Textarea(attrs={'rows': 2}),
			'nominee_exception': forms.Textarea(attrs={'rows': 2}),
			'nominee_reference_links': forms.Textarea(attrs={'rows': 2}),
			'nominator_bio': forms.Textarea(attrs={'rows': 2}),
        }
