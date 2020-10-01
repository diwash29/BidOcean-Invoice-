from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='user_invoice-home'),
    path('employee/<int:user_id>', views.EmployeeAddView.as_view(), name='employee_add'),
    path('ir/',views.IrAddView.as_view(),name='ir'),
    path('br/',views.BrAddView.as_view(),name='br'),
    path('fixed/',views.FixedAddView.as_view(),name='fixed'),

    path('error/',views.ErrorMessageView.as_view(),name='error_msg'), 
    
    path('rate-add/',views.RateAddView.as_view(),name='rate_add'),
    path('rate-list/',views.RateDisplayView.as_view(),name='rate_list'),
    path('rate-edit/<int:pk>',views.RateEditView.as_view(),name='rate_edit'),
    path('rate-pull/<int:pk>',views.RatePullView.as_view(),name='rate_pull'),
    path('rate-approve/<int:pk>',views.RateApproveView.as_view(),name='rate_approve'),

    path('role-add/',views.RoleAddView.as_view(),name='role_add'),
    path('role-list/',views.RoleDisplayView.as_view(),name='role_list'),
    path('role-edit/<int:pk>',views.RoleEditView.as_view(),name='role_edit'),
    path('role-delete/<int:pk>',views.RoleDeleteView.as_view(),name='role_delete'),

    path('employee-list/',views.EmployeeDisplayView.as_view(),name='employee_list'),
    path('employee-edit/<int:pk>',views.EmployeeEditView.as_view(),name='employee_edit'),
    path('employee-delete/<int:pk>',views.EmployeeDeleteView.as_view(),name='employee_delete'),

    path('invoice-list/', views.InvoiceDisplayView.as_view(), name='invoice_list' ),
    
    path('ir/<int:pk>', views.IrEditView.as_view(), name='edit_ir'),
    path('br/<int:pk>', views.BrEditView.as_view(), name='edit_br'),
    path('fixed/<int:pk>', views.FixedEditView.as_view(), name='edit_fixed'),

    path('export/csv/', views.export_invoice_xls, name='export_invoice_xls'),

    path('change-password/', views.ChangePassword.as_view(), name='change_password'),

    path('ajax/get_leave/', views.ajax_get_leave, name='ajax_get_leave')
]