from django.urls import path

from . import views

urlpatterns = [
    path('', views.LeaveRequestAddView.as_view(), name='leave'),
    path('ajax/leave_bal', views.leave_bal, name="leave_bal"),
    path('approve-leave/', views.LeaveRequestDisplayView.as_view(), name="approve_leave"),
    ]