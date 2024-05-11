from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse

from . import serializers
from . import models
from . import emails

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
    # get user details
    def get(self, request):
        user = request.user
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)

    # for post request, no need of any permission
    def get_permissions(self):
        if self.request.method == 'POST':
            return []
        return super().get_permissions()

    # create a new user
    def post(self, request):
        data = request.data
        serializer = serializers.UserSerializer(data=data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(data.get('password'))
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    # update user details
    def patch(self, request):
        data = request.data
        user = models.CustomUser.objects.get(username=request.user)
        serializer = serializers.UserEditSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            if data.get('password'):
                serializer.validated_data['password'] = make_password(data.get('password'))
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # delete user
    def delete(self, request):
        user = models.CustomUser.objects.get(username=request.user)
        user.delete()
        return Response({'message': 'User deleted successfully!'})

class Slots(APIView):
    permission_classes = [IsAuthenticated]
    # get slots as per user and staff
    def get(self, request):
        user = request.user
        if user.is_staff:
            approved = models.Slot.objects.filter(is_booked=True)
            pending = models.Slot.objects.filter(is_booked=False)
            rejected = models.DeletedSlot.objects.all()
        else:
            approved = models.Slot.objects.filter(user=user, is_booked=True)
            pending = models.Slot.objects.filter(user=user, is_booked=False)
            rejected = models.Slot.objects.filter(user=user)
        approved_serializer = serializers.SlotSerializer(approved, many=True)
        pending_serializer = serializers.SlotSerializer(pending, many=True)
        rejected_serializer = serializers.DeletedSerializer(rejected, many=True)
        payload = {
            'approved': approved_serializer.data,
            'pending': pending_serializer.data,
            'rejected': rejected_serializer.data
        }
        return Response(payload)

    # book a new slot
    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer = serializers.SlotSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Details':serializer.data, 'message':'Slot Request Sent successfully!'}, status=201)
        return Response(serializer.errors, status=400)

    # update slot details (staff)
    def patch(self, request):
        if request.user.is_staff:
            data = request.data
            slot = models.Slot.objects.get(id=data.get('id'))
            serializer = serializers.UserSlotEditSerializer(slot, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({'message': 'Slot booked successfully!'})
        else:
            return Response({'message': 'You are not authorized to perform this action!'}, status=403)

class SlotReqeusts(APIView):
    permission_classes = [IsAuthenticated]
    # get slot requests as per user and staff
    def get(self, request):
        user = request.user
        if user.is_staff:
            slots = models.Slot.objects.filter(is_booked=False)
        else:
            slots = models.Slot.objects.filter(user=user)
        serializer = serializers.SlotSerializer(slots, many=True)
        return Response(serializer.data)

    # book a slot (staff)
    def post(self, request):
        try:
            data = request.data
            slot = models.Slot.objects.get(id=data.get('id'))
            deleted_slot = models.DeletedSlot.objects.create(
                date=slot.date,
                start_time=slot.start_time,
                end_time=slot.end_time,
                payment_image=slot.payment_image,
                user=slot.user,
                request_time=slot.request_time,
                reason=data.get('reason')
            )
            deleted_slot.save()
            slot.delete()
            return Response({'message': 'Slot deleted successfully!'})
        except Exception as e:
            return Response({'message': e}, status=404)

    # delete slot (staff)
    def patch(self, request):
        if request.user.is_staff:
            data = request.data
            slot = models.Slot.objects.get(id=data.get('id'))
            slot.is_booked = True
            slot.save()
            return Response({'message': 'Slot booked successfully!'})
        else:
            return Response({'message': 'You are not authorized to perform this action!'}, status=403)

class VerifyEmail(APIView):
    permission_classes = [IsAuthenticated]
    # get verification code via email
    def get(self, request):
        user = request.user
        if user.email_verified == True:
            return Response({'message': 'Contact already Verified successfully!'})
        else:
            emails.sendverificationcode(user.email)
            return Response({'message': 'Verification code sent successfully!'})

    # verify email via OTP
    def post(self, request):
        user = request.user
        if user.email_verified == True:
            return Response({'message': 'Contact already Verified successfully!'})
        else:
            data = request.data
            try:
                if str(data.get('otp')) == str(emails.generate_verification_code(user.email)):
                    user.email_verified = True
                    user.save()
                    return Response({'message': 'Email Verified successfully!'})
                else:
                    return Response({'message': 'Invalid verification code!'}, status=400)
            except Exception as e:
                return Response({'message': 'Error occured',"Error":e})
