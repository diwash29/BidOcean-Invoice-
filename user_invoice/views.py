from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import EmployeeForm, RoleAddForm, RateAddForm
from django.contrib.auth.models import User
from .mixin import AdminOrHRPanelMixin, AdminPanelMixin
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
        context = {
            'employees' : Employee.objects.all(),
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
        role_form = RoleAddForm(request.POST)
        if role_form.is_valid():
            role = role_form.save()
            messages.success(request, "Successfully created new Role")
            return HttpResponseRedirect('/role-list/')
        else:
            print(role_form.errors)
            messages.error(request, "There was a problem creating the Role")
            return render(request, self.template_name, {'role_form': role_form, 'submit': 'Add Role'})
        # user     = User.objects.get(pk=user_id)
        # name     = request.POST['name']
        # role     = Role.objects.get(pk=request.POST['role'])
        # salary   = request.POST['salary']
        # address  = request.POST['address']
        # phone_no = request.POST['phone_no']
        # leaves   = request.POST['leaves']
        # auth_tbl = user
      #  employee = Employee.objects.create(name=name, role=role, salary=salary, address=address, phone_no=phone_no, leaves=leaves, auth_tbl=auth_tbl)
        return HttpResponseRedirect('/')

class BrAddView(AdminPanelMixin,TemplateView):
    template_name='user_invoice/br.html'

    def get(self, request):
        user          = request.user
        employee      = Employee.objects.get(auth_tbl=user)
        # employee_form = EmployeeForm()
        context = {
            # 'employee_form': employee_form,
            'employee'     : employee,
            'submit'       : 'Submit Invoice'
        }
        return render(request, self.template_name, context)

    def post(self, request):
        # user     = User.objects.get(pk=user_id)
        # name     = request.POST['name']
        # role     = Role.objects.get(pk=request.POST['role'])
        # salary   = request.POST['salary']
        # address  = request.POST['address']
        # phone_no = request.POST['phone_no']
        # leaves   = request.POST['leaves']
        # auth_tbl = user
      #  employee = Employee.objects.create(name=name, role=role, salary=salary, address=address, phone_no=phone_no, leaves=leaves, auth_tbl=auth_tbl)
        return HttpResponseRedirect('/')        

class FixedAddView(AdminPanelMixin, TemplateView):
    template_name='user_invoice/fixed.html'

    def get(self, request):
        user          = request.user
        employee      = Employee.objects.get(auth_tbl=user)
        # employee_form = EmployeeForm()
        context = {
            # 'employee_form': employee_form,
            'employee'     : employee,
            'submit'       : 'Submit Invoice'
        }
        return render(request, self.template_name, context)

    def post(self, request):
        # user     = User.objects.get(pk=user_id)
        # name     = request.POST['name']
        # role     = Role.objects.get(pk=request.POST['role'])
        # salary   = request.POST['salary']
        # address  = request.POST['address']
        # phone_no = request.POST['phone_no']
        # leaves   = request.POST['leaves']
        # auth_tbl = user
      #  employee = Employee.objects.create(name=name, role=role, salary=salary, address=address, phone_no=phone_no, leaves=leaves, auth_tbl=auth_tbl)
        return HttpResponseRedirect('/')                