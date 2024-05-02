from django.urls import path
from .views import RegisterAPIView, UserLogin, LeadsAssignToTcAPIView, FolowUpLeads, LeadsListView
urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', UserLogin.as_view(), name='login'),
    path('leadassign', LeadsAssignToTcAPIView.as_view(), name='lead'),
     path('followlead/<int:tc_id>/', FolowUpLeads.as_view(), name='followlead'),
    path('leadslist/<int:tc_id>/', LeadsListView.as_view(), name='listlead'),
]