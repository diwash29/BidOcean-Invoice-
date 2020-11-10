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
from .utils import get_first_n_last_day, count_leaves, check_invoice, count_file_uploads, listToString, Currency_convertor

from django.contrib.auth import authenticate, login

import requests
import json
import xlwt
from django.http import JsonResponse

# Create your views here.

# 3650-8243-248
@login_required(login_url='/login/')
def index(request):
    user = request.user
    banner_obj = Banner.objects.all()
    banner = None
    if banner_obj:
        banner = banner_obj[0]
    try:
        employee = Employee.objects.get(auth_tbl=user)
        rolename = employee.role.name.lower()
        url = 'fixed'
        if rolename=='ir':
            url = 'ir'
        elif rolename=='br':
            url = 'br'	
        context = {'url':url, 'title':'home', 'role':rolename, 'banner':banner}	
        return render(request,'user_invoice/home.html',context)
    except:
        return HttpResponseRedirect('/employee/'+str(user.pk))

def make_users(request):
    url2   = "https://www.bidocean.com/api/production/request.php"
    token2 = "Pr85SNYWOV3GQdKProdReqstwer53VjZpA6lHoegm"

    requestData2               = {}
    requestData2['empid']      = ''
    requestData2['date_start'] = '2020-09-01'
    requestData2['date_end']   = '2020-09-30'
    requestData2['request']    = 'wds_researcher_stats'
    requestData2['token']      = token2
    requestDataJson2           = json.dumps(requestData2, ensure_ascii = 'False')

    result2 = requests.post(url2, json = requestDataJson2)

    result2_json = result2.json()
    for each in result2_json:
        username = (result2_json[each]['emp_name'].replace(" ", "_")).lower()
        designation = result2_json[each]['position']
        role = None
        if designation is not None:
            if 'Researcher' in designation:
                role = Role.objects.get(name__iexact='ir')
            elif 'Bids Reporter' in designation:
                role = Role.objects.get(name__iexact='br')
            else:
                role = Role.objects.get(name__iexact='fixed') 
        try:           
            user = Userdetail.objects.create(username=username, firstname=result2_json[each]['emp_name'].split(" ")[0], lastname=listToString(result2_json[each]['emp_name'].split(" ")[1:]), employee_id=result2_json[each]['emp_id'], role=role, designation=designation)
            user.set_password(result2_json[each]['hire_date'])
            user.save()
        except:
            pass    
    return HttpResponseRedirect('/manage_user/')


def ajax_get_leave(request):
    date        = request.GET.get('date', None)  
    emp         = request.GET.get('emp', None)   
    year        = int(date.split("-")[0])
    month       = int(date.split("-")[1])
    
    first_and_last_day = get_first_n_last_day(year,month)

    if emp is not None and emp is not "":
        employee = Employee.objects.get(pk=emp)
    else:
        emp      = request.user
        employee = Employee.objects.get(auth_tbl=request.user)
        
    rate =  Rate.objects.get(is_approved=1)    
    monthdate   = datetime.strptime(date, '%Y-%m').date()        
    leaves      = count_leaves(employee, monthdate)
    file_upload = count_file_uploads(employee, monthdate)
    employee_id = employee.emp_id
    params = {'empid': employee_id, 'year_month': date}


    url1   = 'https://www.bidocean.com/api/production/request.php'
    token1 = "Pr85SNYWOV3GQdKProdReqstwer53VjZpA6lHoegm"

    requestData1               = {}
    requestData1["empid"]      = int(employee_id)#1296#
    requestData1["year_month"] = date
    requestData1["request"]    = 'emp_production'
    requestData1["token"]      = token1

    requestDataJson1 = json.dumps(requestData1, ensure_ascii = 'False')
    result1 = requests.post(url1, json = requestDataJson1)

    url2   = "https://www.bidocean.com/api/production/request.php"
    token2 = "Pr85SNYWOV3GQdKProdReqstwer53VjZpA6lHoegm"

    requestData2               = {}
    requestData2['empid']      = int(employee_id)#1211#
    requestData2['date_start'] = first_and_last_day[0].strftime("%Y-%m-%d")
    requestData2['date_end']   = first_and_last_day[1].strftime("%Y-%m-%d")
    requestData2['request']    = 'wds_researcher_stats'
    requestData2['token']      = token2
    requestDataJson2           = json.dumps(requestData2, ensure_ascii = 'False')

    result2 = requests.post(url2, json = requestDataJson2)

    result2_json = result2.json()
    
    #wds_import_amt      = result2_json['0']['total_import']*(rate.wds_import)
    
    data                = {}
    data['wds']         = result2.json()
    if data['wds']:
        wds_solocitaion_amt = result2_json['0']['total_solicitation']*float(rate.wds_solicitaion)
        wds_source_amt      = result2_json['0']['total_source_count']*float(rate.wds_source)
        wds_edits_amt       = result2_json['0']['total_edits']*float(rate.wds_edit)

        data['wds']['0']['wds_solocitaion_amt'] = wds_solocitaion_amt
        data['wds']['0']['wds_source_amt']      = wds_source_amt
        data['wds']['0']['wds_edits_amt']       = wds_edits_amt
    #data['wds']['0']['wds_import_amt']      = wds_import_amt
    data['pp']              = result1.json()
    data['leaves']          = leaves
    data['file_upload']     = file_upload
    data['file_upload_amt'] = file_upload*float(rate.file_attach) 
    #data        = {'leaves' : leaves}
    return JsonResponse(data)

def export_invoice_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="'+str(datetime.today())+'invoice.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Invoice')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Employee name', 'Employee id', 'Invoice type', 'Phone no', 'Total payable', 'Bank Name', 'IfscCode', 'Account no']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    invoice = Invoice.objects.all()
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
        invoice   = invoice.filter(monthdate__gte=from_date, monthdate__lte=to_date)
    if bank is not None and bank is not '':
        query_param['bank'] = bank
        invoice = invoice.filter(bank_account__bank__iexact=bank)

    invoice = invoice.order_by('-invoice_date')    

    # paginator        = Paginator(invoice,1)
    # page             = request.GET.get('page')
    # paginatedcontent = paginator.get_page(page)

    rows = invoice.values_list('emp_ownwer__name', 'emp_ownwer__emp_id', 'emp_ownwer__role__name', 'emp_ownwer__phone_no','total_payable','bank_account__bank', 'bank_account__ifsc_other' ,'bank_account__acc_no')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response   

class PaySlip(TemplateView):
    template_name = "user_invoice/pay_slip.html"
    def get(self, request, pk):
        invoice            = Invoice.objects.get(id=pk)
        employee           = invoice.emp_ownwer
        today              = datetime.today()
        first_and_last_day = get_first_n_last_day(today.year,today.month)
        ps_others          =  PaySlipOthers.objects.filter(month_year__gte=first_and_last_day[0], month_year__lte=first_and_last_day[1], employee=employee)
        ps_others_data     = {'emp_state_ins_fund':0, 'percent_pf_prev_month':0, 'advance':0, 'commission':0, 'other_field': '', 'other_value':0}
        if ps_others:
            ps_others_data = ps_others[0]

        total       = round(float(invoice.total_payable)/(1.0-(float(invoice.percent_deduction)/100)), 2)
        dollar_rate = 0.0

        try:
            dollar_rate = float(DollarRate.objects.all()[0].dollar_rate)
        except:
            dollar_rate = 0.0
                 
        context = {
            'total'          : round(total),
            'invoice'        : invoice,
            'roles'          : Role.objects.all(),
            'title'          : 'Salary Slip',
            'role'           : Employee.objects.get(auth_tbl=self.request.user).role.name.lower(),
            'dollar_rate'    : dollar_rate,
            'ps_others_data' : ps_others_data
        }
        return render(request, self.template_name, context)
    def post(self, request, pk):
        invoice = Invoice.objects.get(id=pk)
        payslip_date = None
        if request.POST['payslip_date'] != '':
            payslip_date = datetime.strptime(request.POST['payslip_date'], '%Y-%m-%d').date()   
        try:
            invoice.emp_pf_id             = request.POST['emp_pf_id']
            invoice.emp_esi_id            = request.POST['emp_esi_id']
            invoice.dollar_rate           = request.POST['dollar_rate']
            invoice.emp_ins_fund          = request.POST['emp_ins_fund']
            invoice.percent_pf_prev_month = request.POST['percent_pf_prev_month']
            invoice.advance               = request.POST['advance']  
            invoice.payslip_date          = payslip_date
            invoice.cheque_cash           = request.POST['cheque_cash']
            invoice.cheque_no             = request.POST['cheque_no']
            invoice.payslip_bank          = request.POST['payslip_bank']               
            invoice.is_approved           = 1
            invoice.save()
            messages.success(request, "Successfully saved invoice")   
            return HttpResponseRedirect('/pay-slip/'+str(pk))
        except:
            print("error")
            messages.error(request, "There was a problem saving invoice")
            return HttpResponseRedirect('/pay-slip/'+str(pk))



class ChangePassword(TemplateView):
    template_name = 'user_invoice/change_password.html'
    def get(self, request):
        context = {
            'title': 'Change password',
            'role' : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
        }
        return render(request, self.template_name, context)
    def post(self, request):
        print(request.POST)
        username     = request.user.username
        old_password = request.POST['old_password']
        user = authenticate(request, username=username, password=old_password)  
        if user is not None:
            user.set_password(request.POST['password'])
            user.save()  
            login(request, user)         
            messages.success(request, "password changed Successfully")
            return HttpResponseRedirect('/change-password') 
        else:
            messages.error(request, "Old password is not correct")
            context = {
            'title': 'Change password',
            'role' : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
            }
            return render(request, self.template_name, context)    
            #messages.error(request, "There was a problem updating the role")

class RoleDisplayView(AdminOrHROrAccountsPanelMixin,TemplateView):
    template_name = 'user_invoice/role_list.html'
    def get(self, request):
        context = {
            'roles': Role.objects.all(),
            'title': 'Role list',
            'role' : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
        }
        return render(request, self.template_name, context)


class ErrorMessageView(TemplateView):
    template_name = 'user_invoice/error_msg.html'
    def get(self, request):
        context = {
            'title': 'Error',
            'role' : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
        }
        return render(request, self.template_name, context)


class RoleAddView(AdminOrHROrAccountsPanelMixin,TemplateView):
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

class RoleEditView(AdminOrHROrAccountsPanelMixin,TemplateView):
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


class RateDisplayView(AdminOrHROrAccountsPanelMixin,TemplateView):
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

class RateApproveView(AdminOrHROrAccountsPanelMixin, TemplateView):
    def get(self, request,pk):
        Rate.objects.all().update(is_approved=0)
        rate = Rate.objects.get(pk=pk)
        rate.is_approved = 1
        rate.save()
        #messages.success(request, "Successfully deleted employee") 
        return HttpResponseRedirect('/rate-list')



class RatePullView(AdminOrHROrAccountsPanelMixin, TemplateView):
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
            rate = Rate.objects.create(wds_solicitaion=request.POST['wds_solicitaion'], wds_source=request.POST['wds_source'], wds_edit=request.POST['wds_edit'], wds_import=request.POST['wds_import'], file_attach=request.POST['file_attach'], auth_day_off=request.POST['auth_day_off'], unauth_day_off=request.POST['unauth_day_off'], added_by=employee, is_approved=1)
            messages.success(request, "Successfully added rate")   
            return HttpResponseRedirect('/rate-list/')
        except:
            print("error")
            messages.error(request, "There was a problem adding rate")
        return HttpResponseRedirect('/rate-pull/'+str(pk))
              


class RateEditView(AdminOrHROrAccountsPanelMixin,TemplateView):
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
            rate.wds_solicitaion = request.POST['wds_solicitaion']
            rate.wds_source      = request.POST['wds_source']
            rate.wds_edit        = request.POST['wds_edit']
            rate.wds_import      = request.POST['wds_import']
            rate.file_attach     = request.POST['file_attach']
            rate.auth_day_off    = request.POST['auth_day_off']
            rate.unauth_day_off  = request.POST['unauth_day_off']
            
            rate.is_approved        = 1
            rate.save()
            messages.success(request, "Successfully edited rate")   
            return HttpResponseRedirect('/rate-list/')
        except:
            print("error")
            messages.error(request, "There was a problem adding rate")
        return HttpResponseRedirect('/rate-edit/'+str(pk))    


class RateAddView(AdminOrHROrAccountsPanelMixin,TemplateView):
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
            rate = Rate.objects.create(wds_solicitaion=request.POST['wds_solicitaion'], wds_source=request.POST['wds_source'], wds_edit=request.POST['wds_edit'], wds_import=request.POST['wds_import'], file_attach=request.POST['file_attach'], auth_day_off=request.POST['auth_day_off'], unauth_day_off=request.POST['unauth_day_off'], added_by=employee, is_approved=1)
            messages.success(request, "Successfully added rate")   
            return HttpResponseRedirect('/rate-list/')
        except:
            print("error")
            messages.error(request, "There was a problem adding rate")
            return HttpResponseRedirect('/rate-add/')


        



class EmployeeDisplayView(AdminOrHROrAccountsPanelMixin,TemplateView):
    template_name = 'user_invoice/employee_list.html'
    def get(self, request):
        employee_list    = Employee.objects.exclude(Q(name__icontains="None None")).all()
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
        managers      = Employee.objects.filter(is_manager=1)
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
            'title'        : 'Add employee',
            'managers'     : managers
        }
        return render(request, self.template_name, context)

    def post(self, request, user_id):
        user     = Userdetail.objects.get(pk=user_id)
        name     = request.POST['name']
        try:
            role      = Role.objects.get(pk=request.POST['role'])
            user.role = role
            user.save()
        except:
            role = user.role                 
        salary      = request.POST['salary']
        address     = request.POST['address']
        phone_no    = request.POST['phone_no']
        emp_id      = request.POST['emp_id']
        designation = request.POST['designation']
        pf_id       = request.POST['pf_id']
        esi_id      = request.POST['esi_id']
        # report_to = None
        if emp_id == 'None' or emp_id == '':
            emp_id = 999999999
        if 'report_to' not in request.POST:
            report_to = None
        else:
            try:
                report_to = Employee.objects.get(pk=request.POST['report_to'])
            except:
                report_to =None

        # leaves   = request.POST['leaves']
        auth_tbl = user
        employee = Employee.objects.create(name=name, role=role, salary=salary, pf_id=pf_id, esi_id=esi_id, address=address, phone_no=phone_no, emp_id=emp_id, auth_tbl=auth_tbl, is_manager=user.is_manager, report_to=report_to, designation = designation)
        user.designation = designation
        user.save()
        leave_bal = LeaveBalance.objects.create(paid_leave=10, others_leave=0, sick_leave=0, employee=employee)

        return HttpResponseRedirect('/')

class EmployeeEditView(AdminOrHROrAccountsPanelMixin,TemplateView):
    template_name = 'user_invoice/add_employee.html'

    def get(self, request, pk):
        employee      = Employee.objects.get(pk=pk)
        roles         = Role.objects.all()        # employee_form = EmployeeForm()
        managers      = Employee.objects.filter(is_manager=1)
        context = {
            # 'employee_form': employee_form,
            'employee'     : employee,
            'roles'        : roles,
            'submit'       : 'Edit Employee',
            'title'        : 'Edit employee',
            'role'         : Employee.objects.get(auth_tbl=self.request.user).role.name.lower(),
            'managers'     : managers
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        print(request.POST)
        if 'report_to' not in request.POST:
            report_to = None
        else:
            try:
                report_to = Employee.objects.get(pk=request.POST['report_to'])
            except:
                report_to =None
        user               = request.user
        employee           = Employee.objects.get(pk=pk)
        leave_bal          = LeaveBalance.objects.get(employee=employee)
        employee.name      = request.POST['name']
        employee.role      = user.role
        employee.salary    = request.POST['salary']
        employee.address   = request.POST['address']
        employee.phone_no  = request.POST['phone_no']
        employee.designation = request.POST['designation']
        employee.pf_id       = request.POST['pf_id']
        employee.esi_id      = request.POST['esi_id']
        # employee.leaves   = request.POST['leaves']
        employee.emp_id    = request.POST['emp_id']
        employee.report_to = report_to    
        employee.save()
        user.designation = request.POST['designation']
        user.save()
        leave_bal.paid_leave   = request.POST['paid_leave']
        leave_bal.sick_leave   = request.POST['sick_leave']
        leave_bal.others_leave = request.POST['others_leave']
        leave_bal.save()
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
        #try:
        employee           = Employee.objects.get(auth_tbl=self.request.user)
        rolename           = employee.role.name.lower()
        today              = datetime.now()   
        date               = today.strftime("%Y-%m")
        first_and_last_day = get_first_n_last_day(today.year,today.month) 
        # if rolename == 'ir' or rolename == 'br':
        rate =  Rate.objects.get(is_approved=1)    
        monthdate   = datetime.strptime(date, '%Y-%m').date()  
        print(monthdate)      
        leaves      = count_leaves(employee, monthdate)
        file_upload = count_file_uploads(employee, monthdate)
        employee_id = employee.emp_id
        params = {'empid': employee_id, 'year_month': date}


        url1   = 'https://www.bidocean.com/api/production/request.php'
        token1 = "Pr85SNYWOV3GQdKProdReqstwer53VjZpA6lHoegm"

        requestData1               = {}
        requestData1["empid"]      = int(employee_id)#1296#
        requestData1["year_month"] = date
        requestData1["request"]    = 'emp_production'
        requestData1["token"]      = token1

        requestDataJson1 = json.dumps(requestData1, ensure_ascii = 'False')
        result1 = requests.post(url1, json = requestDataJson1)

        url2   = "https://www.bidocean.com/api/production/request.php"
        token2 = "Pr85SNYWOV3GQdKProdReqstwer53VjZpA6lHoegm"

        requestData2               = {}
        requestData2['empid']      = int(employee_id)#1211#
        requestData2['date_start'] = first_and_last_day[0].strftime("%m/%d/%y")
        requestData2['date_end']   = first_and_last_day[1].strftime("%m/%d/%y")
        requestData2['request']    = 'wds_researcher_stats'
        requestData2['token']      = token2
        requestDataJson2           = json.dumps(requestData2, ensure_ascii = 'False')

        result2 = requests.post(url2, json = requestDataJson2)

        result2_json = result2.json()

        
        #wds_import_amt      = result2_json['0']['total_import']*(rate.wds_import)
        
        data                = {}
        data['wds']         = result2.json()
        total_solocitaion_count = 0
        total_source_count      = 0
        total_edits             = 0


        
        emp_fixed_salary = employee.salary
        if employee.salary == 'None' or employee.salary is None or employee.salary == "":
            emp_fixed_salary = 0.0 
            
        if data['wds']:
            total_solocitaion_count = result2_json['0']['total_solicitation']
            total_source_count      = result2_json['0']['total_source_count']
            total_edits             = result2_json['0']['total_edits']
            data['wds']['0']['wds_solocitaion_amt'] = total_solocitaion_count*float(rate.wds_solicitaion)
            data['wds']['0']['wds_source_amt']      = total_source_count*float(rate.wds_source)
            data['wds']['0']['wds_edits_amt']       = total_edits*float(rate.wds_edit)
        wds_solocitaion_amt = total_solocitaion_count*float(rate.wds_solicitaion)
        wds_source_amt      = total_source_count*float(rate.wds_source)
        wds_edits_amt       = total_edits*float(rate.wds_edit)
            
        #data['wds']['0']['wds_import_amt']      = wds_import_amt
        data['pp']              = result1.json()
        data['leaves']          = leaves
        data['file_upload']     = file_upload
        data['file_upload_amt'] = file_upload*float(rate.file_attach)

        leaves_deduction        = (leaves*float(rate.auth_day_off)) + float(data['pp']['Total Fine'])
        leaves_deduction        = round(leaves_deduction, 2)
        # print(data)
        try:
            month                = int(monthdate.month)
            pdeduction_obj       = MonthlyDeduction.objects.get(month=month)
            percentage_deduction = float(pdeduction_obj.deduction_percent)       
        except:
            percentage_deduction = 0.0
        # print(float(wds_solocitaion_amt))
        # print(float(wds_source_amt))  
        # print(float(wds_edits_amt))
        # print(float(data['file_upload_amt']))  
        # print(float(emp_fixed_salary))
        total_pay        = float(wds_solocitaion_amt)+float(wds_source_amt)+float(wds_edits_amt)+float(data['file_upload_amt'])+float(emp_fixed_salary)-leaves_deduction
        total_pay = float(round(total_pay*(1.0-(percentage_deduction/100)), 2))
        ch_invoice    = check_invoice(employee)
        if ch_invoice is None:
            invoice_add = Invoice.objects.create(invoice_date=today, monthdate=today, production_pay_deduction=data['pp']['Total Fine'], wds_solicitaion=total_solocitaion_count, wds_source=total_source_count, wds_edit=total_edits, file_upload=data['file_upload'], authorised_day_off = leaves,  total_deduction = leaves_deduction , total_payable = total_pay, emp_ownwer = employee, percent_deduction=percentage_deduction, wds_solicitaion_rate=rate.wds_solicitaion, wds_source_rate=rate.wds_source, wds_edit_rate=rate.wds_edit,fixed_salary=emp_fixed_salary, auth_day_rate=rate.auth_day_off)    
        else:
            invoice_edit                          = Invoice.objects.get(pk=ch_invoice)
            invoice_edit.production_pay_deduction = data['pp']['Total Fine']
            invoice_edit.wds_solicitaion          = total_solocitaion_count
            invoice_edit.wds_source               = total_source_count
            invoice_edit.wds_edit                 = total_edits
            invoice_edit.file_upload              = data['file_upload']
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

        today          = datetime.now()    
        current_month  = today.month
        current_year   = today.year
        start_end_date = get_first_n_last_day(current_year, current_month)    
        invoice = Invoice.objects.exclude(monthdate__gte=start_end_date[0], monthdate__lte=start_end_date[1])    
        if rolename == 'admin' or  rolename == 'hr' or  rolename == 'accountant':
            invoice = invoice.exclude(Q(emp_ownwer__name__icontains="None None")).all()
        else:
            invoice = invoice.filter(emp_ownwer=employee).all()	

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
            invoice   = invoice.filter(monthdate__gte=from_date, monthdate__lte=to_date)
        if bank is not None and bank is not '':
            query_param['bank'] = bank
            invoice = invoice.filter(bank_account__bank__iexact=bank)

        invoice = invoice.order_by('-invoice_date')    

        paginator        = Paginator(invoice,10)
        page             = request.GET.get('page')
        paginatedcontent = paginator.get_page(page)	
        context = {
            'query_param' : query_param,
            'invoices'    : paginatedcontent,
            'title'       : 'Invoice list',
            'role'        : rolename
        }
        return render(request, self.template_name, context)
        # except:
        #     return HttpResponseRedirect('/employee/'+str(self.request.user.pk))

class IrEditView(IRPanelMixin,TemplateView):
    template_name='user_invoice/ir.html'

    def get(self, request, pk):
        invoice  = Invoice.objects.get(pk=pk)
        employee = invoice.emp_ownwer
        rates    = invoice.rate
        rolename = Employee.objects.get(auth_tbl=request.user).role.name.lower()
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
        try:
            user          = self.request.user
            employee      = Employee.objects.get(auth_tbl=user)
            ch_invoice    = check_invoice(employee)
            if ch_invoice is None:
                rolename      = employee.role.name.lower()
                rates         = Rate.objects.get(is_approved=1)
                context = {
                    'employee'  : employee,
                    'submit'    : 'Add IR Invoice',
                    'title'     : 'Add ir',
                    'role'      : rolename,
                    'rates'     : rates,
                }
                return render(request, self.template_name, context)
            else:
                 return HttpResponseRedirect('/ir/'+str(ch_invoice))  
        except:
            return HttpResponseRedirect('/error/')            

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
            invoice = Invoice.objects.create(invoice_date=invoice_date, monthdate=monthdate, emp_type=request.POST['emp_type'], bank_account=bank_account, production_pay=request.POST['production_pay'], wds_solicitaion=request.POST['wds_solicitaion'], wds_source=request.POST['wds_source'], wds_edit=request.POST['wds_edit'], wds_import=request.POST['wds_import'], file_upload=request.POST['file_upload'], fixed_salary=request.POST['fixed_salary'], authorised_day_off = request.POST['authorised_day_off'], unauthorised_day_off=request.POST['unauthorised_day_off'],  total_deduction = request.POST['total_deduction'] , total_payable = request.POST['total_payable'], emp_ownwer = employee, rate=rate)    
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
        rolename = Employee.objects.get(auth_tbl=request.user).role.name.lower()
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
        try:
            user          = self.request.user
            employee      = Employee.objects.get(auth_tbl=user)
            ch_invoice    = check_invoice(employee)
            if ch_invoice is None:
                rolename      = employee.role.name.lower()
                # leaves        = count_leaves(employee)
                rates         = Rate.objects.get(is_approved=1)
                context = {
                    'employee'  : employee,
                    'submit'    : 'Add BR Invoice',
                    'title'     : 'Add br',
                    'role'      : rolename,
                    'rates'     : rates,
                }
                return render(request, self.template_name, context)
            else:
                return HttpResponseRedirect('/br/'+str(ch_invoice)) 
        except:
            return HttpResponseRedirect('/error/')                        

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
            invoice = Invoice.objects.create(invoice_date=invoice_date, monthdate=monthdate, emp_type=request.POST['emp_type'], bank_account=bank_account, production_pay=request.POST['production_pay'], wds_solicitaion=request.POST['wds_solicitaion'], wds_source=request.POST['wds_source'], wds_edit=request.POST['wds_edit'], wds_import=request.POST['wds_import'], file_upload=request.POST['file_upload'], fixed_salary=request.POST['fixed_salary'], authorised_day_off = request.POST['authorised_day_off'], unauthorised_day_off=request.POST['unauthorised_day_off'],  total_deduction = request.POST['total_deduction'] , total_payable = request.POST['total_payable'], emp_ownwer = employee, rate=rate)
            messages.success(request, "Successfully added invoice")   
            return HttpResponseRedirect('/invoice-list/')
        except:
            print("error")
            messages.error(request, "There was a problem adding invoice")
            return HttpResponseRedirect('/br/')	  

class FixedAddView(FixedPanelMixin,TemplateView):
    template_name='user_invoice/fixed.html'

    def get(self, request):  
        try:      
            user           = self.request.user
            employee       = Employee.objects.get(auth_tbl=user)  
            ch_invoice     = check_invoice(employee)    
            if ch_invoice is None:  
                # leaves         = count_leaves(employee)
                rolename       = employee.role.name.lower()
                rates          = Rate.objects.get(is_approved=1)
                context = {
                    'employee'  : employee,
                    'submit'    : 'Add Fixed Invoice',
                    'title'     : 'Add fixed',
                    'role'      : rolename,
                    'rates'     : rates,
                }
                return render(request, self.template_name, context)
            else:
                return HttpResponseRedirect('/fixed/'+str(ch_invoice))
        except:
            return HttpResponseRedirect('/error/')                    
                

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
        rolename = Employee.objects.get(auth_tbl=request.user).role.name.lower()
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
           

class ProductionReportAddView(TemplateView):
    template_name='user_invoice/productionreportform.html'

    def get(self, request):
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        rolename      = employee.role.name.lower()
        try:
            todays_report = ProductionReport.objects.get(employee=employee, date=date.today())
        except:
            todays_report = None
        # leaves        = count_leaves(employee)
        if todays_report is  None:
            context = {
                'employee'  : employee,
                'submit'    : 'Add Production Report',
                'title'     : 'Add production report',
                'role'      : rolename,
            }
            return render(request, self.template_name, context) 
        else:
            return HttpResponseRedirect('/production_report-edit/'+str(todays_report.pk))            
                    

    def post(self, request):
        print(request.POST)
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        try:
            production_date = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
            production_report = ProductionReport.objects.create(date=production_date, source=request.POST['source'], entries=request.POST['entries'], addendum=request.POST['addendum'], import_report=request.POST['import_report'], import_reject=request.POST['import_reject'], solic_no=request.POST['solic_no'], file_attach=request.POST['file_attach'], wds_per_day=request.POST['wds_per_day'], employee=employee )    
            messages.success(request, "Successfully added production report")   
            return HttpResponseRedirect('/production_report-list/')
        except:
            print("error")
            messages.error(request, "There was a problem adding invoice")
            return HttpResponseRedirect('/production_report-add/')


class ProductionReportEditView(TemplateView):
    template_name='user_invoice/productionreportform.html'

    def get(self, request, pk):
        user              = self.request.user
        employee          = Employee.objects.get(auth_tbl=user)
        rolename          = employee.role.name.lower()
        production_report = ProductionReport.objects.get(pk=pk)
        # leaves        = count_leaves(employee)
        context = {
            'employee'          : employee,
            'submit'            : 'Edit Production Report',
            'title'             : 'Edit production report',
            'role'              : rolename,
            'production_report' : production_report
        }
        return render(request, self.template_name, context) 
                    

    def post(self, request, pk):
        print(request.POST)
        user              = self.request.user
        employee          = Employee.objects.get(auth_tbl=user)
        production_report = ProductionReport.objects.get(pk=pk)
        try:
            production_date                 = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()
            production_report.date          = production_date
            production_report.source        = request.POST['source']
            production_report.entries       = request.POST['entries']
            production_report.addendum      = request.POST['addendum']
            production_report.import_report = request.POST['import_report']
            production_report.import_reject = request.POST['import_reject']
            production_report.solic_no      = request.POST['solic_no']
            production_report.file_attach   = request.POST['file_attach']
            production_report.wds_per_day   = request.POST['wds_per_day']
            production_report.save() 
            messages.success(request, "Successfully edited production report")   
            return HttpResponseRedirect('/production_report-list/')
        except:
            print("error")
            messages.error(request, "There was a problem editing invoice")
            return HttpResponseRedirect('/production_report-edit/'+str(pk))


class ProductionReportDisplayView(AdminPanelMixin, TemplateView):
    template_name = 'user_invoice/production_report_list.html'

    def get(self, request):
        # try:
        employee  =  Employee.objects.get(auth_tbl=self.request.user)
        rolename  =  employee.role.name.lower()
        try:
            todays_report = ProductionReport.objects.get(employee=employee, date=date.today())
        except:
            todays_report = None
        if rolename == 'admin' or  rolename == 'hr':
            production_report = ProductionReport.objects.all()
        else:
            production_report = ProductionReport.objects.filter(employee=employee).all() 

        search        = request.GET.get('search', None)
        from_date     = request.GET.get('from_date', None)
        to_date       = request.GET.get('to_date', None)
        bank          = request.GET.get('bank',None)
        
        query_param = {}  
        if search is not None and search is not '':
            search = search.strip()
            query_param['search'] = search 
            production_report = production_report.filter(Q(employee__name__icontains=search)|Q(solic_no__icontains=search)) 
        if (from_date is not None and to_date is not None) and (from_date != "" and to_date != ""):
            query_param['from_date'] = from_date
            query_param['to_date']   = to_date
            to_date   = datetime.strptime(to_date,"%Y-%m-%d").date()
            from_date = datetime.strptime(from_date,"%Y-%m-%d").date()  
            production_report   = production_report.filter(date__gte=from_date, date__lte=to_date)
        # if bank is not None and bank is not '':
        #     query_param['bank'] = bank
        #     invoice = invoice.filter(bank_account__bank__iexact=bank)

        production_report = production_report.order_by('employee__name')    

        paginator        = Paginator(production_report,10)
        page             = request.GET.get('page')
        paginatedcontent = paginator.get_page(page) 
        context = {
            'query_param'       : query_param,
            'production_report' : paginatedcontent,
            'title'             : 'Production report list',
            'role'              : rolename,
            'todays_report'     : todays_report
        }
        return render(request, self.template_name, context)
        # except:
        #     return HttpResponseRedirect('/employee/'+str(self.request.user.pk))            



class DeductionDisplayView(AdminOrAccountsPanelMixin,TemplateView):
    template_name = "user_invoice/deduction_list.html"
    def get(self, request):
        employee = Employee.objects.get(auth_tbl=self.request.user)
        role     = employee.role.name.lower()
        context = {
            'role'      : role,
            'duduction' : MonthlyDeduction.objects.all().order_by('month'),
            'title'     : 'Deduction list', 
            'employee'  : employee
        }
        return render(request, self.template_name, context)


class DeductionEditView(AdminOrAccountsPanelMixin, TemplateView):
    template_name = 'user_invoice/add_deduction.html'
    def get(self, request, pk):
        month = [(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')]
        deduction = MonthlyDeduction.objects.get(pk=pk)
        context ={
            'submit'    : 'Edit Deduction',
            'title'     : 'Edit deduction',
            'month'     : month,
            'role'      : Employee.objects.get(auth_tbl=self.request.user).role.name.lower(),
            'deduction' : deduction
        }
        return render(request, self.template_name, context)   
    def post(self, request, pk):
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        deduction     = MonthlyDeduction.objects.get(pk=pk)
        try:
            deduction.month             = request.POST['month']
            deduction.deduction_percent = request.POST['deduction_percent']
            deduction.save()
            messages.success(request, "Successfully edited deduction")   
            return HttpResponseRedirect('/deduction-list/')
        except:
            print("error")
            messages.error(request, "There was a problem editing deduction")
            return HttpResponseRedirect('/deduction-edit/'+pk)


class DeductionAddView(AdminOrAccountsPanelMixin, TemplateView):
    template_name = 'user_invoice/add_deduction.html'
    def get(self, request):
        month = [(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')]
        context ={
            'submit'    : 'Add Deduction',
            'title'     : 'Add deduction',
            'month'     : month,
            'role'      : Employee.objects.get(auth_tbl=self.request.user).role.name.lower(),
        }
        return render(request, self.template_name, context)   
    def post(self, request):
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        # try:
        deduction = MonthlyDeduction.objects.create(month=request.POST['month'], deduction_percent=request.POST['deduction_percent'])
        messages.success(request, "Successfully edited deduction")   
        return HttpResponseRedirect('/deduction-list/')
        # except:
        #     print("error")
        #     messages.error(request, "There was a problem editing deduction")
        #     return HttpResponseRedirect('/deduction-add/')            
class DollarRateEditView(AdminOrAccountsPanelMixin, TemplateView):
    template_name = 'user_invoice/add_dollar_rate.html'
    def get(self, request, pk):
        dollar_rate = DollarRate.objects.get(pk=pk)
        context ={
            'submit'      : 'Edit Dollar Rate',
            'title'       : 'Edit dollar rate',
            'role'        : Employee.objects.get(auth_tbl=self.request.user).role.name.lower(),
            'dollar_rate' : dollar_rate
        }
        return render(request, self.template_name, context)   
    def post(self, request, pk):
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        dollar_rate   = DollarRate.objects.get(pk=pk)
        try:
            dollar_rate.dollar_rate = request.POST['dollar_rate']
            dollar_rate.save()
            messages.success(request, "Successfully edited dollar rate")   
            return HttpResponseRedirect('/dollar-rate-list/')
        except:
            print("error")
            messages.error(request, "There was a problem editing dollar rate")
            return HttpResponseRedirect('/dollar-rate-edit/'+pk)


class AddDollarRateView(AdminOrAccountsPanelMixin, TemplateView):
    template_name = 'user_invoice/add_dollar_rate.html'
    def get(self, request):
        
        context ={
            'submit'    : 'Add Dollar Rate',
            'title'     : 'Add dollar rate',
            'role'      : Employee.objects.get(auth_tbl=self.request.user).role.name.lower(),
        }
        return render(request, self.template_name, context)   
    def post(self, request):
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        # try:
        deduction = DollarRate.objects.create(dollar_rate=request.POST['dollar_rate'])
        messages.success(request, "Successfully added dollar rate")   
        return HttpResponseRedirect('/dollar-rate-list/')

class DollarRateDisplayView(AdminOrAccountsPanelMixin,TemplateView):
    template_name = "user_invoice/dollar_rate_list.html"
    def get(self, request):
        employee    = Employee.objects.get(auth_tbl=self.request.user)
        role        = employee.role.name.lower()
        dollar_rate = DollarRate.objects.all()
        if dollar_rate:
            context = {
                'role'        : role,
                'dollar_rate' : dollar_rate,
                'title'       : 'Dollar rate list', 
                'employee'    : employee
            }
            return render(request, self.template_name, context)      
        else:
            return HttpResponseRedirect('/add-payslip-other/')
                  

class AddPaySlipOthersView(AdminOrAccountsPanelMixin, TemplateView):
    template_name = 'user_invoice/add_pay_slip_others.html'
    def get(self, request):     
        context ={
            'submit'    : 'Add PaySlip Others',
            'title'     : 'Add payslip others',
            'role'      : Employee.objects.get(auth_tbl=self.request.user).role.name.lower(),
            'employees' : Employee.objects.exclude(Q(name__icontains="None None")).all().order_by('name')
        }
        return render(request, self.template_name, context)   
    def post(self, request):
        print(request.POST)
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        payslipother  = PaySlipOthers.objects.create(month_year=request.POST['month_year'], employee=Employee.objects.get(id=request.POST['employee']), emp_state_ins_fund=request.POST['emp_state_ins_fund'], percent_pf_prev_month=request.POST['percent_pf_prev_month'], advance=request.POST['advance'], commission=request.POST['commission'], other_field=request.POST['other_field'], other_value=request.POST['other_value']) 
        # try:
        #deduction = PaySlipOthers.objects.create(dollar_rate=request.POST['dollar_rate'])
        #messages.success(request, "Successfully added dollar rate")   
        return HttpResponseRedirect('/payslips-others-list/')                  


class PaySlipOthersDisplayView(AdminOrAccountsPanelMixin, TemplateView):
    template_name = 'user_invoice/pay_slip_others_list.html'
    def get(self, request):
        context = {
            'title'          : 'PaySlip other list',
            'role'           : Employee.objects.get(auth_tbl=self.request.user).role.name.lower(),
            'payslip_others' : PaySlipOthers.objects.all()
        }
        return render(request, self.template_name, context)

class EditPaySlipOthersView(AdminOrAccountsPanelMixin, TemplateView):
    template_name = 'user_invoice/add_pay_slip_others.html'
    def get(self, request, pk):
        ps_others =  PaySlipOthers.objects.get(pk=pk)     
        context ={
            'submit'    : 'EditPaySlip Others',
            'title'     : 'Edit payslip others',
            'role'      : Employee.objects.get(auth_tbl=self.request.user).role.name.lower(),
            'employees' : Employee.objects.exclude(Q(name__icontains="None None")).all().order_by('name'),
            'ps_others' : ps_others
        }
        return render(request, self.template_name, context)

def ajax_check_ps_others(request):
    emp_id             = request.GET.get('emp_id', None)
    add_or_edit        = request.GET.get('add_or_edit', None)
    date               = request.GET.get('date', None)
    employee           = Employee.objects.get(pk=emp_id)
    date               = datetime.strptime(date,"%Y-%m-%d").date()
    first_and_last_day = get_first_n_last_day(date.year,date.month)  
    # print(first_and_last_day)
    data               = {}
    ps_others          = PaySlipOthers.objects.filter(month_year__gte=first_and_last_day[0], month_year__lte=first_and_last_day[1], employee=employee)  
    data['redirect_page'] = None
    if ps_others:
        data['is_present']    = 'yes'
        data['redirect_page'] = '/edit-payslips-others/'+str(ps_others[0].pk)
    else:
        data['is_present'] = 'no'
        if add_or_edit == 'edit':
            data['redirect_page'] = '/add-payslips-others/'  
    
    return JsonResponse(data)   