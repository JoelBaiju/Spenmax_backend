# views.py
from rest_framework import status , generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .serializers import UserLoginSerializer , PasswordChangeSerializer , PasswordSerializer , CustomUserSerializer , ValidateEmailSerializer  ,PasswordSerializer
from django.contrib.auth import authenticate
from user.variable import ADMIN ,VENDOR ,USER
from user.api.utils import send_confirmation_email , send_verification_email , send_forgotverificaiton_email , sendOTP
from rest_framework.decorators import api_view , permission_classes
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from shop.models import Customer
from user.models import CustomUser
from django.contrib.auth.hashers import make_password ,check_password
from django.db import transaction
from shop.api import serializers
from user.api.permissions import IsAdminUserType
import time

import os
from django.conf import settings
from django.http import FileResponse, Http404
from django.core.cache import cache

class DownloadAPKView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # Path to the APK file
        apk_path = os.path.join(settings.STATIC_ROOT, 'spenmax.apk')

        if not os.path.exists(apk_path):
            raise Http404("File not found.")

        # Serve the file as a download
        response = FileResponse(open(apk_path, 'rb'), as_attachment=True, filename='spenmax.apk')
        return response 

class UserLoginAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        if not user.is_active:
            return Response({"not_verified":"user is not verifed yet.","user" : user.id}, status=status.HTTP_307_TEMPORARY_REDIRECT)
        login(request, user)

        existing_token = Token.objects.filter(user=user).first()
        
        response_data = {'type':user.user_type , "is_active" : user.is_active}

        if user.user_type == ADMIN:
            response_data['name'] = user.username
        elif user.user_type == VENDOR:
            response_data['name'] = user.detail_v.owner
            response_data["company_id"] = user.detail_v.id
        else:
            response_data['name'] = user.detail_c.name


        if existing_token:
            response_data['token'] = existing_token.key
        else:
            new_token, created = Token.objects.get_or_create(user=user)
            response_data['token']  =  new_token.key 
        return Response(response_data, status=status.HTTP_200_OK)

class RegisterApiView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if 'username' not in request.data or 'password' not in request.data:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.data['username']
        password= request.data["password"]
        user_serializer = CustomUserSerializer(data={'username': email , "password" :password , "type" : USER })
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        data = request.data.copy()
        data["user"] = user.id
        data["email_id"] = email
        customer_serializer = serializers.CustomerSerializer(data=data)
        customer_serializer.is_valid(raise_exception=True)
        customer = customer_serializer.save()
        #s = SessionStore()
        #s["user_id"] = user.id
        #s.create()
        #s.set_expiry(300)
        #session_key = s.session_key
        #try:
         #   send_verification_email(customer.email_id , customer.name , session_key)
        #except:
         #   return Response({'error':'there is an error in the server for sending the email to user.'}, status=status.HTTP_409_CONFLICT)
        return Response(customer_serializer.data, status=status.HTTP_201_CREATED)

class ForgotPasswordView(APIView):

    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if 'email_id' not in request.data:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.data["email_id"]
        if not CustomUser.objects.filter(username = email).exists():
            return Response({'error': 'Invalid Eamil'}, status=status.HTTP_400_BAD_REQUEST)
        #s = SessionStore()
        #s["email"] =  email
        #s.create()
        #s.set_expiry(300)
        #session_key = s.session_key

        try:
            otp = sendOTP(email )
            print(otp)
            cache.set(f"otp_{email}", otp, timeout=300)
        except:
            transaction.set_rollback(True)
            return Response({'error':'there is an error in the Server.Please Try again later.'}, status=status.HTTP_409_CONFLICT)
        return Response({"success" : "otp send successful"}, status=status.HTTP_201_CREATED)

class OtpVerifyView(APIView):
    permission_classes =[AllowAny]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        otp = request.data.get('otp', None)
        if not email or not otp:
            return Response({'error': 'Email, OTP, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        cached_otp = cache.get(f"otp_{email}")
        print(otp , cached_otp , email)
        if not cached_otp or cached_otp != otp:
            return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'otp verification successfully', 'token' : 'Asdgyhk12@lhnsTY'}, status=status.HTTP_200_OK)
 
class ResetPasswordView(APIView):
    permission_classes =[AllowAny]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        token = request.data.get('token', None)
        if not email or not token:
            return Response({'error': 'Email, OTP, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if token != "Asdgyhk12@lhnsTY":
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        try :
            obj = CustomUser.objects.get(username = email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PasswordSerializer(data= request.data)
        if serializer.is_valid(): 
            obj.set_password(serializer.validated_data["password"])
            obj.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForcedVerifyView(APIView):

    permission_classes = [IsAdminUserType]

    @transaction.atomic
    def post(self, request,pk, *args, **kwargs):

        try :
            obj = CustomUser.objects.get(pk = pk)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
        
        obj.is_active = True
        obj.save()

        if obj.user_type == VENDOR:
            obj.detail_v.is_registered = True
            obj.detail_v.save()

        return Response({"success" : "Forced verification successful."}, status=status.HTTP_201_CREATED)

class ReSendVerificationView(APIView):
    
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request,pk, *args, **kwargs):
        try :
            obj = CustomUser.objects.get(pk = pk)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
        if obj.is_active:
            return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
        s = SessionStore()
        s["user_id"] = obj.id
        s.create()
        s.set_expiry(300)
        session_key = s.session_key
        
        try:
            send_verification_email(obj.username , obj.detail_c.name , session_key)
        except:
            return Response({'error':'there is an error in the server for sending the email to user.'}, status=status.HTTP_409_CONFLICT)
        return Response({"success" : "verification send successful"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
@transaction.atomic
def verify_account(request):
    if request.method == 'POST':
        session_key = request.GET.get('id', None)
        if not session_key:
            return Response({'error': 'Invalid or expired session'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            session_data = Session.objects.get(session_key=session_key)
            user = session_data.get_decoded()
        except Session.DoesNotExist:
            return Response({'error': 'Invalid or expired session'}, status=status.HTTP_400_BAD_REQUEST)
        # if not session_data.modified + session_data.get_expiry_age() > time.time():
        #     session_data.delete()
        #     return Response({'error': 'Invalid or expired session'}, status=status.HTTP_400_BAD_REQUEST)
        if not user["user_id"]:
            session_data.delete()
            return Response({'error': 'Invalid or expired session'}, status=status.HTTP_400_BAD_REQUEST)
        u_id = user["user_id"]

        try :

            obj = CustomUser.objects.get(pk = u_id)
            obj.is_active = True
            obj.save()

            if obj.user_type == VENDOR:
                obj.detail_v.is_registered = True
                obj.detail_v.save()
            
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid or expired session'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        session_data.delete()
        return Response({'success': 'User created successfully'}, status=status.HTTP_201_CREATED)

class PasswordChangeView(generics.GenericAPIView):

    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.validated_data["old_password"]):
                user.set_password(serializer.validated_data["new_password"])
                user.save()
                return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


