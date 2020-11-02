from django.urls import path
from . import views

app_name = "letter"

urlpatterns = [
    path("",views.employeeList,name="joinee_list"),
    path("add/",views.createEmployee,name="add_joinee"),
    path("edit/<int:pk>",views.editEmployee,name="edit_joinee"),
    path("pdfGenerate/<str:pk>/",views.generatePDF,name="pdf-generate"),

    path("ajax/get_user_data", views.ajax_get_user_data,name="get_user_data"),
]