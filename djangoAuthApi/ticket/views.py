from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from . import serializers
from django.contrib.auth import authenticate
from account.renderers import UserJSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from account.models import User


# Create your views here.

class TicketView(APIView):
    renderer_classes = [UserJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    # def get(self, request, formate=None):
    #     user = request.user
    #     serializer = serializers.TicketSerializer(user)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def put(self, request, formate=None):
    #     user = request.user
    #     serializer = serializers.TicketSerializer(user, data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response({'msg': 'Profile Updated Success', 'data': serializer.data}, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, formate=None):
        user = request.user
        ticket = request.data
        serializer = serializers.TicketSerializer(data=ticket)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg': 'Ticket Generated Success', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
