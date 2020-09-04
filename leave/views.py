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

# Create your views here.

# def index(request):	
# 	return render(request,'leave/leave_request.html')


def leave_bal(request):
    leave_type = request.GET.get('leave_type', None)
    emp        = request.GET.get('emp', None)
    employee   = Employee.objects.get(pk=emp)
    emp_leave_bal = LeaveBalance.objects.get(employee=employee)
    
    if leave_type == 'sl':
    	leave_bal = emp_leave_bal.sick_leave
    elif leave_type == 'cl':
    	leave_bal = emp_leave_bal.casual_leave
    else:
    	leave_bal = emp_leave_bal.earned_leave
    data = {'leave' : leave_bal}
    return JsonResponse(data)	  

class LeaveRequestDisplayView(AdminPanelMixin,TemplateView):
    template_name = "leave/approve_leave.html"
    def get(self, request):
        user          = self.request.user
        employee      = Employee.objects.get(auth_tbl=user)
        rolename      = employee.role.name.lower()
        # if rolename == 'admin' or  rolename == 'hr':
        #     request_list = LeaveRequest.objects.all()
        # else:
        #     request_list = LeaveRequest.objects.filter(employee=employee).all()
        context = {
            'employee'     : employee,
            'role'         : rolename,
            'title'        : "leave request"
        }
        return render(request, self.template_name, context)


class LeaveRequestAddView(AdminPanelMixin,TemplateView):
    template_name = 'leave/leave_request.html'
    today         = datetime.today()
    month         = today.month 
    year          = today.year
    firstnlast_d  = calendar.monthrange(year,month) 
    from_date     = datetime.strptime(str(year)+"-"+str(month)+"-"+str(firstnlast_d[0]),"%Y-%m-%d").date()
    to_date       = datetime.strptime(str(year)+"-"+str(month)+"-"+str(firstnlast_d[1]),"%Y-%m-%d").date()
    
    def get(self, request):
        user           = self.request.user
        employee       = Employee.objects.get(auth_tbl=user)
        rem_leaves     = LeaveBalance.objects.get(employee=employee)
        rolename       = employee.role.name.lower()
        leave_requests = LeaveRequest.objects.filter(employee=employee, from_date__gte=self.from_date, from_date__lte=self.to_date) 
        context = {
            'employee'       : employee,
            'role'           : rolename,
            'title'          : 'request leave',
            'submit'         : 'Request leave',
            'rem_leaves'     : rem_leaves,
            'leave_requests' : leave_requests,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user     = self.request.user
        employee = Employee.objects.get(auth_tbl=user)  

        try:
            from_date = datetime.strptime(request.POST['from_date'], '%Y-%m-%d').date()
            to_date   = datetime.strptime(request.POST['to_date'], '%Y-%m-%d').date()   
            leave_request = LeaveRequest.objects.create(leave_type=request.POST['leave_type'], reason_msg=request.POST['reason_msg'], from_date=from_date, to_date=to_date, available_days= request.POST['available_days'], requesting_days=request.POST['requesting_days'], employee=employee)
            messages.success(request, "Successfully added leave request")   
            return HttpResponseRedirect('/leave')
        except:
            print("error")
            messages.error(request, "There was a problem adding leave request")
            return HttpResponseRedirect('/leave') 


    # def post(self, request, user_id):
    #     user     = User.objects.get(pk=user_id)
    #     name     = request.POST['name']
    #     role     = Role.objects.get(pk=request.POST['role'])
    #     salary   = request.POST['salary']
    #     address  = request.POST['address']
    #     phone_no = request.POST['phone_no']
    #     emp_id   = request.POST['emp_id']
    #     leaves   = request.POST['leaves']
    #     auth_tbl = user
    #     employee = Employee.objects.create(name=name, role=role, salary=salary, address=address, phone_no=phone_no, emp_id=emp_id, leaves=leaves, auth_tbl=auth_tbl)
    #     return HttpResponseRedirect('/')	