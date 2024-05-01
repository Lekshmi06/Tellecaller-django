from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LogRegister_Details, Leads_assignto_tc
from .serializers import LoginSerializer, RegisterSerializers, LeadsAssignToTcSerializer

from django.contrib.auth import authenticate

class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
   
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
              
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LeadsAssignToTcAPIView(APIView):
    def get(self, request, *args, **kwargs):
        leads_assignments = Leads_assignto_tc.objects.all()
        serializer = LeadsAssignToTcSerializer(leads_assignments, many=True)
        return Response(serializer.data)

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
