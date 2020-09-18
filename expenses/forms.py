from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class ExpenseTypeAddForm(forms.ModelForm):
	expense_type = forms.CharField(widget=forms.TextInput(
		attrs = {
			'placeholder' : 'Enter expense type name',
			'class'       : 'form-control',
			'id'          : 'expense_type',
			'required'    : 'required',
		}
		))     
	class Meta:
		model   = ExpenseType
		exclude = ['added_date', 'added_by']