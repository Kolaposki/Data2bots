import json

from django.urls import reverse
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from drf_user.models import User

from .models import Product, Payment, OrderProduct, Order,Address


class OrderTestCase(APITestCase):
    order_url = '/api/cart/'

    def setUp(self):
        # username, email, name, password
        self.user = User.objects.create_user(username="testcase", email="test@localhost.app",
                                             password="some-very-strong-psw", name="John Doe")
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.api_authentication()

    def api_authentication(self):
        # Include an appropriate `Authorization:` header on all requests.
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_order_list(self):
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order(self):
        address = Address.objects.create(user=self.user, street_address='broad street',
                                         apartment_address='broad street', country="Nigeria", zip="12345", default=True)
        product = Product.objects.create(title='Balenciaga', category='shoe', price=400, quantity=10,
                                         description="A lovely designer shoe.")
        payment = Payment.objects.create(user=self.user, amount=5000, method="CASH")
        cart = OrderProduct.objects.create(client=self.user, product=product, quantity=5)
        order = Order.objects.create(client=self.user,payment=payment, address=address, ordered=True)
        order.products.add(cart)
        order.save()
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CartTestCase(APITestCase):
    cart_url = '/api/cart/'

    def setUp(self):
        # username, email, name, password
        self.user = User.objects.create_user(username="testcase", email="test@localhost.app",
                                             password="some-very-strong-psw", name="John Doe")
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.api_authentication()

    def api_authentication(self):
        # Include an appropriate `Authorization:` header on all requests.
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_cart_list(self):
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cart_create(self):
        product = Product.objects.create(title='Balenciaga', category='shoe', price=400, quantity=10,
                                         description="A lovely designer shoe.")
        cart = OrderProduct.objects.create(client=self.user, product=product, quantity=5)
        response = self.client.get(self.cart_url)
        response_data = dict(dict(response.data)['order_products'][0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["id"], cart.pk)
        self.assertEqual(response_data["quantity"], 5)
        self.assertEqual(response_data["product_id"], product.pk)
        self.assertFalse(response_data["ordered"])

    def test_cart_detail(self):
        product = Product.objects.create(title='Balenciaga', category='shoe', price=400, quantity=10,
                                         description="A lovely designer shoe.")
        cart = OrderProduct.objects.create(client=self.user, product=product, quantity=2)
        url = f"{self.cart_url}{cart.pk}/"
        response = self.client.get(url)
        response_data = response.data['order_product']
        product_data = dict(response_data['product'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["quantity"], cart.quantity)
        self.assertFalse(response_data["ordered"])
        self.assertEqual(response_data["id"], cart.pk)
        self.assertEqual(response_data["client_id"], self.user.pk)
        self.assertEqual(response_data["product_id"], product.pk)
        self.assertEqual(product_data["id"], product.pk)
        self.assertEqual(product_data["title"], product.title)
        self.assertEqual(product_data["category"], product.category)


class ProductsTestCase(APITestCase):
    product_url = '/api/product/'

    def test_products_list(self):
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_products_detail(self):
        product = Product.objects.create(title='Balenciaga', category='shoe', price=400, quantity=10,
                                         description="A lovely designer shoe.")
        url = f"{self.product_url}{product.pk}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["product"]["id"], 1)
        self.assertEqual(response.data["product"]["quantity"], 10)
        self.assertEqual(response.data["product"]["title"], "Balenciaga")
        self.assertEqual(response.data["product"]["category"], "shoe")
        self.assertTrue(response.data["product"]["available"])


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"username": "testcase", "email": "test@localhost.app",
                "password": "some_strong_psw", "name": "John Shankar"}
        response = self.client.post("/api/user/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "testcase")
        self.assertEqual(response.data["email"], "test@localhost.app")
        self.assertEqual(response.data["name"], "John Shankar")


class ProfileTestCase(APITestCase):
    profile_url = '/api/user/account/'

    def setUp(self):
        # username, email, name, password
        self.user = User.objects.create_user(username="testcase", email="test@localhost.app",
                                             password="some-very-strong-psw", name="John Doe")
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.api_authentication()

    def api_authentication(self):
        # Include an appropriate `Authorization:` header on all requests.
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_profile_authenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_detail_retrieve(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testcase")
        self.assertEqual(response.data["name"], "John Doe")

    def test_profile_update(self):
        response = self.client.patch(self.profile_url,
                                     {"username": "Marky", "name": "Mark Zuckerburg"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                         {"id": 1, "username": "Marky", "name": "Mark Zuckerburg", "email": "test@localhost.app",
                          "mobile": None, "is_superuser": False, "is_staff": False})
