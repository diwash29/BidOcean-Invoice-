from django.urls import path
from . import views

urlpatterns = [
    path("",views.ExpensesView.as_view(),name="expenses"),
    path("ajax/expenses_data", views.ajax_expenses_data,name="edit_expenses_data"),

    path('expensetype-add/',views.ExpenseTypeAddView.as_view(),name='expensetype_add'),
    path('expensetype-list/',views.ExpenceTypeDisplayView.as_view(),name='expensetype_list'),
    path('expensetype-edit/<int:pk>',views.ExpenseTypeEditView.as_view(),name='expensetype_edit'),
    path('expensetype-delete/<int:pk>',views.ExpenseTypeDeleteView.as_view(),name='expensetype_delete'),

    path('export/csv/', views.export_expenses_xls, name='export_expenses_xls'),
    
]