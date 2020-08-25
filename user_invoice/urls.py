from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='user_invoice-home'),
    path('employee/<int:user_id>', views.EmployeeAddView.as_view(), name='employee_add'),
    path('ir/',views.IrAddView.as_view(),name='ir'),
    path('br/',views.BrAddView.as_view(),name='br'),
    path('fixed/',views.FixedAddView.as_view(),name='fixed'),

    path('rate-add/',views.RateAddView.as_view(),name='rate_add'),

    path('role-add/',views.RoleAddView.as_view(),name='role_add'),
    path('role-list/',views.RoleDisplayView.as_view(),name='role_list'),
    path('role-edit/<int:pk>',views.RoleEditView.as_view(),name='role_edit'),
    
    path('employee-list/',views.EmployeeDisplayView.as_view(),name='employee_list'),
    path('employee-edit/<int:pk>',views.EmployeeEditView.as_view(),name='employee_edit'),
]