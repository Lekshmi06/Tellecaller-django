from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import (
  CustomUser, Leads, Leads_assignto_tc, EmployeeRegister_Details
)


class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(RegisterSerializers, self).create(validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required.")

        return data 

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

