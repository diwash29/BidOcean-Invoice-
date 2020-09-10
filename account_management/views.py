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

# class ManageAccounts(AdminOrHRPanelMixin,TemplateView):
#     template_name = 'account_management/account_management.html'
#     def get(self, request):
#         context = {
#             # 'roles': Role.objects.all(),
#             # 'title': 'Role list',
#             # 'role' : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
#         }
#         return render(request, self.template_name, context)

class ManageAccounts(AdminOrHRPanelMixin,TemplateView):
    template_name = 'account_management/account_management.html'
    def get(self, request):
        employee      = Employee.objects.get(auth_tbl=self.request.user)
        role          = employee.role.name.lower()
        employee_list = Employee.objects.all().order_by('name')
        accounts      = AccountDetails.objects.all().order_by('employee__name')
        paginator        = Paginator(accounts,10)
        page             = request.GET.get('page')
        paginatedcontent = paginator.get_page(page)
        context = {
            'role'          : role,
            'employee_list' : employee_list,
            'accounts'      : paginatedcontent
        }
        return render(request, self.template_name, context)
    def post(self, request):
        print(request.POST)
        try:
            delete_id = request.POST['delete']
            account = AccountDetails.objects.get(pk=delete_id)
            account.delete()
            messages.success(request, "Successfully deleted account") 
            return HttpResponseRedirect('/account_management/')	
        except:                        	 
            if request.POST['hidden_account'] != "":
                account            = AccountDetails.objects.get(pk = request.POST['hidden_account'])
                account.employee   = Employee.objects.get(pk=request.POST['employee'])
                account.bank       = request.POST['bank']
                account.acc_no     = request.POST['acc_no']
                account.other_bank = request.POST['other_bank']
                account.ifsc_other = request.POST['ifsc_other']
                account.save()
                messages.success(request, "Successfully edited account")
            else:
                account = AccountDetails.objects.create(employee=Employee.objects.get(pk=request.POST['employee']), bank=request.POST['bank'], acc_no=request.POST['acc_no'], other_bank=request.POST['other_bank'], ifsc_other=request.POST['ifsc_other'])
                messages.success(request, "Successfully added account")
        return HttpResponseRedirect('/account_management/')	        

def ajax_account_data(request):
    edit_id = request.GET.get('edit_id', None)
    account = AccountDetails.objects.get(pk=edit_id)
    
    data = {'id':account.pk, 'employee':account.employee.pk, 'bank':account.bank, 'acc_no':account.acc_no, 'other_bank':account.other_bank, 'ifsc_other':account.ifsc_other }
    return JsonResponse(data)        