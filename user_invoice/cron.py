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
	main_url   = "https://www.bidocean.com/api/production/request.php"
	main_token = "Pr85SNYWOV3GQdKProdReqstwer53VjZpA6lHoegm"
	today              = datetime.now()   
	date               = today.strftime("%Y-%m")
	monthdate          = datetime.strptime(date, '%Y-%m').date()        
	first_and_last_day = get_first_n_last_day(today.year,today.month) 
	rate               =  Rate.objects.get(is_approved=1)

	try:
		month                = int(monthdate.month)
		pdeduction_obj       = MonthlyDeduction.objects.get(month=month)
		percentage_deduction = float(pdeduction_obj.deduction_percent)       
	except:
		percentage_deduction = 0.0

	

	mainData               = {}
	mainData['empid']      = ""
	mainData['date_start'] = first_and_last_day[0].strftime("%m/%d/%y")
	mainData['date_end']   = first_and_last_day[1].strftime("%m/%d/%y")
	mainData['request']    = 'wds_researcher_stats'
	mainData['token']      = main_token
	mainDataJson           = json.dumps(mainData, ensure_ascii = 'False')
	main_result = requests.post(main_url, json = mainDataJson)
	main_json   = main_result.json()
	for each_emp in main_json:
		employee_id =  int(main_json[each_emp]['emp_id'])
		try:
			employee    =  Employee.objects.get(emp_id=employee_id)
			# print(employee)
			leaves      = count_leaves(employee, monthdate)
			file_upload = count_file_uploads(employee, monthdate)
			employee_id = employee.emp_id
			emp_fixed_salary = employee.salary
			# print(employee.salary)
			if employee.salary == 'None' or employee.salary is None or employee.salary == "":
				emp_fixed_salary = 0.0 


			url1   = 'https://www.bidocean.com/api/production/request.php'
			token1 = "Pr85SNYWOV3GQdKProdReqstwer53VjZpA6lHoegm"

			requestData1               = {}
			requestData1["empid"]      = int(employee_id)#1296#
			requestData1["year_month"] = date
			requestData1["request"]    = 'emp_production'
			requestData1["token"]      = token1

			requestDataJson1 = json.dumps(requestData1, ensure_ascii = 'False')
			result1          = requests.post(url1, json = requestDataJson1)
			production_data  = result1.json()


			total_solocitaion_count = main_json[each_emp]['total_solicitation']
			total_source_count      = main_json[each_emp]['total_source_count']
			total_edits             = main_json[each_emp]['total_edits']
			wds_solocitaion_amt     = total_solocitaion_count*float(rate.wds_solicitaion)
			wds_source_amt          = total_source_count*float(rate.wds_source)
			wds_edits_amt           = total_edits*float(rate.wds_edit)
			file_upload_amt         = file_upload*float(rate.file_attach)
			leaves_deduction        = (leaves*float(rate.auth_day_off)) + float(production_data['Total Fine'])
			leaves_deduction        = round(leaves_deduction, 2)
			total_pay        = float(wds_solocitaion_amt)+float(wds_source_amt)+float(wds_edits_amt)+float(file_upload_amt)+float(emp_fixed_salary)-leaves_deduction
			total_pay        = float(round(total_pay*(1.0-(percentage_deduction/100)), 2))

			ch_invoice       = check_invoice(employee)
			# print(ch_invoice)
			# print("~~~~~~~~~~~~~~~")
			if ch_invoice is None:
				# print(today)
				# print(production_data['Total Fine'])
				# print(total_solocitaion_count)
				# print(total_source_count)
				# print(total_edits)
				# print(file_upload)
				# print(leaves)
				# print(leaves_deduction)
				# print(total_pay)
				# print(employee)
				# print(percentage_deduction)
				invoice_add = Invoice.objects.create(invoice_date=today, monthdate=today, production_pay_deduction=production_data['Total Fine'], wds_solicitaion=total_solocitaion_count, wds_source=total_source_count, wds_edit=total_edits, file_upload=file_upload, authorised_day_off = leaves,  total_deduction = leaves_deduction , total_payable = total_pay, emp_ownwer = employee, percent_deduction=percentage_deduction, wds_solicitaion_rate=rate.wds_solicitaion, wds_source_rate=rate.wds_source, wds_edit_rate=rate.wds_edit,fixed_salary=emp_fixed_salary, auth_day_rate=rate.auth_day_off)  
				# print("added")
			else:
				invoice_edit                          = Invoice.objects.get(pk=ch_invoice)
				invoice_edit.production_pay_deduction = production_data['Total Fine']
				invoice_edit.wds_solicitaion          = total_solocitaion_count
				invoice_edit.wds_source               = total_source_count
				invoice_edit.wds_edit                 = total_edits
				invoice_edit.file_upload              = file_upload
				invoice_edit.authorised_day_off       = leaves 
				invoice_edit.total_deduction          = leaves_deduction
				invoice_edit.total_payable            = total_pay
				invoice_edit.percent_deduction        = percentage_deduction
				invoice_edit.wds_solicitaion_rate     = rate.wds_solicitaion
				invoice_edit.wds_source_rate          = rate.wds_source
				invoice_edit.wds_edit_rate            = rate.wds_edit
				invoice_edit.fixed_salary             = emp_fixed_salary
				invoice_edit.auth_day_rate            = rate.auth_day_off
				invoice_edit.save()
				# print("edited")


			

		except:
			pass
			# print("not even logined yet")	
		# employee_id =  each_emp['emp_id']
		# print(employee_id)
		# print(each_emp)

	# f = open("/home/bds/NewDjango/biocean-invoice/user_invoice/demofile2.txt", "a")
	# f.write("Now the file has more content!")
	# f.close()
	# print("hello~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

	# #open and read the file after the appending:
	# f = open("/home/bds/NewDjango/biocean-invoice/user_invoice/demofile2.txt", "r")
	# print(f.read())