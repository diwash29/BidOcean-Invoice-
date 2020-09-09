from django.urls import path
from . import views

urlpatterns = [
    path("",views.ManageUser.as_view(),name="manage_user"),
    
]