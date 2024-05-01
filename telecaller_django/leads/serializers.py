from rest_framework import serializers
from .models import (
  LogRegister_Details, Leads, Leads_assignto_tc, EmployeeRegister_Details
)


class  RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model =  LogRegister_Details
        fields = "__all__"

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)        

class LeadsAssignToTcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads_assignto_tc
        fields = '__all__'

class LeadsAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leads_assignto_tc
        fields = "__all__"


class  LeadsSerializers(serializers.ModelSerializer):
    class Meta:
        model =  Leads
        fields = "__all__"

class EmployeeRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeRegister_Details
        fields = "__all__"

