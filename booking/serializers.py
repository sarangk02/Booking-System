
from rest_framework import serializers

from . import models

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = models.CustomUser
        fields = ['username','password','name','email','contact','emerg_name','emerg_contact','gender','email_verified','contact_verified']

class SlotSerializer(serializers.ModelSerializer):
    # payment_image = serializers.ImageField(required=True)
    class Meta:
        model = models.Slot
        fields = ['date','start_time','end_time','payment_image','user']

class SlotEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Slot
        fields = ['id','date','start_time','end_time','is_booked']

