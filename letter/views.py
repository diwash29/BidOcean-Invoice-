from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
import math
import datetime
from .converter import convertToWords
from .utils import *
# Create your views here.

def generate_pdf(request):
	salary_annually = 480000
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
	tds_annually = get_tds_annually(salary_annually)

	net_payable_salary_annually = get_net_salary_annually(gross_salary_annually,pf_annually,tds_annually)

	context = {
		'name':'Name',
		'date':datetime.datetime.now().date,
		'designation':'Designation',
		'joining_date':'Date of Joining',
		'ctc':'Amount CTC',

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
	return render(request,'letter/invoice.html',context)