
from rest_framework import serializers

from . import models

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = models.CustomUser
        fields = ['username','password','name','email','contact','emerg_name','emerg_contact','gender','email_verified','contact_verified']
