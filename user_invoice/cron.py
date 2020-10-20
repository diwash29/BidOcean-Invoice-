from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import EmployeeForm, RoleAddForm, RateAddForm
from django.contrib.auth.models import User
from manage_user.models import Userdetail
from account_management.models import AccountDetails
from leave.models import LeaveRequest, LeaveBalance
from manage_user.models import Userdetail
from .mixin import AdminOrHRPanelMixin, AdminOrHROrAccountsPanelMixin, AdminPanelMixin, IRPanelMixin, BRPanelMixin, FixedPanelMixin, AdminOrAccountsPanelMixin
from datetime import datetime, date
from django.core.paginator import Paginator
from django.db.models import Q
from leave.models import LeaveBalance
from .utils import get_first_n_last_day, count_leaves, check_invoice, count_file_uploads, listToString

from django.contrib.auth import authenticate, login

import requests
import json
import xlwt
from django.http import JsonResponse

def update_invoice():

	f = open("/home/bds/NewDjango/biocean-invoice/user_invoice/demofile2.txt", "a")
	f.write("Now the file has more content!")
	f.close()
	print("hello~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

	#open and read the file after the appending:
	f = open("/home/bds/NewDjango/biocean-invoice/user_invoice/demofile2.txt", "r")
	print(f.read())