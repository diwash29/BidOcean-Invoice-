from django.urls import path
from . import views

urlpatterns = [
    path("",views.ManageAccounts.as_view(),name="account_management"),
    
]