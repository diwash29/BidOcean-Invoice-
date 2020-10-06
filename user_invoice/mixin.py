from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Employee


class AdminPanelMixin(LoginRequiredMixin, UserPassesTestMixin):
    """ Mixin ensures that the views to which this mixin is added can only be accessed after logging in and can only
        be accessed by editors(is_staff=True) or superusers(is_superuser=True)"""
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_active

class OnlyAdminPanelMixin(LoginRequiredMixin, UserPassesTestMixin):
    """ Mixin ensures that the views to which this mixin is added can only be accessed after logging in and can only
        be accessed by editors(is_staff=True) or superusers(is_superuser=True)"""
    login_url = 'login'

    def test_func(self):
        user     = self.request.user
        employee = Employee.objects.get(auth_tbl=user)
        return employee.role.name.lower() == 'admin'



class AdminOrHRPanelMixin(LoginRequiredMixin, UserPassesTestMixin):
    """ Mixin ensures that the views to which this mixin is added can only be accessed after logging in and can only
        be accessed by editors(is_staff=True) or superusers(is_superuser=True)"""
    login_url = 'login'

    def test_func(self):
        user     = self.request.user
        employee = Employee.objects.get(auth_tbl=user)
        return employee.role.name.lower() == 'admin' or employee.role.name.lower() == 'hr'
        # return self.request.user.is_staff or self.request.user.is_superuser

class AdminOrAccountsPanelMixin(LoginRequiredMixin, UserPassesTestMixin):
    """ Mixin ensures that the views to which this mixin is added can only be accessed after logging in and can only
        be accessed by editors(is_staff=True) or superusers(is_superuser=True)"""
    login_url = 'login'

    def test_func(self):
        user     = self.request.user
        employee = Employee.objects.get(auth_tbl=user)
        return employee.role.name.lower() == 'admin' or employee.role.name.lower() == 'accounts'        

class AdminOrHROrAccountsPanelMixin(LoginRequiredMixin, UserPassesTestMixin):
    """ Mixin ensures that the views to which this mixin is added can only be accessed after logging in and can only
        be accessed by editors(is_staff=True) or superusers(is_superuser=True)"""
    login_url = 'login'

    def test_func(self):
        user     = self.request.user
        employee = Employee.objects.get(auth_tbl=user)
        return employee.role.name.lower() == 'admin' or employee.role.name.lower() == 'hr' or employee.role.name.lower() == 'accounts'
        # return self.request.user.is_staff or self.request.user.is_superuser  


class AdminOrHROrManagerPanelMixin(LoginRequiredMixin, UserPassesTestMixin):
    """ Mixin ensures that the views to which this mixin is added can only be accessed after logging in and can only
        be accessed by editors(is_staff=True) or superusers(is_superuser=True)"""
    login_url = 'login'

    def test_func(self):
        user     = self.request.user
        employee = Employee.objects.get(auth_tbl=user)
        return employee.role.name.lower() == 'admin' or employee.role.name.lower() == 'hr' or employee.is_manager == 1


class IRPanelMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'login'

    def test_func(self):
        user     = self.request.user
        employee = Employee.objects.get(auth_tbl=user)
        return employee.role.name.lower() == 'admin' or employee.role.name.lower() == 'hr' or employee.role.name.lower() == 'ir' 
        # return self.request.user.is_staff or self.request.user.is_superuser         

class BRPanelMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'login'

    def test_func(self):
        user     = self.request.user
        employee = Employee.objects.get(auth_tbl=user)
        return employee.role.name.lower() == 'admin' or employee.role.name.lower() == 'hr' or employee.role.name.lower() == 'br' 

class FixedPanelMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = 'login'

    def test_func(self):
        user     = self.request.user
        employee = Employee.objects.get(auth_tbl=user)
        return employee.role.name.lower() == 'admin' or employee.role.name.lower() == 'hr' or employee.role.name.lower() == 'fixed' or employee.role.name.lower() == 'accounts' 