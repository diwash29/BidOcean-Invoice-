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
        employee = Employee.objects.get(auth_tbl=self.request.user)
        role     = employee.role.name.lower()
        users    = Userdetail.objects.all()
        context = {
            'role'  : role,
            'users' : users
            # 'title': 'Role list',
            # 'role' : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
        }
        return render(request, self.template_name, context)
    def post(self, request):
        print(request.POST)
        try:
            delete_id = request.POST['delete']
            user = Userdetail.objects.get(pk=delete_id)
            user.delete()
            messages.success(request, "Successfully deleted user") 
            return HttpResponseRedirect('/manage_user/')	
        except:                        	 
            if request.POST['hidden_user'] != "":
                user           = Userdetail.objects.get(pk = request.POST['hidden_user'])
                user.username  = request.POST['username']
                user.firstname = request.POST['firstname']
                user.lastname  = request.POST['lastname']
                user.phone     = request.POST['phone']
                user.email     = request.POST['email']
                user.address   = request.POST['address']
                user.save()
            else:
                user = Userdetail.objects.create(username=request.POST['username'], firstname=request.POST['firstname'], lastname=request.POST['lastname'], phone=request.POST['phone'], email=request.POST['email'], address=request.POST['address'])
                user.set_password(request.POST["password"])
                user.save()
            return HttpResponseRedirect('/manage_user/')	


def ajax_user_data(request):
    edit_id = request.GET.get('edit_id', None)
    user    = Userdetail.objects.get(pk=edit_id)
    
    data = {'id':user.pk, 'username':user.username, 'firstname':user.firstname, 'lastname':user.lastname, 'phone':user.phone, 'email':user.email, 'address':user.address }
    return JsonResponse(data)
