from django.urls import path
from .views import RegisterAPIView,LeadDetail, UserLogin, LeadsAssignToTcAPIView, FolowUpLeads, LeadsListView,  TodaysLeadView,LeadsAssigntoTcView
urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', UserLogin.as_view(), name='login'),
    path('leadassign', LeadsAssignToTcAPIView.as_view(), name='lead'),
    path('followlead/<int:tc_id>/', FolowUpLeads.as_view(), name='followlead'),
    path('leadslist/<int:tc_id>/', LeadsListView.as_view(), name='listlead'),
    path('todaylead/<int:tc_id>/', TodaysLeadView.as_view(), name='todaylead'),
    path('post-leadassign/<int:tc_id>/', LeadsAssigntoTcView.as_view(), name='leads_assignto_tc'),
    path('lead/<int:pk>/', LeadDetail.as_view(), name='lead-detail'),
]

