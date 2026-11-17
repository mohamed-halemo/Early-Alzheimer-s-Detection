from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from .serializers import LogInSerializer,SignUpSerializer
from .models import User

# Create your views here.
#User login
#sign up user
class SignUpView(generics.GenericAPIView):
    authentication_classes=[]
    serializer_class = SignUpSerializer
    #POST for user signing up
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        #Setting email message
        user = User.objects.get(email=user_data['email'])

        return Response(user_data, status=status.HTTP_201_CREATED)

    
class LoginView(generics.GenericAPIView):
    authentication_classes=[]
    serializer_class = LogInSerializer

    #POST
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)