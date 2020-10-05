from django.urls import path

from . import views

urlpatterns = [
    path('', views.LeaveRequestAddView.as_view(), name='leave'),
    path('ajax/leave_bal', views.leave_bal, name="leave_bal"),
    path('approve-leave/', views.LeaveRequestDisplayView.as_view(), name="approve_leave"),
    path('toapprove/<int:pk>', views.ToApprove.as_view(), name="to_approve"),
    path('topending/<int:pk>', views.ToPending.as_view(), name="to_pending"),
    #path('topending/', views.ToPending.as_view(), name="to_pending"),

    path('ajax/check_overlap_leave', views.check_overlap_leave, name="check_overlap_leave")

    ]