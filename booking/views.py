from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models

class IndexView(APIView):
    def get(self, request):
        # return all available paths
        return Response({
            'paths': [
                '/',
                '/user/',
                '/user/add',
            ]}
        )

class UserCreate(APIView):
    def post(self, request):
        data = request.data
        serializer = serializers.UserSerializer(data=data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(data.get('password'))
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class UserEdit(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)

    def get_permissions(self):
        if self.request.method == 'POST':
            return []
        return super().get_permissions()
    def post(self, request):
        data = request.data
        serializer = serializers.UserSerializer(data=data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(data.get('password'))
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def patch(self, request):
        data = request.data
        user = models.CustomUser.objects.get(username=request.user)
        serializer = serializers.UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            if data.get('password'):
                serializer.validated_data['password'] = make_password(data.get('password'))
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        user = models.CustomUser.objects.get(username=request.user)
        user.delete()
        return Response({'message': 'User deleted successfully!'})


# {
#     "username": "sarangkulkarniii",
#     "password": "asdf@1234",
#     "name": "Sarang Kulkarni",
#     "email": "sarangakulkarni02@gmail.com",
#     "contact": "9421062179",
#     "emerg_name": "Shreyas Kulkarni",
#     "emerg_contact": "9881074107",
#     "gender": "M",
#     "email_verified": False,
#     "contact_verified": False
# }

# {
#     "username": "shreyaskulkarniii",
#     "password": "asdf@1234",
#     "name": "Shreyas Kulkarni",
#     "email": "ishreyas1998@gmail.com",
#     "contact": "988174107",
#     "emerg_name": "Sarang Kulkarni",
#     "emerg_contact": "9421062179",
#     "gender": "M",
#     "email_verified": False,
#     "contact_verified": False
# }