from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from . import serializers
from django.contrib.auth import authenticate
from account.renderers import UserJSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions

# Generate Token Manually


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserJSONRenderer]

    def post(self, request, formate=None):
        serializer = serializers.UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            if user:
                json = serializer.data
                return Response({'msg': 'Registration Success', 'token': token, 'data': json}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = [UserJSONRenderer]

    def post(self, request, formate=None):
        serializer = serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'msg': 'Login Success', 'token': token}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'msg': ['Email or Password is not Valid']}}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, formate=None):
        user = request.user
        serializer = serializers.UserProfileSerializer(user)
        return Response({'msg': 'Data Fetch Success', 'data': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, formate=None):
        user = request.user
        serializer = serializers.UserProfileSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Profile Updated Success', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, formate=None):
        user = request.user
        user.delete()
        return Response({'msg': 'User Deleted Success'}, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, formate=None):

        userCred = {
            'password': request.data.get('old_password'),
            'email': request.user.email,
        }

        loginSerializer = serializers.UserLoginSerializer(data=userCred)

        if loginSerializer.is_valid(raise_exception=True):
            email = loginSerializer.data.get('email')
            password = loginSerializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                serializer = serializers.UserChangePasswordSerializer(
                    data=request.data, context={'user': user})
                serializer.is_valid(raise_exception=True)
                return Response({'msg': 'Password Changed Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'msg': ['Old Password is not Valid']}}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendEmailView(APIView):
    renderer_classes = [UserJSONRenderer]

    def post(self, request, formate=None):
        serializer = serializers.SendEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Password Reset Link Sent Success', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    renderer_classes = [UserJSONRenderer]

    def post(self, request, uid, token, formate=None):
        serializer = serializers.ResetPasswordSerializer(data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Password Reset Success'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
