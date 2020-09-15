from django.urls import path
from . import views

urlpatterns = [
    path("",views.Expenses.as_view(),name="expenses"),
    
]