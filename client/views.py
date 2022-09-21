from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from drf_user.models import User

from .api.serializers import UserSerializer, ProductSerializer, OrderSerializer, OrderProductSerializer
from .models import Product, Order, OrderProduct


# api-view for products
class OrderProductView(APIView):
    """
       Gets all the ordered-products or by id.
    """
    permission_classes = [IsAuthenticated]  # only allow authenticated users

    def get(self, request, pk=None):
        if pk:
            order_product = get_object_or_404(OrderProduct, pk=pk)
            serializer = OrderProductSerializer(order_product)
            return Response({"order_product": serializer.data}, status=status.HTTP_200_OK)

        # No PK provided. return all OrderProduct
        order_products = OrderProduct.objects.all()
        serializer = OrderProductSerializer(order_products, many=True)  # return all order_products
        return Response({"order_products": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            # Validate data then save
            serializer = OrderProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "result": serializer.data, },
                                status=status.HTTP_201_CREATED)
            else:
                error_dict = {}
                for field_name, field_errors in serializer.errors.items():
                    print(field_name, field_errors)
                    error_dict[field_name] = field_errors[0]
                return Response({"status": "error", "result": error_dict}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"status": "error", "result": "An error occurred"}, status=status.HTTP_501_NOT_IMPLEMENTED)


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
