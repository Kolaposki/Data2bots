from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from drf_user.models import User
from rest_framework.generics import get_object_or_404

from .api.serializers import UserSerializer, ProductSerializer
from .models import Product
from rest_framework.generics import ListAPIView


# api-view for products
class ProductsView(APIView):
    """
       Gets all the products or by id. Adding of products isn't considered in objectives. Add products through admin
    """
    permission_classes = (AllowAny,)  # allow any unathenticated request

    def get(self, request, pk=None):
        if pk:
            product = get_object_or_404(Product, pk=pk)
            serializer = ProductSerializer(product)
            return Response({"product": serializer.data}, status=status.HTTP_200_OK)

        # No PK provided. return all products
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)  # return all products
        return Response({"products": serializer.data}, status=status.HTTP_200_OK)


# API for registering users
class RegisterView(CreateAPIView):
    """
    Register View

    Register a new user to the system.
    The data required are username, email, name, password and mobile (optional).

    Author: Himanshu Shankar (https://himanshus.com)
            Aditya Gupta (https://github.com/ag93999)
    """

    # renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """Override perform_create to create user"""
        data = {
            "username": serializer.validated_data["username"],
            "email": serializer.validated_data["email"],
            "password": serializer.validated_data["password"],
            "name": serializer.validated_data["name"],
        }
        try:
            data["mobile"] = serializer.validated_data["mobile"]
        except KeyError:
            if not settings.USER_SETTINGS["MOBILE_OPTIONAL"]:
                raise ValidationError({"error": "Mobile is required."})

        new_user = User.objects.create_user(**data)  # Creates a normal user
        # TODO: Create profile automatically
        print("new_user", new_user)
        refresh = RefreshToken.for_user(new_user)
        print("refresh", refresh)

        data = {
            "username": new_user.username,
            "name": new_user.name,
            "email": new_user.email,
            "mobile": new_user.mobile,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        print("data", data)

        # tokens = get_tokens_for_user(new_user)
        # TODO : It doesnt return tokens
        return data

        # return new_user, tokens


# extract token from user object
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class HelloView(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
