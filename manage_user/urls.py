from django.urls import path
from . import views

urlpatterns = [
    path("",views.ManageUser.as_view(),name="manage_user"),
    path("ajax/user_data", views.ajax_user_data,name="edit_user_data"),

    path("ajax/username_exist", views.ajx_check_username, name="check_username")
    
]