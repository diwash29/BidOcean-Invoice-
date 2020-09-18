from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from user_invoice.models import Role, Employee
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, View
from django.contrib import messages
from .forms import ExpenseTypeAddForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from user_invoice.mixin import AdminOrHRPanelMixin, AdminPanelMixin, IRPanelMixin, BRPanelMixin, FixedPanelMixin
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q
import calendar
from django.http import JsonResponse

# Create your views here.

class ExpensesView(AdminOrHRPanelMixin, TemplateView):
    template_name = 'expenses/expenses.html'
    def get(self, request):
        employee         = Employee.objects.get(auth_tbl=self.request.user)
        role             = employee.role.name.lower()
        expenses_list    = Expenses.objects.all()
        expense_types    = ExpenseType.objects.all()
        paginator        = Paginator(expenses_list,10)
        page             = request.GET.get('page')
        paginatedcontent = paginator.get_page(page)
        context = {
            'role'          : role,
            'expense_types' : expense_types,
            'expenses'      : paginatedcontent,
        }

        return render(request, self.template_name, context)
    def post(self, request):
        print(request.POST)
        try:
            delete_id = request.POST['delete']
            expenses = Expenses.objects.get(pk=delete_id)
            expenses.delete()
            messages.success(request, "Successfully deleted expenses") 
            return HttpResponseRedirect('/expenses/')	
        except:
            if request.POST['hidden_expense'] != "":
                expense_date          = datetime.strptime(request.POST['expense_date'], '%Y-%m-%d').date()   
                expenses              = Expenses.objects.get(pk = request.POST['hidden_expense'])
                expenses.expense_date = expense_date
                expenses.expense_type = ExpenseType.objects.get(pk=request.POST['expense_type'])
                expenses.amount       = request.POST['amount']
                expenses.bill_no      = request.POST['bill_no']
                expenses.remarks      = request.POST['remarks']
                expenses.save()
            else:
            	expense_date = datetime.strptime(request.POST['expense_date'], '%Y-%m-%d').date()   
            	expense = Expenses.objects.create(expense_date=expense_date, expense_type=ExpenseType.objects.get(pk=request.POST['expense_type']),amount=request.POST['amount'],bill_no=request.POST['bill_no'],remarks=request.POST['remarks'], added_by=Employee.objects.get(auth_tbl=self.request.user))
        return HttpResponseRedirect('/expenses/')    	



def ajax_expenses_data(request):
    edit_id = request.GET.get('edit_id', None)
    expense = Expenses.objects.get(pk=edit_id)
    
    data = {'id':expense.pk, 'expense_date':expense.expense_date, 'expense_type':expense.expense_type.pk, 'amount':expense.amount, 'bill_no':expense.bill_no, 'remarks':expense.remarks}
    return JsonResponse(data)  



class ExpenceTypeDisplayView(AdminOrHRPanelMixin,TemplateView):
    template_name = 'expenses/expense_type_list.html'
    def get(self, request):
        context = {
            'expense_type': ExpenseType.objects.all(),
            'title'       : 'ExpenseType list',
            'role'        : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
        }
        return render(request, self.template_name, context)



class ExpenseTypeAddView(AdminOrHRPanelMixin,TemplateView):
    template_name = 'expenses/add_expense_type.html'
    def get(self, request):
        expensetype_form = ExpenseTypeAddForm()
        context = {
            'expensetype_form' : expensetype_form,
            'submit'           : 'Add Expence Type',
            'title'            : 'Add expense type',
            'role'             : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        expensetype_form = ExpenseTypeAddForm(request.POST)
        if expensetype_form.is_valid():
            expensetype = expensetype_form.save()
            expensetype.added_by = Employee.objects.get(auth_tbl=self.request.user)
            expensetype.save()
            messages.success(request, "Successfully created new Expense type")
            return HttpResponseRedirect('/expenses/expensetype-list/')
        else:
            print(expensetype_form.errors)
            messages.error(request, "There was a problem adding the expense type")
            return render(request, self.template_name, {
                'expensetype_form'   : expensetype_form,
                'submit'             : 'Add Expence Type',
                'title'              : 'Add expence type',
                'role'               : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
            })	

class ExpenseTypeEditView(AdminOrHRPanelMixin,TemplateView):
    template_name = 'expenses/add_expense_type.html'
    def get(self, request, pk):
        expensetype      = ExpenseType.objects.get(id=pk)
        expensetype_form = ExpenseTypeAddForm(instance=expensetype)
        context = {
        	'selected_expense' : expensetype,
            'expensetype_form' : expensetype_form,
            'submit'           : 'Edit Expense Type',
            'title'            : 'Edit expense type',
            'role'             : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        expensetype      = ExpenseType.objects.get(id=pk)
        expensetype_form = ExpenseTypeAddForm(request.POST, instance=expensetype)
        if expensetype_form.is_valid():
            expensetype = expensetype_form.save()
            messages.success(request, "Successfully edited Expense Type")            
            return HttpResponseRedirect('/expenses/expensetype-list/')    
        else:
            messages.error(request, "There was a problem updating the expensetype")
            return render(request, self.template_name, {
            	'selected_expense' : expensetype,
                'expensetype_form' : expensetype_form,
                'submit'           : 'Edit Expense Type',
                'title'            : 'Edit expense type',
                'role'             : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
            })

class ExpenseTypeDeleteView(AdminPanelMixin, TemplateView):
	def get(self, request, pk):
		expensetype = ExpenseType.objects.get(pk=pk)
		expensetype.delete()
		messages.success(request, "Successfully deleted expense type")
		return HttpResponseRedirect('/expenses/expensetype-list/') 	