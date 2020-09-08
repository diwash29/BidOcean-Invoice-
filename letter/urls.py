from django.urls import path
from . import views

app_name = "letter"

urlpatterns = [
    path("",views.employeeList,name="joinee_list"),
    path("add/",views.createEmployee,name="add_joinee"),
    path("pdfGenerate/<str:pk>/",views.generatePDF,name="pdf-generate"),
]