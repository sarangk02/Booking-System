from .test_setup import TestSetUp

class TestViews(TestSetUp):
        def test_index_get(self):
            response = self.client.get(self.index_url)
            self.assertEqual(response.status_code, 200)

        def test_user_create(self):
            data = {
                "username": "testusername",
                "password": "password",
                "name": "test name",
                "email": "test123@gmail.com",
                "contact": "1234566690",
                "emerg_name": "test name2",
                "emerg_contact": "9876543210",
                "gender": "F"
            }
            response = self.client.post(self.user_url, data)
            self.assertEqual(response.status_code, 201)

        def test_get_user_random(self):
            response = self.client.get(self.user_url)
            self.assertEqual(response.status_code, 401)

        def test_get_user_auth(self):
            self.client.credentials(HTTP_AUTHORIZATION=self.http_authorization)
            response = self.client.get(self.user_url)
            self.assertEqual(response.status_code, 200)

        def test_patch_user_name(self):
            self.client.credentials(HTTP_AUTHORIZATION=self.http_authorization)
            data = {
                "name": "test name",
                "emerg_name": "test name2",
                "emerg_contact": "9876543210",
                "gender": "F"
            }
            response = self.client.patch(self.user_url, data)
            self.assertEqual(response.status_code, 200)

        def test_delete_user(self):
            self.client.credentials(HTTP_AUTHORIZATION=self.http_authorization)
            response = self.client.delete(self.user_url)
            self.assertEqual(response.status_code, 200)