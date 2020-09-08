from django.shortcuts import render,HttpResponse,HttpResponseRedirect,reverse
from django.core.paginator import Paginator
from django.views.generic import View
from django.contrib import messages
import datetime
import math

from user_invoice.models import Employee
from django.contrib.auth.models import User

from .converter import convertToWords
from .models import EmployeeDetail
from .utils import *

# Create your views here.

def createEmployee(request):
	user           = request.user
	employee       = Employee.objects.get(auth_tbl=user)
	rolename       = employee.role.name.lower()

	if request.method=="POST":
		form = EmployeeDetail.objects.create(
			first_name 		= request.POST['first_name'],
			last_name 		= request.POST['last_name'],
			designation 	= request.POST['designation'],
			email 			= request.POST['email'],
			phone 			= request.POST['phone'],
			joining_date 	= request.POST['joining_date'],
			ctc 			= request.POST['ctc'],
		)
		form.save()
		messages.success(request,'Employee Just Added')
		return HttpResponseRedirect(reverse('letter:employee-list'))
	
	return render(request,'letter/add_employee.html', {'role':rolename, "employee":employee})

def employeeList(request):
	employee_list = EmployeeDetail.objects.all()

	firstName = request.POST.get('first_name')
	lastName = request.POST.get('last_name')

	if firstName != '' and firstName is not None:
		employee_list = EmployeeDetail.objects.filter(first_name__icontains = firstName)

	if lastName != '' and lastName is not None:
		employee_list = EmployeeDetail.objects.filter(last_name__icontains = lastName)
	
	paginator = Paginator(employee_list, 50)
	page = request.GET.get('page')
	employee_list = paginator.get_page(page)
	user           = request.user
	employee       = Employee.objects.get(auth_tbl=user)
	rolename       = employee.role.name.lower()

	context = {
		'emps':employee_list,
		'role':rolename
	}
	return render(request,'letter/employee_list.html',context)


def generatePDF(request,pk):
	employee = EmployeeDetail.objects.get(id=pk)
	salary_annually = employee.ctc
	words_salary = convertToWords(salary_annually)

	basic_annual = get_basic_annually(salary_annually)
	house_rent_al_annual = get_house_rent_allowance_annually(salary_annually)
	city_al_annual = get_city_allowance_annually(salary_annually)
	conveyance_al_annual = get_conveyance_allowance_annually(salary_annually)
	children_education_al_annual = get_children_education_allowance_annually(salary_annually)
	medical_al_annual = get_medical_allowance_annually(salary_annually)
	special_al_annual = get_special_allowance_annually(salary_annually)

	gross_salary_annually = get_gross_annually(basic_annual,
		house_rent_al_annual,city_al_annual,
		conveyance_al_annual,children_education_al_annual,
		medical_al_annual,special_al_annual)

	pf_annually = get_pf_annually(salary_annually)
	
	#more tds conditions need to be added.
	tds_annually = get_tds_annually(salary_annually)

	net_payable_salary_annually = get_net_salary_annually(gross_salary_annually,pf_annually,tds_annually)

	context = {
		'name':employee,
		'date':datetime.datetime.now().date,
		'designation':employee.designation,
		'joining_date':employee.joining_date,
		'ctc':salary_annually,

		'basic_annual':basic_annual,
		'house_rent_allowance_annual':house_rent_al_annual,
		'city_allowance_annual':city_al_annual,
		'conveyance_allowance_annual':conveyance_al_annual,
		'children_education_allowance_annual':children_education_al_annual,
		'medical_allowance_annual':medical_al_annual,
		'special_allowance_annual':special_al_annual,

		'basic_monthly':math.floor(basic_annual/12),
		'house_rent_allowance_monthly':math.floor(house_rent_al_annual/12),
		'city_allowance_monthly':math.floor(city_al_annual/12),
		'conveyance_allowance_monthly':math.floor(conveyance_al_annual/12),
		'children_education_allowance_monthly':math.floor(children_education_al_annual/12),
		'medical_allowance_monthly':math.floor(medical_al_annual/12),
		'special_allowance_monthly':math.floor(special_al_annual/12),

		'gross_salary_annually':gross_salary_annually,
		'gross_salary_monthly':math.floor(gross_salary_annually/12),
		
		'words_salary':words_salary,
		'pf_annually':pf_annually,
		'pf_monthly':math.floor(pf_annually/12),
		'tds_annually':tds_annually,
		'tds_monthly':math.floor(tds_annually/12),
		'net_payable_salary_annually':net_payable_salary_annually,
		'net_payable_salary_monthly':math.floor(net_payable_salary_annually/12),

	}
	return render(request,'letter/offer_letter.html',context)