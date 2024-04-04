from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers
from . import models

class IndexView(APIView):
    def get(self, request):
        return Response({'message': 'Hello, world!'})

class UserView(APIView):
    def get(self, request):
        users = models.CustomUser.objects.all()
        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = serializers.UserSerializer(data=data)
        if serializer.is_valid():
            serializer.password = data.get('password')
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

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