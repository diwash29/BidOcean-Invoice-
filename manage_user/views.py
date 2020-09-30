from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from user_invoice.models import Role, Employee
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from user_invoice.mixin import AdminOrHRPanelMixin, AdminPanelMixin, IRPanelMixin, BRPanelMixin, FixedPanelMixin
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q
import calendar
from django.http import JsonResponse

class ManageUser(AdminOrHRPanelMixin,TemplateView):
    template_name = 'manage_user/user_list.html'
    def get(self, request):
        employee   = Employee.objects.get(auth_tbl=self.request.user)
        role       = employee.role.name.lower()
        roles_data = Role.objects.all() 
        users      = Userdetail.objects.all()
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
                user.role        = Role.objects.get(pk=request.POST['role'])
                user.save()
                try:
                    emp      = Employee.objects.get(auth_tbl=user)
                    emp.role = Role.objects.get(pk=request.POST['role'])
                    emp.save()
                except:
                    pass    
                messages.success(request, "Successfully edited user")
            else:
                try:
                    role = Role.objects.get(pk=request.POST['role'])
                except:
                    role = None
                user = Userdetail.objects.create(username=request.POST['username'], firstname=request.POST['firstname'], lastname=request.POST['lastname'], phone=request.POST['phone'], email=request.POST['email'], address=request.POST['address'], employee_id=request.POST['employee_id'], salary=request.POST['salary'], role=role)
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
    data = {'id':user.pk, 'username':user.username, 'firstname':user.firstname, 'lastname':user.lastname, 'phone':user.phone, 'email':user.email, 'address':user.address, 'role':role, 'employee_id':user.employee_id, 'salary':user.salary }
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

