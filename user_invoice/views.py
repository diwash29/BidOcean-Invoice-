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
from leave.models import LeaveRequest
from .mixin import AdminOrHRPanelMixin, AdminPanelMixin, IRPanelMixin, BRPanelMixin, FixedPanelMixin
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q
from leave.models import LeaveBalance
from .utils import get_first_n_last_day, count_leaves, check_invoice
# Create your views here.

# 3650-8243-248
@login_required(login_url='/login/')
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
        	'selected_role' : role,
            'role_form'     : role_form,
            'submit'        : 'Edit Role',
            'title'         : 'Edit role',
            'role'          : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
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


class RateDisplayView(AdminOrHRPanelMixin,TemplateView):
    template_name = "user_invoice/rate_list.html"
    def get(self, request):
        employee = Employee.objects.get(auth_tbl=self.request.user)
        role     = employee.role.name.lower()
        context = {
            'role'     : role,
            'rates'    : Rate.objects.all(),
            'title'    : 'Rate list', 
            'employee' : employee
        }
        return render(request, self.template_name, context)

class RateApproveView(AdminOrHRPanelMixin, TemplateView):
    def get(self, request,pk):
        Rate.objects.all().update(is_approved=0)
        rate = Rate.objects.get(pk=pk)
        rate.is_approved = 1
        rate.save()
        #messages.success(request, "Successfully deleted employee") 
        return HttpResponseRedirect('/rate-list')



class RatePullView(AdminOrHRPanelMixin, TemplateView):
    template_name = 'user_invoice/add_rate.html'
    def get(self, request, pk):
        rate = Rate.objects.get(pk=pk)
        context ={
            'submit' : 'Push Rate',
            'title'  : 'Push rate',
            'role'   : Employee.objects.get(auth_tbl=self.request.user).role.name.lower(),
            'rate'   : rate
        }
        return render(request, self.template_name, context)   
    def post(self, request, pk):
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        try:
            Rate.objects.all().update(is_approved=0)
            rate = Rate.objects.create(base_ir=request.POST['base_ir'], base_br=request.POST['base_br'], total_pay=request.POST['total_pay'], difficultnp=request.POST['difficultnp'], extra_hours=request.POST['extra_hours'], file_attach=request.POST['file_attach'], add_auth_days=request.POST['add_auth_days'], new_entities_added=request.POST['new_entities_added'], extra_days=request.POST['extra_days'], duplicate_entities=request.POST['duplicate_entities'], errors=request.POST['errors'], fines=request.POST['fines'], duplicate_solic=request.POST['duplicate_solic'], entity_cont_wrong= request.POST['entity_cont_wrong'], false_referal=request.POST['false_referal'], fraudsolic_update=request.POST['fraudsolic_update'], source_ret_wo_res=request.POST['source_ret_wo_res'], missed_bond=request.POST['missed_bond'], missed_categories=request.POST['missed_categories'], missed_solic_src=request.POST['missed_solic_src'], missed_file=request.POST['missed_file'], missed_link=request.POST['missed_link'], missed_term=request.POST['missed_term'], not_posted_lead=request.POST['not_posted_lead'], other_error=request.POST['other_error'], other_serious_err=request.POST['other_serious_err'], refreshing_wds=request.POST['refreshing_wds'], wage_not_selected=request.POST['wage_not_selected'], skipped_solic=request.POST['skipped_solic'], source_ret_wo_note=request.POST['source_ret_wo_note'], unjustified_absence=request.POST['unjustified_absence'], wrong_pre_bid=request.POST['wrong_pre_bid'], wrong_categories=request.POST['wrong_categories'], wrong_geo_location=request.POST['wrong_geo_location'], incorrect_scope=request.POST['incorrect_scope'], wrong_text_format=request.POST['wrong_text_format'], auth_day_off=request.POST['auth_day_off'], unauth_day_off=request.POST['unauth_day_off'], added_by=employee, is_approved=1)
            messages.success(request, "Successfully added rate")   
            return HttpResponseRedirect('/rate-list/')
        except:
            print("error")
            messages.error(request, "There was a problem adding rate")
        return HttpResponseRedirect('/rate-pull/'+pk)
              


class RateEditView(AdminOrHRPanelMixin,TemplateView):
    template_name = 'user_invoice/add_rate.html'
    def get(self, request, pk):
        rate = Rate.objects.get(pk=pk)
        context ={
            'submit' : 'Edit Rate',
            'title'  : 'Edit rate',
            'role'   : Employee.objects.get(auth_tbl=self.request.user).role.name.lower(),
            'rate'   : rate
        }   
        return render(request, self.template_name, context)   
    def post(self, request, pk):
        rate = Rate.objects.get(pk=pk)
        Rate.objects.all().update(is_approved=0)
        try:
            rate.base_ir            = request.POST['base_ir']
            rate.base_br            = request.POST['base_br']
            rate.total_pay          = request.POST['total_pay']
            rate.difficultnp        = request.POST['difficultnp']
            rate.extra_hours        = request.POST['extra_hours']
            rate.file_attach        = request.POST['file_attach']
            rate.add_auth_days      = request.POST['add_auth_days']
            rate.new_entities_added = request.POST['new_entities_added']
            rate.extra_days         = request.POST['extra_days']
            rate.duplicate_entities = request.POST['duplicate_entities']
            rate.errors             = request.POST['errors']
            rate.fines              = request.POST['fines']
            rate.duplicate_solic    = request.POST['duplicate_solic']
            rate.entity_cont_wrong  = request.POST['entity_cont_wrong']
            rate.false_referal      = request.POST['false_referal']
            rate.fraudsolic_update  = request.POST['fraudsolic_update']
            rate.source_ret_wo_res  = request.POST['source_ret_wo_res']
            rate.missed_bond        = request.POST['missed_bond']
            rate.missed_categories  = request.POST['missed_categories']
            rate.missed_solic_src   = request.POST['missed_solic_src']
            rate.missed_file        = request.POST['missed_file']
            rate.missed_link        = request.POST['missed_link']
            rate.missed_term        = request.POST['missed_term']
            rate.not_posted_lead    = request.POST['not_posted_lead']
            rate.other_error        = request.POST['other_error']
            rate.other_serious_err  = request.POST['other_serious_err']
            rate.refreshing_wds     = request.POST['refreshing_wds']
            rate.wage_not_selected  = request.POST['wage_not_selected']
            rate.skipped_solic      = request.POST['skipped_solic']
            rate.source_ret_wo_note = request.POST['source_ret_wo_note']
            rate.unjustified_absence= request.POST['unjustified_absence']
            rate.wrong_pre_bid      = request.POST['wrong_pre_bid']
            rate.wrong_categories   = request.POST['wrong_categories']
            rate.wrong_geo_location = request.POST['wrong_geo_location']
            rate.incorrect_scope    = request.POST['incorrect_scope']
            rate.wrong_text_format  = request.POST['wrong_text_format']
            rate.auth_day_off       = request.POST['auth_day_off']
            rate.unauth_day_off     = request.POST['unauth_day_off']
            rate.is_approved        = 1
            rate.save()
            messages.success(request, "Successfully edited rate")   
            return HttpResponseRedirect('/rate-list/')
        except:
            print("error")
            messages.error(request, "There was a problem adding rate")
        return HttpResponseRedirect('/rate-edit/'+pk)    


class RateAddView(AdminOrHRPanelMixin,TemplateView):
    template_name = 'user_invoice/add_rate.html'
    def get(self, request):
        # rate_form = RateAddForm()
        context = {
            # 'rate_form' : rate_form,
            'submit'    : 'Add Rate',
            'title'     : 'Add rate',
            'role'      : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        print(request.POST)
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        try:
            Rate.objects.all().update(is_approved=0)
            rate = Rate.objects.create(base_ir=request.POST['base_ir'], base_br=request.POST['base_br'], total_pay=request.POST['total_pay'], difficultnp=request.POST['difficultnp'], extra_hours=request.POST['extra_hours'], file_attach=request.POST['file_attach'], add_auth_days=request.POST['add_auth_days'], new_entities_added=request.POST['new_entities_added'], extra_days=request.POST['extra_days'], duplicate_entities=request.POST['duplicate_entities'], errors=request.POST['errors'], fines=request.POST['fines'], duplicate_solic=request.POST['duplicate_solic'], entity_cont_wrong= request.POST['entity_cont_wrong'], false_referal=request.POST['false_referal'], fraudsolic_update=request.POST['fraudsolic_update'], source_ret_wo_res=request.POST['source_ret_wo_res'], missed_bond=request.POST['missed_bond'], missed_categories=request.POST['missed_categories'], missed_solic_src=request.POST['missed_solic_src'], missed_file=request.POST['missed_file'], missed_link=request.POST['missed_link'], missed_term=request.POST['missed_term'], not_posted_lead=request.POST['not_posted_lead'], other_error=request.POST['other_error'], other_serious_err=request.POST['other_serious_err'], refreshing_wds=request.POST['refreshing_wds'], wage_not_selected=request.POST['wage_not_selected'], skipped_solic=request.POST['skipped_solic'], source_ret_wo_note=request.POST['source_ret_wo_note'], unjustified_absence=request.POST['unjustified_absence'], wrong_pre_bid=request.POST['wrong_pre_bid'], wrong_categories=request.POST['wrong_categories'], wrong_geo_location=request.POST['wrong_geo_location'], incorrect_scope=request.POST['incorrect_scope'], wrong_text_format=request.POST['wrong_text_format'], auth_day_off=request.POST['auth_day_off'], unauth_day_off=request.POST['unauth_day_off'], added_by=employee, is_approved=1)
            messages.success(request, "Successfully added rate")   
            return HttpResponseRedirect('/rate-list/')
        except:
            print("error")
            messages.error(request, "There was a problem adding rate")
        return HttpResponseRedirect('/rate-add/')


        



class EmployeeDisplayView(AdminOrHRPanelMixin,TemplateView):
    template_name = 'user_invoice/employee_list.html'
    def get(self, request):
        employee_list    = Employee.objects.all()
        try:
            search     = request.GET['search']
        except:
            search     = None
        try:
            role     = request.GET['role']
        except:
            role     = None  
        query_param = {}     
        if search is not None and search is not "":
            search = search.strip()
            query_param['search'] = search
            employee_list = employee_list.filter(Q(name__icontains=search)|Q(address__icontains=search)|(Q(phone_no__icontains=search))|Q(emp_id__icontains=search)) 
        if role is not None and role is not "":
            query_param['role'] = role
            employee_list = employee_list.filter(role__pk__exact=role)
        # print(employee_list.query)	
        		    
        
        roles            = Role.objects.all()
        paginator        = Paginator(employee_list,10)
        page             = request.GET.get('page')
        paginatedcontent = paginator.get_page(page)
        context = {
            'query_param' : query_param, 
            'employees'   : paginatedcontent,
            'title'       : 'Employee list',
            'roles'       : roles,    
            'role'        : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
        }
        return render(request, self.template_name, context)
    	    

class EmployeeAddView(AdminPanelMixin,TemplateView):
    template_name = 'user_invoice/add_employee.html'
    def get(self, request, user_id):
        user          = Userdetail.objects.get(pk=user_id)
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
        user     = Userdetail.objects.get(pk=user_id)
        name     = request.POST['name']
        role     = Role.objects.get(pk=request.POST['role'])
        salary   = request.POST['salary']
        address  = request.POST['address']
        phone_no = request.POST['phone_no']
        emp_id   = request.POST['emp_id']
        leaves   = request.POST['leaves']
        auth_tbl = user
        employee = Employee.objects.create(name=name, role=role, salary=salary, address=address, phone_no=phone_no, emp_id=emp_id, leaves=leaves, auth_tbl=auth_tbl)
        leave_bal = LeaveBalance.objects.create(casual_leave=3, sick_leave=3, earned_leave=4, employee=employee)

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
        employee.emp_id   = request.POST['emp_id']
        employee.save()
        return HttpResponseRedirect('/employee-list')

class EmployeeDeleteView(AdminPanelMixin, View):
	def get(self, request, pk):
		employee = Employee.objects.get(pk=pk)
		print(employee)
		employee.delete()
		messages.success(request, "Successfully deleted employee") 
		return HttpResponseRedirect('/employee-list')

class RoleDeleteView(AdminPanelMixin, TemplateView):
	def get(self, request, pk):
		role = Role.objects.get(pk=pk)
		role.delete()
		messages.success(request, "Successfully deleted role")
		return HttpResponseRedirect('/role-list') 		  


class InvoiceDisplayView(AdminPanelMixin, TemplateView):
    template_name = 'user_invoice/invoice_list.html'

    def get(self, request):
        employee  =  Employee.objects.get(auth_tbl=self.request.user)
        rolename  =  employee.role.name.lower()
        if rolename == 'admin' or  rolename == 'hr':
            invoice = Invoice.objects.all()
        else:
            invoice = Invoice.objects.filter(emp_ownwer=employee).all()	

        search        = request.GET.get('search', None)
        from_date     = request.GET.get('from_date', None)
        to_date       = request.GET.get('to_date', None)
        bank          = request.GET.get('bank',None)
        
        query_param = {}  
        if search is not None and search is not '':
            search = search.strip()
            query_param['search'] = search 
            invoice = invoice.filter(Q(emp_ownwer__name__icontains=search)|Q(emp_ownwer__address__icontains=search)|(Q(emp_ownwer__phone_no__icontains=search))|Q(emp_ownwer__emp_id__icontains=search)) 
        if (from_date is not None and to_date is not None) and (from_date != "" and to_date != ""):
            query_param['from_date'] = from_date
            query_param['to_date']   = to_date
            to_date   = datetime.strptime(to_date,"%Y-%m-%d").date()
            from_date = datetime.strptime(from_date,"%Y-%m-%d").date()	
            invoice   = invoice.filter(invoice_date__gte=from_date, invoice_date__lte=to_date)
        if bank is not None and bank is not '':
            query_param['bank'] = bank
            invoice = invoice.filter(bank_account__bank__iexact=bank)

        invoice = invoice.order_by('-invoice_date')    

        paginator        = Paginator(invoice,10)
        page             = request.GET.get('page')
        paginatedcontent = paginator.get_page(page)	
        print(query_param)
        context = {
            'query_param' : query_param,
            'invoices'    : paginatedcontent,
            'title'       : 'Invoice list',
            'role'        : rolename
        }
        return render(request, self.template_name, context)

class IrEditView(IRPanelMixin,TemplateView):
    template_name='user_invoice/ir.html'

    def get(self, request, pk):
        invoice  = Invoice.objects.get(pk=pk)
        employee = invoice.emp_ownwer
        rates    = invoice.rate
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
    def post(self, request, pk):
        invoice = Invoice.objects.get(pk=pk)
        try:
            bank_account = None
            if 'bank_account' in request.POST:
                bank_account = AccountDetails.objects.get(pk=request.POST['bank_account'])
            invoice_date = datetime.strptime(request.POST['invoice_date'], '%Y-%m-%d').date()   
            monthdate    = datetime.strptime(request.POST['monthdate'], '%Y-%m').date()
            invoice.invoice_date                       = invoice_date
            invoice.monthdate                          = monthdate
            invoice.emp_type                           = request.POST['emp_type']
            invoice.bank_account                       = bank_account
            invoice.additional_auth_days               = request.POST['additional_auth_days']
            invoice.wds_source_checked_completely      = request.POST['wds_source_checked_completely']
            invoice.new_solicitation_entered_correctly = request.POST['new_solicitation_entered_correctly']
            invoice.updated_solicitation_by_addenda    = request.POST['updated_solicitation_by_addenda']
            invoice.extra_hours_worked                 = request.POST['extra_hours_worked']
            invoice.file_attached                      = request.POST['file_attached']
            invoice.difficult_and_nonproductive_source = request.POST['difficult_and_nonproductive_source'] 
            invoice.authorised_day_off                 = request.POST['authorised_day_off']
            invoice.unauthorised_day_off               = request.POST['unauthorised_day_off']
            invoice.total_working_days                 = request.POST['total_working_days']
            invoice.total_days_worked                  = request.POST['total_days_worked']
            invoice.duplicate_solic                    = request.POST['duplicate_solic']
            invoice.entity_cont_wrong                  = request.POST['entity_cont_wrong']
            invoice.false_referal                      = request.POST['false_referal']
            invoice.fraudulent_solicitation_update     = request.POST['fraudulent_solicitation_update']
            invoice.source_returned_without_good_res   = request.POST['source_returned_without_good_res']
            invoice.missed_bidbond_and_specs           = request.POST['missed_bidbond_and_specs']
            invoice.missed_categories                  = request.POST['missed_categories']
            invoice.missed_solic_or_addend_from_source = request.POST['missed_solic_or_addend_from_source']
            invoice.missed_incorrect_filetype          = request.POST['missed_incorrect_filetype']
            invoice.missing_or_wrong_outside_link      = request.POST['missing_or_wrong_outside_link']
            invoice.missing_or_wrong_term_contract     = request.POST['missing_or_wrong_term_contract']
            invoice.not_posted_as_lead                 = request.POST['not_posted_as_lead']
            invoice.other_error                        = request.POST['other_error']
            invoice.other_serious_error                = request.POST['other_serious_error']
            invoice.refreshing_wds_page_to_diff_source = request.POST['refreshing_wds_page_to_diff_source']
            invoice.prevailing_wage_not_selected       = request.POST['prevailing_wage_not_selected']
            invoice.skipped_solicitation               = request.POST['skipped_solicitation']
            invoice.source_returned_without_a_note     = request.POST['source_returned_without_a_note']
            invoice.unexcused_unjustified_absence      = request.POST['unexcused_unjustified_absence']
            invoice.wrongbid_prebid_mandatory          = request.POST['wrongbid_prebid_mandatory']
            invoice.wrong_categories                   = request.POST['wrong_categories']
            invoice.wrong_geographic_location          = request.POST['wrong_geographic_location']
            invoice.incomplete_and_incorrect_scope     = request.POST['incomplete_and_incorrect_scope']
            invoice.wrong_text_format                  = request.POST['wrong_text_format']
            invoice.total_deduction                    = request.POST['total_deduction']
            invoice.total_payable                      = request.POST['total_payable']
            invoice.save()
            messages.success(request, "Successfully edited invoice")   
            return HttpResponseRedirect('/invoice-list/')
        except:
            print("error")
            messages.error(request, "There was a problem editing invoice")
            return HttpResponseRedirect('/ir/') 



            

	# def post(self, request,pk):
	# 	invoice =  Invoice.objects.get(pk=pk)
	# 	invoice_date = datetime.strptime(request.POST['invoice_date'], '%Y-%m-%d').date()	
	# 	monthdate    = datetime.strptime(request.POST['monthdate'], '%Y-%m').date()
	# 	invoice.invoice

class IrAddView(IRPanelMixin,TemplateView):
    template_name='user_invoice/ir.html'

    def get(self, request):
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        ch_invoice    = check_invoice(employee)
        if ch_invoice is None:
            rolename      = employee.role.name.lower()
            rates         = Rate.objects.get(is_approved=1)
            leaves        = count_leaves(employee)
            context = {
                'employee'  : employee,
                'submit'    : 'Add IR Invoice',
                'title'     : 'Add ir',
                'role'      : rolename,
                'rates'     : rates,
                'auth_leave': leaves,
            }
            return render(request, self.template_name, context)
        else:
             return HttpResponseRedirect('/ir/'+str(ch_invoice))   

    def post(self, request):
        print(request.POST)
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        rate          = Rate.objects.get(is_approved =1)
        try:
            bank_account = None
            if 'bank_account' in request.POST:
                bank_account = AccountDetails.objects.get(pk=request.POST['bank_account'])
            invoice_date = datetime.strptime(request.POST['invoice_date'], '%Y-%m-%d').date()	
            monthdate    = datetime.strptime(request.POST['monthdate'], '%Y-%m').date()
            invoice = Invoice.objects.create(invoice_date=invoice_date, monthdate=monthdate, emp_type=request.POST['emp_type'], bank_account=bank_account, additional_auth_days = request.POST['additional_auth_days'], wds_source_checked_completely = request.POST['wds_source_checked_completely'], new_solicitation_entered_correctly = request.POST['new_solicitation_entered_correctly'], updated_solicitation_by_addenda = request.POST['updated_solicitation_by_addenda'], extra_hours_worked = request.POST['extra_hours_worked'], file_attached = request.POST['file_attached'], difficult_and_nonproductive_source=request.POST['difficult_and_nonproductive_source'], authorised_day_off = request.POST['authorised_day_off'], unauthorised_day_off=request.POST['unauthorised_day_off'], total_working_days = request.POST['total_working_days'], total_days_worked = request.POST['total_days_worked'], duplicate_solic = request.POST['duplicate_solic'], entity_cont_wrong = request.POST['entity_cont_wrong'], false_referal = request.POST['false_referal'], fraudulent_solicitation_update = request.POST['fraudulent_solicitation_update'], source_returned_without_good_res = request.POST['source_returned_without_good_res'], missed_bidbond_and_specs = request.POST['missed_bidbond_and_specs'], missed_categories = request.POST['missed_categories'], missed_solic_or_addend_from_source = request.POST['missed_solic_or_addend_from_source'], missed_incorrect_filetype = request.POST['missed_incorrect_filetype'], missing_or_wrong_outside_link  = request.POST['missing_or_wrong_outside_link'], missing_or_wrong_term_contract = request.POST['missing_or_wrong_term_contract'], not_posted_as_lead = request.POST['not_posted_as_lead'], other_error = request.POST['other_error'], other_serious_error = request.POST['other_serious_error'], refreshing_wds_page_to_diff_source = request.POST['refreshing_wds_page_to_diff_source'], prevailing_wage_not_selected = request.POST['prevailing_wage_not_selected'], skipped_solicitation = request.POST['skipped_solicitation'], source_returned_without_a_note = request.POST['source_returned_without_a_note'], unexcused_unjustified_absence = request.POST['unexcused_unjustified_absence'], wrongbid_prebid_mandatory = request.POST['wrongbid_prebid_mandatory'], wrong_categories = request.POST['wrong_categories'], wrong_geographic_location =  request.POST['wrong_geographic_location'], incomplete_and_incorrect_scope = request.POST['incomplete_and_incorrect_scope'], wrong_text_format = request.POST['wrong_text_format'], total_deduction = request.POST['total_deduction'] , total_payable = request.POST['total_payable'], emp_ownwer = employee, rate=rate)    
            messages.success(request, "Successfully added invoice")   
            return HttpResponseRedirect('/invoice-list/')
        except:
            print("error")
            messages.error(request, "There was a problem adding invoice")
            return HttpResponseRedirect('/ir/')	

class BrEditView(BRPanelMixin,TemplateView):
    template_name='user_invoice/br.html'

    def get(self, request, pk):
        invoice  = Invoice.objects.get(pk=pk)
        employee = invoice.emp_ownwer
        rates    = invoice.rate
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
    def post(self, request, pk):
        invoice = Invoice.objects.get(pk=pk)
        try:
            bank_account = None
            if 'bank_account' in request.POST:
                bank_account = AccountDetails.objects.get(pk=request.POST['bank_account'])
            invoice_date = datetime.strptime(request.POST['invoice_date'], '%Y-%m-%d').date()   
            monthdate    = datetime.strptime(request.POST['monthdate'], '%Y-%m').date()
            invoice.invoice_date           = invoice_date
            invoice.monthdate              = monthdate
            invoice.bank_account           = bank_account
            invoice.emp_type               = request.POST['emp_type']
            invoice.new_entities_added     = request.POST['new_entities_added']
            invoice.ph_added_to_bid_list   = request.POST['ph_added_to_bid_list']
            invoice.ph_edited_in_bid_list  = request.POST['ph_edited_in_bid_list']
            invoice.ph_deleted_in_bid_list = request.POST['ph_deleted_in_bid_list']
            invoice.extra_days_worked      = request.POST['extra_days_worked']
            invoice.total_working_days     = request.POST['total_working_days']
            invoice.total_days_worked      = request.POST['total_days_worked']
            invoice.authorised_day_off     = request.POST['authorised_day_off']
            invoice.unauthorised_day_off   = request.POST['unauthorised_day_off']
            invoice.duplicate_entities     = request.POST['duplicate_entities']
            invoice.errors                 = request.POST['errors']
            invoice.fines                  = request.POST['fines']
            invoice.total_deduction        = request.POST['total_deduction']
            invoice.total_payable          = request.POST['total_payable']
            invoice.save()
            messages.success(request, "Successfully edited invoice")   
            return HttpResponseRedirect('/invoice-list/')
        except:
            print("error")
            messages.error(request, "There was a problem editing invoice")
            return HttpResponseRedirect('/br/')   


            


class BrAddView(BRPanelMixin,TemplateView):
    template_name='user_invoice/br.html'

    def get(self, request):
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        ch_invoice    = check_invoice(employee)
        if ch_invoice is None:
            rolename      = employee.role.name.lower()
            leaves        = count_leaves(employee)
            rates         = Rate.objects.get(is_approved=1)
            context = {
                'employee'  : employee,
                'submit'    : 'Add BR Invoice',
                'title'     : 'Add br',
                'role'      : rolename,
                'rates'     : rates,
                'auth_leave': leaves,
            }
            return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect('/br/'+str(ch_invoice))     

    def post(self, request):
        print(request.POST)
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        rate          = Rate.objects.get(is_approved=1)
        try:
            bank_account = None
            if 'bank_account' in request.POST:
                bank_account = AccountDetails.objects.get(pk=request.POST['bank_account'])
            invoice_date = datetime.strptime(request.POST['invoice_date'], '%Y-%m-%d').date()	
            monthdate    = datetime.strptime(request.POST['monthdate'], '%Y-%m').date()
            invoice = Invoice.objects.create(invoice_date=invoice_date, monthdate=monthdate, bank_account=bank_account, emp_type=request.POST['emp_type'], new_entities_added=request.POST['new_entities_added'], ph_added_to_bid_list=request.POST['ph_added_to_bid_list'], ph_edited_in_bid_list=request.POST['ph_edited_in_bid_list'], ph_deleted_in_bid_list=request.POST['ph_deleted_in_bid_list'], extra_days_worked=request.POST['extra_days_worked'], total_working_days=request.POST['total_working_days'], total_days_worked=request.POST['total_days_worked'], authorised_day_off=request.POST['authorised_day_off'], unauthorised_day_off=request.POST['unauthorised_day_off'], duplicate_entities=request.POST['duplicate_entities'],errors=request.POST['errors'],fines=request.POST['fines'], total_deduction=request.POST['total_deduction'], total_payable=request.POST['total_payable'],emp_ownwer=employee, rate=rate)
            messages.success(request, "Successfully added invoice")   
            return HttpResponseRedirect('/invoice-list/')
        except:
            print("error")
            messages.error(request, "There was a problem adding invoice")
            return HttpResponseRedirect('/br/')	  

class FixedAddView(FixedPanelMixin,TemplateView):
    template_name='user_invoice/fixed.html'

    def get(self, request):        
        user           = self.request.user
        employee       = Employee.objects.get(auth_tbl=user)  
        ch_invoice     = check_invoice(employee)    
        if ch_invoice is None:  
            leaves         = count_leaves(employee)
            rolename       = employee.role.name.lower()
            rates          = Rate.objects.get(is_approved=1)
            context = {
                'employee'  : employee,
                'submit'    : 'Add IR Invoice',
                'title'     : 'Add ir',
                'role'      : rolename,
                'rates'     : rates,
                'auth_leave': leaves,
            }
            return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect('/fixed/'+str(ch_invoice))
                

    def post(self, request):
        print(request.POST)
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        rate          = Rate.objects.get(is_approved=1)
        try:
            bank_account = None
            if 'bank_account' in request.POST:
                bank_account = AccountDetails.objects.get(pk=request.POST['bank_account'])
            invoice_date = datetime.strptime(request.POST['invoice_date'], '%Y-%m-%d').date()	
            monthdate    = datetime.strptime(request.POST['monthdate'], '%Y-%m').date()
            invoice = Invoice.objects.create(invoice_date=invoice_date, monthdate=monthdate, bank_account=bank_account, total_pay=request.POST['total_pay'], authorised_day_off = request.POST['authorised_day_off'], unauthorised_day_off=request.POST['unauthorised_day_off'], total_working_days = request.POST['total_working_days'], total_days_worked = request.POST['total_days_worked'], duplicate_solic = request.POST['duplicate_solic'], entity_cont_wrong = request.POST['entity_cont_wrong'], false_referal = request.POST['false_referal'], fraudulent_solicitation_update = request.POST['fraudulent_solicitation_update'], source_returned_without_good_res = request.POST['source_returned_without_good_res'], missed_bidbond_and_specs = request.POST['missed_bidbond_and_specs'], missed_categories = request.POST['missed_categories'], missed_solic_or_addend_from_source = request.POST['missed_solic_or_addend_from_source'], missed_incorrect_filetype = request.POST['missed_incorrect_filetype'], missing_or_wrong_outside_link  = request.POST['missing_or_wrong_outside_link'], missing_or_wrong_term_contract = request.POST['missing_or_wrong_term_contract'], not_posted_as_lead = request.POST['not_posted_as_lead'], other_error = request.POST['other_error'], other_serious_error = request.POST['other_serious_error'], refreshing_wds_page_to_diff_source = request.POST['refreshing_wds_page_to_diff_source'], prevailing_wage_not_selected = request.POST['prevailing_wage_not_selected'], skipped_solicitation = request.POST['skipped_solicitation'], source_returned_without_a_note = request.POST['source_returned_without_a_note'], unexcused_unjustified_absence = request.POST['unexcused_unjustified_absence'], wrongbid_prebid_mandatory = request.POST['wrongbid_prebid_mandatory'], wrong_categories = request.POST['wrong_categories'], wrong_geographic_location =  request.POST['wrong_geographic_location'], incomplete_and_incorrect_scope = request.POST['incomplete_and_incorrect_scope'], wrong_text_format = request.POST['wrong_text_format'], total_deduction = request.POST['total_deduction'] , total_payable = request.POST['total_payable'], emp_ownwer = employee, rate=rate)    
            messages.success(request, "Successfully added invoice")   
            return HttpResponseRedirect('/invoice-list/')
        except:
            print("error")
            messages.error(request, "There was a problem adding invoice")
            return HttpResponseRedirect('/fixed/')

class FixedEditView(FixedPanelMixin, TemplateView):
    template_name='user_invoice/fixed.html'

    def get(self, request, pk):
        invoice  = Invoice.objects.get(pk=pk)
        employee = invoice.emp_ownwer
        rates    = invoice.rate
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

    def post(self,request,pk):
        print(request.POST)
        invoice = Invoice.objects.get(pk=pk)
        try:
            bank_account = None
            if 'bank_account' in request.POST:
                bank_account = AccountDetails.objects.get(pk=request.POST['bank_account'])
            invoice_date = datetime.strptime(request.POST['invoice_date'], '%Y-%m-%d').date()   
            monthdate    = datetime.strptime(request.POST['monthdate'], '%Y-%m').date()
            invoice.invoice_date                       = invoice_date
            invoice.monthdate                          = monthdate
            invoice.bank_account                       = bank_account
            invoice.total_pay                          = request.POST['total_pay']
            invoice.authorised_day_off                 = request.POST['authorised_day_off']
            invoice.unauthorised_day_off               = request.POST['unauthorised_day_off']
            invoice.total_working_days                 = request.POST['total_working_days']
            invoice.total_days_worked                  = request.POST['total_days_worked']
            invoice.duplicate_solic                    = request.POST['duplicate_solic']
            invoice.entity_cont_wrong                  = request.POST['entity_cont_wrong']
            invoice.false_referal                      = request.POST['false_referal']
            invoice.fraudulent_solicitation_update     = request.POST['fraudulent_solicitation_update']
            invoice.source_returned_without_good_res   = request.POST['source_returned_without_good_res']
            invoice.missed_bidbond_and_specs           = request.POST['missed_bidbond_and_specs']
            invoice.missed_categories                  = request.POST['missed_categories']
            invoice.missed_solic_or_addend_from_source = request.POST['missed_solic_or_addend_from_source']
            invoice.missed_incorrect_filetype          = request.POST['missed_incorrect_filetype']
            invoice.missing_or_wrong_outside_link      = request.POST['missing_or_wrong_outside_link']
            invoice.missing_or_wrong_term_contract     = request.POST['missing_or_wrong_term_contract']
            invoice.not_posted_as_lead                 = request.POST['not_posted_as_lead']
            invoice.other_error                        = request.POST['other_error']
            invoice.other_serious_error                = request.POST['other_serious_error']
            invoice.refreshing_wds_page_to_diff_source = request.POST['refreshing_wds_page_to_diff_source']
            invoice.prevailing_wage_not_selected       = request.POST['prevailing_wage_not_selected']
            invoice.skipped_solicitation               = request.POST['skipped_solicitation']
            invoice.source_returned_without_a_note     = request.POST['source_returned_without_a_note']
            invoice.unexcused_unjustified_absence      = request.POST['unexcused_unjustified_absence']
            invoice.wrongbid_prebid_mandatory          = request.POST['wrongbid_prebid_mandatory']
            invoice.wrong_categories                   = request.POST['wrong_categories']
            invoice.wrong_geographic_location          =  request.POST['wrong_geographic_location']
            invoice.incomplete_and_incorrect_scope     = request.POST['incomplete_and_incorrect_scope']
            invoice.wrong_text_format                  = request.POST['wrong_text_format']
            invoice.total_deduction                    = request.POST['total_deduction']
            invoice.total_payable                      = request.POST['total_payable']
            invoice.save()
            messages.success(request, "Successfully edited invoice")   
            return HttpResponseRedirect('/invoice-list/')
        except:
            print("error")
            messages.error(request, "There was a problem editing invoice")
            return HttpResponseRedirect('/fixed/')


            