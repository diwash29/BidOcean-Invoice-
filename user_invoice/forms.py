from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class RoleAddForm(forms.ModelForm):
	name = forms.CharField(widget=forms.TextInput(
		attrs = {
			'placeholder' : 'Enter role name',
			'class'       : 'form-control',
			'id'          : 'name',
		}
		))     
	class Meta:
		model   = Role
		exclude = ['status']

class RateAddForm(forms.ModelForm):
    base = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Enter base rate',
            'class'       : 'form-control',
            'id'          : 'base',
            'required'    : 'required',
        }
        ))
    difficultnp = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Difficult & non productive rate',
            'class'       : 'form-control',
            'id'          : 'difficultnp',
            'required'    : 'required',
        }
        )) 
    extra_hours = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Extra hours rate',
            'class'       : 'form-control',
            'id'          : 'extra_hours',
            'required'    : 'required',
        }
        ))
    file_attach = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'File attach rate',
            'class'       : 'form-control',
            'id'          : 'file_attach',
            'required'    : 'required',
        }
        ))
    duplicate_solic = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Duplicate solic rate',
            'class'       : 'form-control',
            'id'          : 'duplicate_solic',
            'required'    : 'required',
        }
        ))  
    entity_cont_wrong = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Entity/Contact wrong/incomplete/not edited rate',
            'class'       : 'form-control',
            'id'          : 'entity_cont_wrong',
            'required'    : 'required',
        }
        ))    
    false_referal = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'False Referral rate',
            'class'       : 'form-control',
            'id'          : 'false_referal',
            'required'    : 'required',
        }
        ))
    fraudsolic_update = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Fraudulent solicitation update rate',
            'class'       : 'form-control',
            'id'          : 'fraudsolic_update',
            'required'    : 'required',
        }
        ))
    source_ret_wo_res = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Source returned without good reason rate',
            'class'       : 'form-control',
            'id'          : 'source_ret_wo_res',
            'required'    : 'required',
        }
        ))
    missed_bond = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Missed Bid Bond/Incomplete Plans & Specs rate',
            'class'       : 'form-control',
            'id'          : 'missed_bond',
            'required'    : 'required',
        }
        ))
    missed_categories = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Missed Categories rate',
            'class'       : 'form-control',
            'id'          : 'missed_categories',
            'required'    : 'required',
        }
        )) 
    missed_solic_src = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Missed Solic./Addend. From Source rate',
            'class'       : 'form-control',
            'id'          : 'missed_solic_src',
            'required'    : 'required',
        }
        ))
    missed_file = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Missed/Incorrect File Type rate',
            'class'       : 'form-control',
            'id'          : 'missed_file',
            'required'    : 'required',
        }
        ))
    missed_link = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Missing or Wrong Outside Link rate',
            'class'       : 'form-control',
            'id'          : 'missed_link',
            'required'    : 'required',
        }
        ))
    missed_term = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Missing or wrong Term Contract rate',
            'class'       : 'form-control',
            'id'          : 'missed_term',
            'required'    : 'required',
        }
        ))
    not_posted_lead = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Not Posted As Lead rate',
            'class'       : 'form-control',
            'id'          : 'not_posted_lead',
            'required'    : 'required',
        }
        ))
    other_error = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Other Error rate',
            'class'       : 'form-control',
            'id'          : 'other_error',
            'required'    : 'required',
        }
        ))
    other_serious_err = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Other Serious Error rate',
            'class'       : 'form-control',
            'id'          : 'other_serious_err',
            'required'    : 'required',
        }
        ))
    refreshing_wds = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Refreshing WDS page to a different source rate',
            'class'       : 'form-control',
            'id'          : 'refreshing_wds',
            'required'    : 'required',
        }
        ))
    wage_not_selected = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Setaside/Prequalification/Prevailing Wage not selected rate',
            'class'       : 'form-control',
            'id'          : 'wage_not_selected',
            'required'    : 'required',
        }
        ))
    skipped_solic = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Skipped solicitation rate',
            'class'       : 'form-control',
            'id'          : 'skipped_solic',
            'required'    : 'required',
        }
        ))
    source_ret_wo_note = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Source returned without a note rate',
            'class'       : 'form-control',
            'id'          : 'source_ret_wo_note',
            'required'    : 'required',
        }
        ))
    unjustified_absence = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Unexcused/unjustified absence rate',
            'class'       : 'form-control',
            'id'          : 'unjustified_absence',
            'required'    : 'required',
        }
        ))
    wrong_pre_bid = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Wrong bid/pre-bid, mandatory rate',
            'class'       : 'form-control',
            'id'          : 'wrong_pre_bid',
            'required'    : 'required',
        }
        ))
    wrong_categories = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Wrong categories rate',
            'class'       : 'form-control',
            'id'          : 'wrong_categories',
            'required'    : 'required',
        }
        ))
    wrong_geo_location = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Wrong geographic location rate',
            'class'       : 'form-control',
            'id'          : 'wrong_geo_location',
            'required'    : 'required',
        }
        ))
    incorrect_scope = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Incomplete or incorrect scope rate',
            'class'       : 'form-control',
            'id'          : 'incorrect_scope',
            'required'    : 'required',
        }
        ))
    wrong_text_format = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Wrong text format rate',
            'class'       : 'form-control',
            'id'          : 'wrong_text_format',
            'required'    : 'required',
        }
        ))   
    auth_day_off = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Authorized Days Off rate',
            'class'       : 'form-control',
            'id'          : 'auth_day_off',
            'required'    : 'required',
        }
        ))
    unauth_day_off = forms.CharField(widget=forms.TextInput(
        attrs = {
            'placeholder' : 'Unauthorized Days Off rate',
            'class'       : 'form-control',
            'id'          : 'unauth_day_off',
            'required'    : 'required',
        }
        ))                                                                                                                         
    class Meta:
        model  = Rate
        exclude = ['added_by', 'is_approved']        	   

class EmployeeForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder' : 'Enter your name',
            'class'       : 'form-control',
            'id'          : 'name'
        }
    ))

    salary = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder' : 'Enter your salary',
            'class'       : 'form-control',
            'id'          : 'salary'
        }
    ))

    address = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder' : 'Enter your address',
            'class'       : 'form-control',
            'id'          : 'address'
        }
    ))

    phone_no = forms.CharField(widget=forms.TextInput(
        attrs= {
            'placeholder' : 'Enter your phone no',
            'class'       : 'form-control',
            'id'          : 'phone_no',
            'pattern'     : '[6-9]{1}[0-9]{9}'
        }
    ))

    leaves = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder' : 'Enter total no of leaves',
            'class'       : 'form-control',
            'id'          : 'leaves'
        }
    ))

    class Meta:
        model = Employee
        fields = ['name', 'salary', 'address', 'phone_no', 'leaves', 'role']        