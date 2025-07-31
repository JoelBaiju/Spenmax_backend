# serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from user.models import CustomUser
from rest_framework.exceptions import ValidationError

class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        
        user = authenticate(username=username, password=password)

        if user:
            if not user.block:
                data['user'] = user
            else:
                raise serializers.ValidationError("Your account is has been blocked")
        else:
            raise serializers.ValidationError("Invalid username or password.")

        return data
   
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    type = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'type']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        user_type = validated_data['type']

        existing_user = CustomUser.objects.filter(username=username).first()
        if existing_user:
            raise serializers.ValidationError('A user with this username already exists.')

        user = CustomUser.objects.create(
            username=username,
            user_type=user_type,
            is_active=True  
        )
        user.set_password(password)
        user.save()
        return user

class PasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=128, write_only=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Password and Confirm Password do not match")

        return data

class PasswordChangeSerializer(serializers.Serializer):

    old_password = serializers.CharField(write_only = True)
    new_password = serializers.CharField(write_only = True)

class ValidateEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["username"]
        
    



