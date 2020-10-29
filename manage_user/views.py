from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from leave.models import LeaveBalance
from user_invoice.models import Role, Employee
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from user_invoice.mixin import OnlyAdminPanelMixin, AdminPanelMixin, IRPanelMixin, BRPanelMixin, FixedPanelMixin
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q
import calendar
from django.http import JsonResponse

class ManageUser(OnlyAdminPanelMixin,TemplateView):
    template_name = 'manage_user/user_list.html'
    def get(self, request):
        employee   = Employee.objects.get(auth_tbl=self.request.user)
        role       = employee.role.name.lower()
        roles_data = Role.objects.all() 
        users      = Userdetail.objects.all().order_by('username')
        paginator        = Paginator(users,10)
        page             = request.GET.get('page')
        paginatedcontent = paginator.get_page(page)
        context = {
            'role'       : role,
            'users'      : paginatedcontent,
            'roles_data' : roles_data
        }
        return render(request, self.template_name, context)
    def post(self, request):
        print(request.POST)
        try:
            if 'delete' in request.POST:
                delete_id = request.POST['delete']
                user = Userdetail.objects.get(pk=delete_id)
                user.delete()
                messages.success(request, "Successfully deleted user") 
                return HttpResponseRedirect('/manage_user/')	
            else:
                reset_password_id = request.POST['reset_password_user']
                user = Userdetail.objects.get(pk=reset_password_id)
                user.set_password(request.POST['new_password'])
                user.save()
                messages.success(request, "Successfully reset password") 
                return HttpResponseRedirect('/manage_user/')        
        except:                        	 
            if request.POST['hidden_user'] != "":
                user             = Userdetail.objects.get(pk = request.POST['hidden_user'])
                user.username    = request.POST['username']
                user.firstname   = request.POST['firstname']
                user.lastname    = request.POST['lastname']
                user.phone       = request.POST['phone']
                user.email       = request.POST['email']
                user.address     = request.POST['address']
                user.employee_id = request.POST['employee_id']
                user.salary      = request.POST['salary']
                user.is_manager  = request.POST['editis_manager']
                user.role        = Role.objects.get(pk=request.POST['role'])
                user.save()
                try:
                    emp            = Employee.objects.get(auth_tbl=user)
                    emp.role       = Role.objects.get(pk=request.POST['role'])
                    emp.is_manager = request.POST['editis_manager']
                    if emp.is_manager == 1:
                        emp.report_to = None
                    emp.save()
                except:
                    print(request.POST['editis_manager'])
                    if request.POST['editis_manager'] == '1':
                        employee = Employee.objects.create(name=request.POST['firstname']+" "+request.POST['lastname'], role=Role.objects.get(pk=request.POST['role']), salary=request.POST['salary'], address=request.POST['address'], phone_no=request.POST['phone'], emp_id=request.POST['employee_id'],auth_tbl=user, is_manager=request.POST['editis_manager'])    
                        leave_bal = LeaveBalance.objects.create(paid_leave=10, others_leave=0, sick_leave=0, employee=employee)
                messages.success(request, "Successfully edited user")
            else:
                try:
                    role = Role.objects.get(pk=request.POST['role'])
                except:
                    role = None
                user = Userdetail.objects.create(username=request.POST['username'], firstname=request.POST['firstname'], lastname=request.POST['lastname'], phone=request.POST['phone'], email=request.POST['email'], address=request.POST['address'], employee_id=request.POST['employee_id'], salary=request.POST['salary'], role=role, is_manager=request.POST['is_manager'])
                user.set_password(request.POST["password"])
                user.save()
                messages.success(request, "Successfully added user")
            return HttpResponseRedirect('/manage_user/')	


def ajax_user_data(request):
    edit_id = request.GET.get('edit_id', None)
    user    = Userdetail.objects.get(pk=edit_id)
    try:
        role = user.role.pk
    except:
        role = None
    data = {'id':user.pk, 'username':user.username, 'firstname':user.firstname, 'lastname':user.lastname, 'phone':user.phone, 'email':user.email, 'address':user.address, 'role':role, 'employee_id':user.employee_id, 'salary':user.salary, 'is_manager':user.is_manager }
    return JsonResponse(data)


def ajx_check_username(request):
    username  = request.GET.get('username',None)
    editid    = request.GET.get('editid', None)
    select_id = request.GET.get('id', None)       
    if editid is not None and editid is not '':
        user_exist = Userdetail.objects.filter(username=username).exclude(pk=editid)
    else: 
        user_exist = Userdetail.objects.filter(username=username)  
    if user_exist:
        exist = True
    else:
        exist = False
    data = {'exist' : exist, 'id' : select_id, 'username' : username}
    return JsonResponse(data)    

