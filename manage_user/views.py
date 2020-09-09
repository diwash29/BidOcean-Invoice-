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
        context = {
            # 'roles': Role.objects.all(),
            # 'title': 'Role list',
            # 'role' : Employee.objects.get(auth_tbl=self.request.user).role.name.lower()
        }
        return render(request, self.template_name, context)