from django.shortcuts import render

from datetime import datetime, timedelta, date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import CustomUser, Leads_assignto_tc, Leads
from .serializers import LoginSerializer, RegisterSerializers, LeadsAssignToTcSerializer, LeadsSerializers,EmployeeRegister_Details, LeadsWithStatusSerializer
from django.contrib.auth import authenticate

class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        user = CustomUser.objects.all()
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
            user = CustomUser.objects.filter(username=username).first()
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

class LeadsListView(APIView):
    serializer_class = LeadsWithStatusSerializer

    def get(self, request, *args, **kwargs):
        custom_user_id = self.kwargs['tc_id']
        tc_id = EmployeeRegister_Details.objects.get(logreg_id=custom_user_id)
        leads_ids = Leads_assignto_tc.objects.filter(TC_Id=tc_id).values_list('leadId', flat=True)
        leads = Leads.objects.filter(id__in=leads_ids)
        serializer = self.serializer_class(leads, many=True)
        return Response(serializer.data)



# class LeadsListView(APIView):
#     serializer_class = LeadsSerializers

#     def get(self, request, *args, **kwargs):
#         # tc_id = self.kwargs['tc_id']  # Assuming you pass TC_Id in the URL
#         custom_user_id = self.kwargs['tc_id']  # Assuming tc_id is the id of the CustomUser
#         tc_id = EmployeeRegister_Details.objects.get(logreg_id=custom_user_id)
#         leads_ids = Leads_assignto_tc.objects.filter(TC_Id=tc_id).values_list('leadId', flat=True)
#         leads = Leads.objects.filter(id__in=leads_ids)
#         serializer = self.serializer_class(leads, many=True)
#         return Response(serializer.data)
    

class FolowUpLeads(APIView):
    serializer_class = LeadsSerializers

    def get(self, request, *args, **kwargs):
        custom_user_id = self.kwargs['tc_id']  # Assuming tc_id is the id of the CustomUser
        employee_id = EmployeeRegister_Details.objects.get(logreg_id=custom_user_id)
        print( employee_id )
        leads_ids = Leads_assignto_tc.objects.filter(TC_Id=employee_id.id, Status=1).values_list('leadId', flat=True)
        leads = Leads.objects.filter(id__in=leads_ids)
        serializer = self.serializer_class(leads, many=True)
        return Response(serializer.data)
#--------------
# class LeadsAssigntoTcView(APIView):
#     def post(self, request):
#         custom_user_id = self.kwargs['tc_id']
#         tc_id = EmployeeRegister_Details.objects.get(logreg_id=custom_user_id)

#         data = request.data.copy()
#         data['TC_Id'] = tc_id # Assign the primary key of tc_id to TC_Id field

#         serializer =  LeadsAssignToTcSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LeadsAssigntoTcView(APIView):
#     def post(self, request, tc_id, format=None):
#         # Use tc_id from URL to get EmployeeRegister_Details
#         try:
#             tc_id_obj = EmployeeRegister_Details.objects.get(logreg_id=tc_id)
#         except EmployeeRegister_Details.DoesNotExist:
#             return Response({"error": "EmployeeRegister_Details not found"}, status=status.HTTP_404_NOT_FOUND)

#         # Update request data with TC_Id
#         data = request.data.copy()
#         data['TC_Id'] = tc_id_obj.pk  # Assign the primary key of tc_id_obj to TC_Id field

#         serializer = LeadsAssignToTcSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LeadsAssigntoTcView(APIView):
    def post(self, request, tc_id, format=None):
        # Get the tc_id object
        tc_id_obj = EmployeeRegister_Details.objects.get(logreg_id=tc_id)

        # Get the leadId from the request data
        lead_id = request.data.get('leadId')
        # Retrieve the Leads instance
        lead_instance = Leads.objects.get(id=lead_id)

        # Update request data with TC_Id and Leads instance
        data = request.data.copy()
        data['TC_Id'] = tc_id_obj
        data['leadId'] = lead_instance
        # Retrieve or create Leads_assignto_tc object
        leads_assign_to_tc, created = Leads_assignto_tc.objects.get_or_create(
            leadId=lead_instance, TC_Id=tc_id_obj,
            defaults=data
        )

        # Update the fields if the object already exists
        if not created:
            for key, value in data.items():
                setattr(leads_assign_to_tc, key, value)
            leads_assign_to_tc.save()

        serializer =  LeadsAssignToTcSerializer(leads_assign_to_tc)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LeadDetail(APIView):
    def get(self, request, pk):
        try:
            lead = Leads.objects.get(pk=pk)
        except Leads.DoesNotExist:
            return Response({"message": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LeadsSerializers(lead)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class TodaysLeadView(APIView):
#     serializer_class = LeadsSerializers

#     def get(self, request,tc_id):
#         custom_user_id = self.kwargs['tc_id']  # Assuming tc_id is the id of the CustomUser
#         id = EmployeeRegister_Details.objects.get(logreg_id=custom_user_id)
#         # leads_ids = Leads_assignto_tc.objects.filter(TC_Id=tc_id).values_list('leadId', flat=True)
#         print(tc_id,"tc")
#         today = date.today()
#         print(today,"date")
#         leads_ids = Leads_assignto_tc.objects.filter(
#             TC_Id=id,
#             Update_Date=today,
#         ) | Leads_assignto_tc.objects.filter(
#             TC_Id=id,
#             Next_update_date=today,
#         ).values_list('leadId', flat=True)
#         print( leads_ids, "ids")
#         leads = Leads.objects.filter(id__in=leads_ids)
#         serialized_leads = self.serializer_class(leads, many=True)
#         return Response(serialized_leads.data)


from rest_framework.response import Response

from itertools import chain

class TodaysLeadView(APIView):
    serializer_class = LeadsSerializers

    def get(self, request, tc_id):
        custom_user_id = self.kwargs['tc_id']  # Assuming tc_id is the id of the CustomUser
        id = EmployeeRegister_Details.objects.get(logreg_id=custom_user_id)
        today = date.today()

        # Filter for leads with Update_Date=today
        leads_update = Leads_assignto_tc.objects.filter(
            TC_Id=id,
            Update_Date=today,
        )

        # Filter for leads with Next_update_date=today and get leadIds
        leads_next_update = Leads_assignto_tc.objects.filter(
            TC_Id=id,
            Next_update_date=today,
        ).values_list('leadId', flat=True)

        # Get the leadIds from both querysets
        lead_ids = list(chain(leads_update.values_list('leadId', flat=True), leads_next_update))

        # Get the leads based on leadIds
        leads = Leads.objects.filter(id__in=lead_ids)

        # Serialize the leads
        serialized_leads = self.serializer_class(leads, many=True)

        return Response(serialized_leads.data)


