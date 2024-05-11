from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = models.CustomUser
        fields = ['username','password','name','email','contact','emerg_name','emerg_contact','gender']

class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ['name','email','contact','emerg_name','emerg_contact','gender']

class SlotSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = models.Slot
        fields = ['id','date','start_time','end_time','payment_image','user']

class DeletedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = models.DeletedSlot
        fields = ['id','date','start_time','end_time','payment_image','user','reason','deletiontime']

class UserSlotEditSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = models.Slot
        fields = ['id','date','start_time','end_time']

class DeletedSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeletedSlot
        fields = ['reason']
