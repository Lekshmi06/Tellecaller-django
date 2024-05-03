from django.shortcuts import render

from datetime import datetime, timedelta, date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .models import LogRegister_Details, Leads_assignto_tc, Leads
from .serializers import LoginSerializer, RegisterSerializers, LeadsAssignToTcSerializer, LeadsSerializers

from django.contrib.auth import authenticate

class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        user = LogRegister_Details.objects.all()
        serializer = RegisterSerializers(user, many = True)
        return Response(serializer.data)
    



class UserLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            # Check if user exists
            user = LogRegister_Details.objects.filter(log_username=username).first()
            if user is None:
                return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                expiration_time = datetime.utcnow() + timedelta(days=1)
                token = RefreshToken.for_user(user)

                # Creating token with payload
                token['name'] = user.username
                token['id'] = user.id

                return Response({'token': str(token), 'access': str(token.access_token), 'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class UserLoginView(APIView):
   
    
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)

#         if serializer.is_valid():
#             log_username = serializer.validated_data.get('username')
#             log_password = serializer.validated_data.get('password')

#             user = authenticate(request, username=log_username, password=log_password)

#             if user is not None:
              
#                 return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LeadsAssignToTcAPIView(APIView):
    # def get(self, request, *args, **kwargs):
    #     leads_assignments = Leads_assignto_tc.objects.filter()
    #     serializer = LeadsAssignToTcSerializer(leads_assignments, many=True)
    #     return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = LeadsAssignToTcSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             log_username = serializer.validated_data['log_username']
#             log_password = serializer.validated_data['log_password']
#             user = LogRegister_Details.objects.filter(log_username=log_username, log_password=log_password).first()
#             if user:
#                 return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LeadsListView(APIView):
    serializer_class = LeadsSerializers

    def get(self, request, *args, **kwargs):
        tc_id = self.kwargs['tc_id']  # Assuming you pass TC_Id in the URL
        leads_ids = Leads_assignto_tc.objects.filter(TC_Id=tc_id).values_list('leadId', flat=True)
        leads = Leads.objects.filter(id__in=leads_ids)
        serializer = self.serializer_class(leads, many=True)
        return Response(serializer.data)
    
class FolowUpLeads(APIView):
    serializer_class = LeadsSerializers

    def get(self, request, *args, **kwargs):
        tc_id = self.kwargs['tc_id']  # Assuming you pass TC_Id in the URL
        leads_ids = Leads_assignto_tc.objects.filter(TC_Id=tc_id, Status=1).values_list('leadId', flat=True)
        leads = Leads.objects.filter(id__in=leads_ids)
        serializer = self.serializer_class(leads, many=True)
        return Response(serializer.data)    



# class TodaysLeadView(APIView):
#     serializer_class = LeadsSerializers

#     def get(self, request, tc_id):
#         today = date.today()
#         leads = Leads_assignto_tc.objects.filter(
#             TC_Id=tc_id,
#             Update_Date__date=today,
#         ) | Leads_assignto_tc.objects.filter(
#             TC_Id=tc_id,
#             Next_update_date__date=today,
#         )
#         serialized_leads = self.serializer_class(leads, many=True)
#         return Response(serialized_leads.data)

class TodaysLeadView(APIView):
    serializer_class = LeadsSerializers

    def get(self, request, tc_id):
        today = date.today()
        leads = Leads_assignto_tc.objects.filter(
            TC_Id=tc_id,
            Update_Date=today,
        ) | Leads_assignto_tc.objects.filter(
            TC_Id=tc_id,
            Next_update_date=today,
        )
        serialized_leads = self.serializer_class(leads, many=True)
        return Response(serialized_leads.data)


