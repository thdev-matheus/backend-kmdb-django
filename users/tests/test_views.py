import ipdb
from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from users.serializers import UserSerializer


class UserRegisterViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = reverse("register_user")

        cls.CRITICAL_USER = {
            "username": "lucira",
            "email": "lucira@mail.com",
            "birthdate": "1999-09-09",
            "first_name": "Lucira",
            "last_name": "Critica",
            "password": "1234",
            "is_critic": True,
        }

        cls.COMMON_USER = {
            "username": "alexandre",
            "email": "ale@mail.com",
            "birthdate": "1999-09-09",
            "first_name": "Ale",
            "last_name": "Nao Critico",
            "password": "1234",
        }

        cls.WRONG_USER = {
            "username": "alexandre",
            "email": "alemail",
            "birthdate": "1999-09-09",
            "first_name": "Ale",
            "last_name": "Nao Critico",
            "password": "",
        }

    def test_creation_of_critical_user_with_correct_data(self):
        response = self.client.post(self.BASE_URL, self.CRITICAL_USER)

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.data)
        self.assertIn("updated_at", response.data)
        self.assertFalse(response.data["is_superuser"])
        self.assertNotIn("password", response.data)
        self.assertTrue(response.data["is_critic"])

    def test_creation_of_common_user_with_correct_data(self):
        response = self.client.post(self.BASE_URL, self.COMMON_USER)

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.data)
        self.assertIn("updated_at", response.data)
        self.assertFalse(response.data["is_superuser"])
        self.assertNotIn("password", response.data)
        self.assertFalse(response.data["is_critic"])

    def test_user_creation_without_pass_the_keys_in_the_body(self):
        response = self.client.post(self.BASE_URL, {})

        self.assertEqual(response.status_code, 400)

        self.assertIn("password", response.data)
        self.assertIsInstance(response.data["password"][0], ErrorDetail)
        self.assertIs(response.data["password"][0].code, "required")

        self.assertIn("username", response.data)
        self.assertIsInstance(response.data["username"][0], ErrorDetail)
        self.assertIs(response.data["username"][0].code, "required")

        self.assertIn("email", response.data)
        self.assertIsInstance(response.data["email"][0], ErrorDetail)
        self.assertIs(response.data["email"][0].code, "required")

        self.assertIn("birthdate", response.data)
        self.assertIsInstance(response.data["birthdate"][0], ErrorDetail)
        self.assertIs(response.data["birthdate"][0].code, "required")

        self.assertIn("first_name", response.data)
        self.assertIsInstance(response.data["first_name"][0], ErrorDetail)
        self.assertIs(response.data["first_name"][0].code, "required")

        self.assertIn("last_name", response.data)
        self.assertIsInstance(response.data["last_name"][0], ErrorDetail)
        self.assertIs(response.data["last_name"][0].code, "required")

    def test_creation_of_user_that_already_exists(self):
        response_1 = self.client.post(self.BASE_URL, self.CRITICAL_USER)
        response_2 = self.client.post(self.BASE_URL, self.CRITICAL_USER)

        self.assertEqual(response_2.status_code, 400)

        self.assertIn("username", response_2.data)
        self.assertIsInstance(response_2.data["username"][0], ErrorDetail)
        self.assertIs(response_2.data["username"][0].code, "unique")

        self.assertIn("email", response_2.data)
        self.assertIsInstance(response_2.data["email"][0], ErrorDetail)
        self.assertIs(response_2.data["email"][0].code, "unique")

    def test_user_creation_with_invalid_data(self):
        response = self.client.post(self.BASE_URL, self.WRONG_USER)

        self.assertEqual(response.status_code, 400)

        self.assertIn("password", response.data)
        self.assertIsInstance(response.data["password"][0], ErrorDetail)
        self.assertIs(response.data["password"][0].code, "blank")

        self.assertIn("email", response.data)
        self.assertIsInstance(response.data["email"][0], ErrorDetail)
        self.assertIs(response.data["email"][0].code, "invalid")


class UserLoginViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = reverse("login_user")

        user = {
            "username": "lucira",
            "email": "lucira@mail.com",
            "birthdate": "1999-09-09",
            "first_name": "Lucira",
            "last_name": "Critica",
            "password": "1234",
            "is_critic": True,
        }

        serializer = UserSerializer(data=user)
        serializer.is_valid()
        serializer.save()

        cls.CRITICAL_USER = serializer.data

        cls.USER_LOGIN = {
            "username": "lucira",
            "password": "1234",
        }

        cls.WRONG_USER_LOGIN = {
            "username": "gohan2323232",
            "password": "aaaaaaaa",
        }

    def test_user_login_with_the_correct_data(self):
        response = self.client.post(self.BASE_URL, self.USER_LOGIN)

        self.assertEqual(response.status_code, 200)

        self.assertIn("token", response.data)

        # self.assertIn("user", response.data)
        # self.assertIn("id", response.data["user"])
        # self.assertEqual(response.data["user"]["username"], "lucira")

    def test_user_login_with_the_incorrect_data(self):
        response = self.client.post(self.BASE_URL, self.WRONG_USER_LOGIN)

        self.assertEqual(response.status_code, 400)

        self.assertIn("non_field_errors", response.data)
        self.assertIsInstance(response.data["non_field_errors"][0], ErrorDetail)
        self.assertIs(response.data["non_field_errors"][0].code, "authorization")

    def test_user_login_without_pass_the_keys_in_the_body(self):
        response = self.client.post(self.BASE_URL, {})

        self.assertEqual(response.status_code, 400)

        self.assertIn("password", response.data)
        self.assertIsInstance(response.data["password"][0], ErrorDetail)
        self.assertIs(response.data["password"][0].code, "required")

        self.assertIn("username", response.data)
        self.assertIsInstance(response.data["username"][0], ErrorDetail)
        self.assertIs(response.data["username"][0].code, "required")
