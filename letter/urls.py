from django.urls import path
from . import views

app_name = "letter"

urlpatterns = [
    path("",views.employeeList,name="employee-list"),
    path("add/",views.createEmployee,name="add-employee"),
    path("pdfGenerate/<str:pk>/",views.generatePDF,name="pdf-generate"),
]