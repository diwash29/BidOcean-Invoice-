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

import xlwt

# Create your views here.


def export_expenses_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="'+str(datetime.today())+'expenses.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Invoice')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Expense Type', 'Amount', 'Bill no', 'Remarks']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    expenses_list = Expenses.objects.all()
    from_date     = request.GET.get('from_date', None)
    to_date       = request.GET.get('to_date', None)
    
    query_param = {}  
    
    if (from_date is not None and to_date is not None) and (from_date != "" and to_date != ""):
        query_param['from_date'] = from_date
        query_param['to_date']   = to_date
        to_date   = datetime.strptime(to_date,"%Y-%m-%d").date()
        from_date = datetime.strptime(from_date,"%Y-%m-%d").date()  
        expenses_list   = expenses_list.filter(expense_date__gte=from_date, expense_date__lte=to_date)
    

    expenses_list = expenses_list.order_by('-amount')    

    # paginator        = Paginator(invoice,1)
    # page             = request.GET.get('page')
    # paginatedcontent = paginator.get_page(page)

    rows = expenses_list.values_list('expense_type__expense_type', 'amount', 'bill_no', 'remarks')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

class ExpensesView(AdminOrHRPanelMixin, TemplateView):
    template_name = 'expenses/expenses.html'
    def get(self, request):
        employee         = Employee.objects.get(auth_tbl=self.request.user)
        role             = employee.role.name.lower()
        expenses_list    = Expenses.objects.all()
        expense_types    = ExpenseType.objects.all()

        from_date     = request.GET.get('from_date', None)
        to_date       = request.GET.get('to_date', None)

        query_param = {}
        if (from_date is not None and to_date is not None) and (from_date != "" and to_date != ""):
            query_param['from_date'] = from_date
            query_param['to_date']   = to_date
            to_date       = datetime.strptime(to_date,"%Y-%m-%d").date()
            from_date     = datetime.strptime(from_date,"%Y-%m-%d").date()	
            expenses_list = expenses_list.filter(expense_date__gte=from_date, expense_date__lte=to_date)
        expenses_list = expenses_list.order_by('-amount')    

        paginator        = Paginator(expenses_list,10)
        page             = request.GET.get('page')
        paginatedcontent = paginator.get_page(page)
        context = {
            'role'          : role,
            'expense_types' : expense_types,
            'expenses'      : paginatedcontent,
            'query_param'   : query_param,
        }

        return render(request, self.template_name, context)
    def post(self, request):
        try:
            delete_id = request.POST['delete']
            expenses = Expenses.objects.get(pk=delete_id)
            expenses.delete()
            messages.success(request, "Successfully deleted expenses") 
            return HttpResponseRedirect('/expenses/')	
        except:
            print(request.FILES['expense_file'])
            if request.POST['hidden_expense'] != "":
                expense_date          = datetime.strptime(request.POST['expense_date'], '%Y-%m-%d').date()   
                expenses              = Expenses.objects.get(pk = request.POST['hidden_expense'])
                expenses.expense_date = expense_date
                expenses.expense_type = ExpenseType.objects.get(pk=request.POST['expense_type'])
                expenses.amount       = request.POST['amount']
                expenses.bill_no      = request.POST['bill_no']
                expenses.remarks      = request.POST['remarks']
                expenses.expense_file = request.FILES['expense_file']
                expenses.save()
            else:
            	expense_date = datetime.strptime(request.POST['expense_date'], '%Y-%m-%d').date()   
            	expense = Expenses.objects.create(expense_date=expense_date, expense_type=ExpenseType.objects.get(pk=request.POST['expense_type']),amount=request.POST['amount'],bill_no=request.POST['bill_no'],remarks=request.POST['remarks'], added_by=Employee.objects.get(auth_tbl=self.request.user), expense_file=request.FILES['expense_file'])
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