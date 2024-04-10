from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

class TestSetUp(APITestCase):
    def setUp(self):
        self.index_url = reverse('index')
        self.token_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')
        self.user_url = reverse('user-edit')
        self.slot_url = reverse('manage-slot')
        self.booking_url = reverse('slot-requests')

        self.user = User.objects.create(
            username='testuser',
            password='testpassword'
        )

        self.token = AccessToken.for_user(self.user)
        self.http_authorization = f'Bearer {self.token}'

        return super().setUp()

    def tearDown(self):
        return super().tearDown()

