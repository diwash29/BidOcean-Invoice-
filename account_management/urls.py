from django.urls import path
from . import views

urlpatterns = [
    path("",views.ManageAccounts.as_view(),name="account_management"),
    path("ajax/account_data", views.ajax_account_data,name="edit_account_data"),
    
]