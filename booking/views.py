from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models

class IndexView(APIView):
    def get(self, request):
        # return all available paths
        payload = {
            '/': 'get all available paths',
            '/token': 'get access and refresh token',
            '/token/refresh': 'refresh your acccess token',
            '/users': {'GET': 'get details of user (Authorized only)', 'POST': 'create a new user', 'PATCH': 'update user details (Authorized only)', 'DELETE': 'delete user (Authorized only)'},
            '/manage-slot (Authorized only)': {'GET':'get details of slots as per User and Staff','POST': 'book a new slot','PATCH': 'update slot details (Staff)', 'DELETE': 'delete slot'},
            '/slot-requests (Authorized only)': {'GET':'slot-requests as per User and Staff', 'PATCH': 'book a slot (Staff)', 'DELETE': 'delete slot (Staff)'},
        }
        return Response(payload, status=200)

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

class Slots(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.is_staff:
            approved = models.Slot.objects.filter(is_booked=True)
            pending = models.Slot.objects.filter(is_booked=False)
            # rejected = models.Slot.objects.all()
        else:
            approved = models.Slot.objects.filter(user=user, is_booked=True)
            pending = models.Slot.objects.filter(user=user, is_booked=False)
            # rejected = models.Slot.objects.filter(user=user)
        approved_serializer = serializers.SlotSerializer(approved, many=True)
        pending_serializer = serializers.SlotSerializer(pending, many=True)
        # rejected_serializer = serializers.SlotSerializer(rejected, many=True)
        payload = {
            'approved': approved_serializer.data,
            'pending': pending_serializer.data,
            # 'rejected': rejected_serializer.data
        }
        return Response(payload)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer = serializers.SlotSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def patch(self, request):
        if request.user.is_staff:
            data = request.data
            slot = models.Slot.objects.get(id=data.get('id'))
            serializer = serializers.SlotEditSerializer(slot, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({'message': 'Slot booked successfully!'})
        else:
            return Response({'message': 'You are not authorized to perform this action!'}, status=403)

    def delete(self, request):
        data = request.data
        slot = models.Slot.objects.get(id=data.get('id'), user=request.user)
        slot.delete()
        return Response({'message': 'Slot deleted successfully!'})

class SlotReqeusts(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.is_staff:
            slots = models.Slot.objects.filter(is_booked=False)
        else:
            slots = models.Slot.objects.filter(user=user)
        serializer = serializers.SlotSerializer(slots, many=True)
        return Response(serializer.data)

    def patch(self, request):
        if request.user.is_staff:
            data = request.data
            slot = models.Slot.objects.get(id=data.get('id'))
            slot.is_booked = True
            slot.save()
            return Response({'message': 'Slot booked successfully!'})
        else:
            return Response({'message': 'You are not authorized to perform this action!'}, status=403)

    def delete(self, request):
        if request.user.is_staff:
            data = request.data
            slot = models.Slot.objects.get(id=data.get('id'))
            # shift this slot to new table called 'DeletedSlot'
            # models.DeletedSlot.objects.create(
            #     date=slot.date,
            #     start_time=slot.start_time,
            #     end_time=slot.end_time,
            #     payment_image=slot.payment_image,
            #     user=slot.user,
            #     request_time=slot.request_time,
            #     is_booked=slot.is_booked,
            #     is_booked_time=slot.is_booked_time,
            #     reason=data.get('reason')
            # )
            slot.delete()
            return Response({'message': 'Slot deleted successfully!'})
        else:
            return Response({'message': 'You are not authorized to perform this action!'}, status=403)

# {
# "id":2,
# "is_booked":true
# }

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
#     "date": "2021-10-10",
#     "start_time": "08:00:00",
#     "end_time": "09:00:00",
#     "payment_image": null
# }
