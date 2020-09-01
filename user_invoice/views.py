from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import EmployeeForm, RoleAddForm, RateAddForm
from django.contrib.auth.models import User
from .mixin import AdminOrHRPanelMixin, AdminPanelMixin
from datetime import datetime
from django.core.paginator import Paginator
# Create your views here.

# 3650-8243-248

def index(request):
	user = request.user
	try:
		employee = Employee.objects.get(auth_tbl=user)
		rolename = employee.role.name.lower()
		url = 'fixed'
		if rolename=='ir':
			url = 'ir'
		elif rolename=='br':
			url = 'br'	
		context = {'url':url, 'title':'home', 'role':rolename}	
		return render(request,'user_invoice/home.html',context)
	except:
		return HttpResponseRedirect('/employee/'+str(user.pk))

class RoleDisplayView(AdminOrHRPanelMixin,TemplateView):
    template_name = 'user_invoice/role_list.html'
    def get(self, request):
        context = {
            'roles': Role.objects.all(),
            'title': 'Role list',
            'role' : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
        }
        return render(request, self.template_name, context)



class RoleAddView(AdminOrHRPanelMixin,TemplateView):
    template_name = 'user_invoice/add_role.html'
    def get(self, request):
        role_form = RoleAddForm()
        context = {
            'role_form' : role_form,
            'submit'    : 'Add Role',
            'title'     : 'Add role',
            'role'      : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        role_form = RoleAddForm(request.POST)
        if role_form.is_valid():
            role = role_form.save()
            messages.success(request, "Successfully created new Role")
            return HttpResponseRedirect('/role-list/')
        else:
            print(role_form.errors)
            messages.error(request, "There was a problem adding the role")
            return render(request, self.template_name, {
                'role_form'   : role_form,
                'submit'      : 'Edit Role',
                'title'       : 'Edit role',
                'role'        : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
            })	

class RoleEditView(AdminOrHRPanelMixin,TemplateView):
    template_name = 'user_invoice/add_role.html'
    def get(self, request, pk):
        role = Role.objects.get(id=pk)
        role_form = RoleAddForm(instance=role)
        context = {
            'role_form' : role_form,
            'submit'    : 'Edit Role',
            'title'     : 'Edit role',
            'role'      : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        role = Role.objects.get(id=pk)
        role_form = RoleAddForm(request.POST, instance=role)
        if role_form.is_valid():
            role = role_form.save()
            messages.success(request, "Successfully edited Role")            
            return HttpResponseRedirect('/role-list/')    
        else:
            messages.error(request, "There was a problem updating the role")
            return render(request, self.template_name, {
                'role_form' : role_form,
                'submit'    : 'Edit Role',
                'title'     : 'Edit role',
                'role'      : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
            })


class RateAddView(TemplateView):
    template_name = 'user_invoice/add_rate.html'
    def get(self, request):
        rate_form = RateAddForm()
        context = {
            'rate_form' : rate_form,
            'submit'    : 'Add Rate',
            'title'     : 'Add rate',
            'role'      : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        rate_form = RateAddForm(request.POST)
        print(rate_form)
        if rate_form.is_valid():        	
            rate = rate_form.save()
            rate.added_by = Employee.objects.get(auth_tbl=self.request.user)
            rate.save() 
            messages.success(request, "Successfully created new Rate")
            return HttpResponseRedirect('/rate-list/')
        # else:
        #     messages.error(request, "There was a problem adding the role")
        #     return render(request, self.template_name, {
        #         'rate_form'   : rate_form,
        #         'submit'      : 'Edit Rate',
        #         'title'       : 'Edit rate',
        #         'role'        : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
        #     })	



class EmployeeDisplayView(AdminOrHRPanelMixin,TemplateView):
    template_name = 'user_invoice/employee_list.html'
    def get(self, request):
        employee_list    = Employee.objects.all()
        paginator        = Paginator(employee_list,5)
        page             = request.GET.get('page')
        paginatedcontent = paginator.get_page(page)
        context = {
            'employees' : paginatedcontent,
            'title'     : 'Employee list',
            'role'      : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
        }
        return render(request, self.template_name, context)
    	    

class EmployeeAddView(AdminPanelMixin,TemplateView):
    template_name = 'user_invoice/add_employee.html'
    def get(self, request, user_id):
        user          = User.objects.get(pk=user_id)
        roles         = Role.objects.all()
        try:
        	rolename = Employee.objects.get(auth_tbl=self.request.user).role.name.lower(),
        except:
        	rolename = None	
        # employee_form = EmployeeForm()
        context = {
            # 'employee_form': employee_form,
            'user'         : user,
            'roles'        : roles,
            'submit'       : 'Add Employee',
            'role'         : rolename,
            'title'        : 'Add employee'
        }
        return render(request, self.template_name, context)

    def post(self, request, user_id):
        user     = User.objects.get(pk=user_id)
        name     = request.POST['name']
        role     = Role.objects.get(pk=request.POST['role'])
        salary   = request.POST['salary']
        address  = request.POST['address']
        phone_no = request.POST['phone_no']
        leaves   = request.POST['leaves']
        auth_tbl = user
        employee = Employee.objects.create(name=name, role=role, salary=salary, address=address, phone_no=phone_no, leaves=leaves, auth_tbl=auth_tbl)
        return HttpResponseRedirect('/')

class EmployeeEditView(AdminOrHRPanelMixin,TemplateView):
    template_name = 'user_invoice/add_employee.html'

    def get(self, request, pk):
        employee      = Employee.objects.get(pk=pk)
        roles         = Role.objects.all()        # employee_form = EmployeeForm()
        context = {
            # 'employee_form': employee_form,
            'employee'     : employee,
            'roles'        : roles,
            'submit'       : 'Edit Employee',
            'title'        : 'Edit employee',
            'role'         : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        user              = request.user
        employee          = Employee.objects.get(pk=pk)
        employee.name     = request.POST['name']
        employee.role     = Role.objects.get(pk=request.POST['role'])
        employee.salary   = request.POST['salary']
        employee.address  = request.POST['address']
        employee.phone_no = request.POST['phone_no']
        employee.leaves   = request.POST['leaves']
        employee.save()
        return HttpResponseRedirect('/employee-list')

class InvoiceDisplayView(AdminPanelMixin, TemplateView):
	template_name = 'user_invoice/invoice_list.html'

	def get(self, request):
		employee  =  Employee.objects.get(auth_tbl=self.request.user)
		rolename  =  employee.role.name.lower()
		if rolename == 'admin' or  rolename == 'hr':
			invoice = Invoice.objects.all()
		else:
			invoice = Invoice.objects.filter(emp_ownwer=employee).all()	
		context = {
			'invoices' : invoice,
			'title'    : 'Invoice list',
			'role'     : rolename
		}
		return render(request, self.template_name, context)

class IrEditView(AdminPanelMixin,TemplateView):
	template_name='user_invoice/ir.html'

	def get(self, request, pk):
		invoice  = Invoice.objects.get(pk=pk)
		employee = invoice.emp_ownwer
		rates    = Rate.objects.get(pk=1)
		rolename = employee.role.name.lower()
		context ={
			'employee' : employee,
			'submit'   : 'Edit IR Invoice',
			'title'    : 'Edit ir',
			'role'     : rolename,
			'rates'    : rates,
			'invoice'  : invoice 
		} 
		return render(request, self.template_name, context)
	# def post(self, request,pk):
	# 	invoice =  Invoice.objects.get(pk=pk)
	# 	invoice_date = datetime.strptime(request.POST['invoice_date'], '%Y-%m-%d').date()	
	# 	monthdate    = datetime.strptime(request.POST['monthdate'], '%Y-%m').date()
	# 	invoice.invoice

class IrAddView(AdminPanelMixin,TemplateView):
    template_name='user_invoice/ir.html'

    def get(self, request):
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        rolename      = employee.role.name.lower()
        rates         = Rate.objects.get(pk=1)
        context = {
            'employee'  : employee,
            'submit'    : 'Add IR Invoice',
            'title'     : 'Add ir',
            'role'      : rolename,
            'rates'     : rates,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        print(request.POST)
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        try:
            invoice_date = datetime.strptime(request.POST['invoice_date'], '%Y-%m-%d').date()	
            monthdate    = datetime.strptime(request.POST['monthdate'], '%Y-%m').date()
            invoice = Invoice.objects.create(invoice_date=invoice_date, monthdate=monthdate, emp_type=request.POST['emp_type'], additional_auth_days = request.POST['additional_auth_days'], wds_source_checked_completely = request.POST['wds_source_checked_completely'], new_solicitation_entered_correctly = request.POST['new_solicitation_entered_correctly'], updated_solicitation_by_addenda = request.POST['updated_solicitation_by_addenda'], extra_hours_worked = request.POST['extra_hours_worked'], file_attached = request.POST['file_attached'], difficult_and_nonproductive_source=request.POST['difficult_and_nonproductive_source'], authorised_day_off = request.POST['authorised_day_off'], unauthorised_day_off=request.POST['unauthorised_day_off'], total_working_days = request.POST['total_working_days'], total_days_worked = request.POST['total_days_worked'], duplicate_solic = request.POST['duplicate_solic'], entity_cont_wrong = request.POST['entity_cont_wrong'], false_referal = request.POST['false_referal'], fraudulent_solicitation_update = request.POST['fraudulent_solicitation_update'], source_returned_without_good_res = request.POST['source_returned_without_good_res'], missed_bidbond_and_specs = request.POST['missed_bidbond_and_specs'], missed_categories = request.POST['missed_categories'], missed_solic_or_addend_from_source = request.POST['missed_solic_or_addend_from_source'], missed_incorrect_filetype = request.POST['missed_incorrect_filetype'], missing_or_wrong_outside_link  = request.POST['missing_or_wrong_outside_link'], missing_or_wrong_term_contract = request.POST['missing_or_wrong_term_contract'], not_posted_as_lead = request.POST['not_posted_as_lead'], other_error = request.POST['other_error'], other_serious_error = request.POST['other_serious_error'], refreshing_wds_page_to_diff_source = request.POST['refreshing_wds_page_to_diff_source'], prevailing_wage_not_selected = request.POST['prevailing_wage_not_selected'], skipped_solicitation = request.POST['skipped_solicitation'], source_returned_without_a_note = request.POST['source_returned_without_a_note'], unexcused_unjustified_absence = request.POST['unexcused_unjustified_absence'], wrongbid_prebid_mandatory = request.POST['wrongbid_prebid_mandatory'], wrong_categories = request.POST['wrong_categories'], wrong_geographic_location =  request.POST['wrong_geographic_location'], incomplete_and_incorrect_scope = request.POST['incomplete_and_incorrect_scope'], wrong_text_format = request.POST['wrong_text_format'], total_deduction = request.POST['total_deduction'] , total_payable = request.POST['total_payable'], emp_ownwer = employee)    
            messages.success(request, "Successfully added invoice")   
            return HttpResponseRedirect('/invoice-list/')
        except:
            print("error")
            messages.error(request, "There was a problem adding invoice")
            return HttpResponseRedirect('/ir/')	

class BrEditView(AdminPanelMixin,TemplateView):
	template_name='user_invoice/br.html'

	def get(self, request, pk):
		invoice  = Invoice.objects.get(pk=pk)
		employee = invoice.emp_ownwer
		rates    = Rate.objects.get(pk=1)
		rolename = employee.role.name.lower()
		context ={
			'employee' : employee,
			'submit'   : 'Edit BR Invoice',
			'title'    : 'Edit br',
			'role'     : rolename,
			'rates'    : rates,
			'invoice'  : invoice 
		} 
		return render(request, self.template_name, context) 


class BrAddView(AdminPanelMixin,TemplateView):
    template_name='user_invoice/br.html'

    def get(self, request):
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        rolename      = employee.role.name.lower()
        rates         = Rate.objects.get(pk=1)
        context = {
            'employee'  : employee,
            'submit'    : 'Add BR Invoice',
            'title'     : 'Add br',
            'role'      : rolename,
            'rates'     : rates,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        print(request.POST)
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        try:
            invoice_date = datetime.strptime(request.POST['invoice_date'], '%Y-%m-%d').date()	
            monthdate    = datetime.strptime(request.POST['monthdate'], '%Y-%m').date()
            invoice = Invoice.objects.create(invoice_date=invoice_date, monthdate=monthdate, emp_type=request.POST['emp_type'], new_entities_added=request.POST['new_entities_added'], ph_added_to_bid_list=request.POST['ph_added_to_bid_list'], ph_edited_in_bid_list=request.POST['ph_edited_in_bid_list'], ph_deleted_in_bid_list=request.POST['ph_deleted_in_bid_list'], extra_days_worked=request.POST['extra_days_worked'], authorised_day_off=request.POST['authorised_day_off'], unauthorised_day_off=request.POST['unauthorised_day_off'], duplicate_entities=request.POST['duplicate_entities'],errors=request.POST['errors'],fines=request.POST['fines'], total_deduction=request.POST['total_deduction'], total_payable=request.POST['total_payable'])
            messages.success(request, "Successfully added invoice")   
            return HttpResponseRedirect('/br/')
        except:
            print("error")
            messages.error(request, "There was a problem adding invoice")
            return HttpResponseRedirect('/br/')	  

class FixedAddView(AdminPanelMixin,TemplateView):
    template_name='user_invoice/fixed.html'

    def get(self, request):
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        rolename      = employee.role.name.lower()
        rates         = Rate.objects.get(pk=1)
        context = {
            'employee'  : employee,
            'submit'    : 'Add IR Invoice',
            'title'     : 'Add ir',
            'role'      : rolename,
            'rates'     : rates,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        print(request.POST)
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        try:
            invoice_date = datetime.strptime(request.POST['invoice_date'], '%Y-%m-%d').date()	
            monthdate    = datetime.strptime(request.POST['monthdate'], '%Y-%m').date()
            invoice = Invoice.objects.create(invoice_date=invoice_date, monthdate=monthdate, total_pay=request.POST['total_pay'], authorised_day_off = request.POST['authorised_day_off'], unauthorised_day_off=request.POST['unauthorised_day_off'], total_working_days = request.POST['total_working_days'], total_days_worked = request.POST['total_days_worked'], duplicate_solic = request.POST['duplicate_solic'], entity_cont_wrong = request.POST['entity_cont_wrong'], false_referal = request.POST['false_referal'], fraudulent_solicitation_update = request.POST['fraudulent_solicitation_update'], source_returned_without_good_res = request.POST['source_returned_without_good_res'], missed_bidbond_and_specs = request.POST['missed_bidbond_and_specs'], missed_categories = request.POST['missed_categories'], missed_solic_or_addend_from_source = request.POST['missed_solic_or_addend_from_source'], missed_incorrect_filetype = request.POST['missed_incorrect_filetype'], missing_or_wrong_outside_link  = request.POST['missing_or_wrong_outside_link'], missing_or_wrong_term_contract = request.POST['missing_or_wrong_term_contract'], not_posted_as_lead = request.POST['not_posted_as_lead'], other_error = request.POST['other_error'], other_serious_error = request.POST['other_serious_error'], refreshing_wds_page_to_diff_source = request.POST['refreshing_wds_page_to_diff_source'], prevailing_wage_not_selected = request.POST['prevailing_wage_not_selected'], skipped_solicitation = request.POST['skipped_solicitation'], source_returned_without_a_note = request.POST['source_returned_without_a_note'], unexcused_unjustified_absence = request.POST['unexcused_unjustified_absence'], wrongbid_prebid_mandatory = request.POST['wrongbid_prebid_mandatory'], wrong_categories = request.POST['wrong_categories'], wrong_geographic_location =  request.POST['wrong_geographic_location'], incomplete_and_incorrect_scope = request.POST['incomplete_and_incorrect_scope'], wrong_text_format = request.POST['wrong_text_format'], total_deduction = request.POST['total_deduction'] , total_payable = request.POST['total_payable'], emp_ownwer = employee)    
            messages.success(request, "Successfully added invoice")   
            return HttpResponseRedirect('/invoice-list/')
        except:
            print("error")
            messages.error(request, "There was a problem adding invoice")
            return HttpResponseRedirect('/fixed/')

class FixedEditView(AdminPanelMixin, TemplateView):
	template_name='user_invoice/fixed.html'

	def get(self, request, pk):
		invoice  = Invoice.objects.get(pk=pk)
		employee = invoice.emp_ownwer
		rates    = Rate.objects.get(pk=1)
		rolename = employee.role.name.lower()
		context ={
			'employee' : employee,
			'submit'   : 'Edit Fixed Invoice',
			'title'    : 'Edit fixed',
			'role'     : rolename,
			'rates'    : rates,
			'invoice'  : invoice 
		} 
		return render(request, self.template_name, context) 
            