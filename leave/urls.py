from django.urls import path

from . import views

urlpatterns = [
    path('', views.LeaveRequestAddView.as_view(), name='leave'),
    path('ajax/leave_bal', views.leave_bal, name="leave_bal"),
    path('request-list/', views.LeaveRequestDisplayView.as_view(), name="leave_request_list"),
    ]