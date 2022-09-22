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


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


# api-view for CartView
class CartView(APIView):
    """
       Gets all the ordered-products or by id.
    """
    permission_classes = [IsAuthenticated]  # only allow authenticated users

    def get(self, request, pk=None):
        if pk:
            order_product = get_object_or_404(OrderProduct, pk=pk)
            serializer = OrderProductSerializer(order_product)
            return Response({"order_product": serializer.data},
                            status=status.HTTP_200_OK)

        # No PK provided. return all OrderProducts
        order_products = OrderProduct.objects.all()
        serializer = OrderProductSerializer(order_products, many=True)  # return all order_products
        return Response({"order_products": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            # Validate data then save

            # Check if the product is in cart already
            # TODO: Validate the request data

            serializer = OrderProductSerializer(data=request.data)

            if serializer.is_valid():
                # TODO: use validated_data instead
                product = get_object_or_404(Product, pk=request.data.get('product_id'))
                buyer_id = request.data.get('buyer_id')
                cart_item, created = OrderProduct.objects.get_or_create(
                    product=product,
                    buyer_id=buyer_id,
                    ordered=False
                )
                # assumed new quantity is added to old`quantity from the frontend/client
                cart_item.quantity = int(request.data.get('quantity'))
                cart_item.save()
                product_serializer = ProductSerializer(product)
                return Response({"status": "success", "result": {
                    'id': cart_item.id,
                    'quantity': cart_item.quantity,
                    'buyer_id': cart_item.buyer.id,
                    'product': product_serializer.data} }, status=status.HTTP_201_CREATED)

            else:
                error_dict = {}
                for field_name, field_errors in serializer.errors.items():
                    print(field_name, field_errors)
                    error_dict[field_name] = field_errors[0]
                return Response({"status": "error", "result": error_dict}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"status": "error", "result": "An error occurred"}, status=status.HTTP_501_NOT_IMPLEMENTED)

    def delete(self, request, pk=None):
        order_product = get_object_or_404(OrderProduct, pk=pk)
        order_product.delete()
        return Response({"status": "success", "result": "Item Deleted"})


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
