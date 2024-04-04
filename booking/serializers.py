
from rest_framework import serializers

from . import models

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomUser
        fields = ['username','name','email','contact','emerg_name','emerg_contact','gender','email_verified','contact_verified']
