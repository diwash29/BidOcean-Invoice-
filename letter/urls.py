from django.urls import path
from . import views

app_name = "letter"

urlpatterns = [
    path("",views.generate_pdf,name="pdf-generate"),
]