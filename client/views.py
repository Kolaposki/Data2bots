from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from drf_user.models import User
from rest_framework import status, exceptions
import datetime
from .api.serializers import UserSerializer, ProductSerializer, OrderSerializer, OrderProductSerializer, \
    PaymentSerializer
from .models import Product, Order, OrderProduct, Payment, Address

# swagger docs
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# api-view for order
class OrderView(APIView):
    """
      OrderView
      CRUD functionalities for order
    """
    permission_classes = [IsAuthenticated]  # only allow authenticated users

    def get(self, request, pk=None):
        """
        This view is responsible for getting a client's order, or otherwise all orders
        """
        if pk:
            try:
                order = Order.objects.get(pk=pk, client=request.user)
                serializer = OrderSerializer(order)
                return Response({"order": serializer.data}, status=status.HTTP_200_OK)
            except Order.DoesNotExist:
                exc = exceptions.NotFound()
                data = {'order-detail': exc.detail}
                return Response(data, exc.status_code)

        # No PK provided. return all Orders
        order = Order.objects.filter(client=request.user)
        serializer = OrderSerializer(order, many=True)  # return all orders
        return Response({"orders": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'products_id': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER),
                                          description='Cart IDS'),
            'client_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Client ID'),
            'address_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Address ID'),
            'payment_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Payment ID'),
        }),
        responses={200: OrderSerializer, 400: 'Bad Request'})  # for documentation
    def post(self, request):
        try:
            # Validate data then save
            serializer = OrderSerializer(data=request.data)

            if serializer.is_valid():
                validated_data = serializer.validated_data
                print("serializer.is_valid()")
                # verify if payment is valid
                try:
                    payment = Payment.objects.get(pk=validated_data.get('payment_id'), user=request.user)
                except Payment.DoesNotExist:
                    exc = exceptions.NotFound()
                    data = {'payment-detail': exc.detail}
                    return Response(data, exc.status_code)

                products_id = request.data.get('products_id')
                print("products_id", products_id)
                if not products_id:
                    return Response({"status": "error", "result": "products_id must be an array or list"},
                                    status=status.HTTP_400_BAD_REQUEST)

                try:
                    products_id_list = eval(products_id)
                except TypeError:
                    products_id_list = eval(str(products_id))

                print("products_id", products_id_list, products_id_list[0])
                if type(products_id_list) is not list:
                    return Response({"status": "error", "result": "products_id must be an array or list"},
                                    status=status.HTTP_400_BAD_REQUEST)

                # create order object or use previously uncompleted order object
                order_obj, created = Order.objects.get_or_create(
                    client=request.user,
                    ordered=False
                )

                # add products to order
                try:
                    for pk in products_id_list:
                        order_product = OrderProduct.objects.get(pk=pk, client=request.user)
                        order_obj.products.add(order_product)
                except OrderProduct.DoesNotExist:
                    exc = exceptions.NotFound()
                    data = {'OrderProduct object does not exist in the database - products_id ': exc.detail}
                    return Response(data, exc.status_code)

                try:
                    address = Address.objects.get(pk=validated_data.get('address_id'), user=request.user)

                except Address.DoesNotExist:
                    exc = exceptions.NotFound()
                    data = {'address-detail': exc.detail}
                    return Response(data, exc.status_code)

                order_obj.address = address
                # check if payment amount is enough
                print("to pay: ", order_obj.get_total())
                print("funds: : ", payment.amount)
                if payment.amount >= order_obj.get_total():
                    payment.amount = float(payment.amount) - float(order_obj.get_total())  # deduct balance
                    order_obj.payment = payment

                    # process order here
                    order_obj.ordered_date = datetime.datetime.now()
                    order_obj.ordered = True
                    order_obj.save()
                    payment.save()
                else:
                    #     not enough money
                    return Response({"status": "error", "result": "Not enough money. Please fund"},
                                    status=status.HTTP_400_BAD_REQUEST)

                return Response({"status": "success", "result": {
                    'id': order_obj.pk,
                    'total_paid': order_obj.get_total(),
                    'client': order_obj.client.id,
                    'ordered_date': order_obj.ordered_date
                }, "message": 'Created order successfully'},
                                status=status.HTTP_201_CREATED)
            else:
                error_dict = {}
                for field_name, field_errors in serializer.errors.items():
                    print(field_name, field_errors)
                    error_dict[field_name] = field_errors[0]
                return Response({"status": "error", "result": error_dict}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"status": "error", "result": "An error occurred", "message": str(e)},
                            status=status.HTTP_501_NOT_IMPLEMENTED)


# api-view for cart
class CartView(APIView):
    """
      CartView
      CRUD functionalities for cart
    """
    permission_classes = [IsAuthenticated]  # only allow authenticated users

    def get(self, request, pk=None):
        """
        This view is responsible for getting a cart-product, or otherwise all products in all carts
        """
        if pk:
            try:

                order_product = OrderProduct.objects.get(pk=pk, client=request.user)
                serializer = OrderProductSerializer(order_product)
                return Response({"order_product": serializer.data}, status=status.HTTP_200_OK)
            except OrderProduct.DoesNotExist:
                exc = exceptions.NotFound()
                data = {'cart-detail': exc.detail}
                return Response(data, exc.status_code)

        # No PK provided. return all OrderProducts
        order_products = OrderProduct.objects.filter(client=request.user)
        serializer = OrderProductSerializer(order_products, many=True)  # return all order_products
        return Response({"order_products": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'client_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Client ID'),
            'product_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Product ID'),
            'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quantity of products'),
        }),
        responses={200: OrderSerializer, 400: 'Bad Request'})  # for documentation
    def post(self, request):
        """
        This view is responsible for adding a product to cart, and also for editing a product in cart
        """
        try:
            serializer = OrderProductSerializer(data=request.data)

            if serializer.is_valid():
                validated_data = serializer.validated_data
                try:
                    product = Product.objects.get(pk=validated_data.get('product_id'))
                except Product.DoesNotExist:
                    exc = exceptions.NotFound()
                    data = {'product-detail': exc.detail}
                    return Response(data, exc.status_code)

                client_id = validated_data.get('client_id')

                # check if available in store
                if not product.is_available:
                    print("Product not available")
                    return Response({"status": "error", "result": "Product not available in store"},
                                    status=status.HTTP_400_BAD_REQUEST)

                # check if the product is in cart, then update it. Else add product to cart.
                cart_item, created = OrderProduct.objects.get_or_create(
                    product=product,
                    client_id=client_id,
                    ordered=False
                )
                # assumed new quantity is added to old quantity from the frontend/client
                cart_item.quantity = int(validated_data.get('quantity'))
                cart_item.save()

                # deduct from the quantity in store
                product.quantity = product.quantity - int(validated_data.get('quantity'))
                product.save()
                product_serializer = ProductSerializer(product)
                return Response({"status": "success", "result": {
                    'id': cart_item.id,
                    'quantity': cart_item.quantity,
                    'client_id': cart_item.client.id,
                    'product': product_serializer.data,
                    'total_price': cart_item.get_total_product_price()
                }}, status=status.HTTP_201_CREATED)

            else:
                error_dict = {}
                for field_name, field_errors in serializer.errors.items():
                    print(field_name, field_errors)
                    error_dict[field_name] = field_errors[0]
                return Response({"status": "error", "result": error_dict}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"status": "error", "result": "An error occurred while processing the request",
                             'message': str(e)},
                            status=status.HTTP_501_NOT_IMPLEMENTED)

    def delete(self, request, pk=None):
        try:
            order_product = OrderProduct.objects.get(pk=pk, client=request.user)
            order_product.delete()
            return Response({"status": "success", "result": "Item Deleted"}, status=status.HTTP_202_ACCEPTED)
        except OrderProduct.DoesNotExist:
            exc = exceptions.NotFound()
            data = {'detail': exc.detail}
            return Response(data, exc.status_code)


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


# extract token from user object
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# api used for making payment
class PaymentView(APIView):
    permission_classes = [IsAuthenticated]  # only allow authenticated users

    def get(self, request, pk=None):
        """
        This view is responsible for getting payment
        """
        if pk:
            try:

                payment = Payment.objects.get(pk=pk, user=request.user)
                serializer = PaymentSerializer(payment)
                return Response({"payment": serializer.data}, status=status.HTTP_200_OK)
            except Payment.DoesNotExist:
                exc = exceptions.NotFound()
                data = {'Payment-detail': exc.detail}
                return Response(data, exc.status_code)

        # No PK provided. return all payments made by user
        payments = Payment.objects.filter(user=request.user)
        serializer = PaymentSerializer(payments, many=True)  # return all payments
        return Response({"payments": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
            'amount': openapi.Schema(type=openapi.TYPE_INTEGER, description='Amount'),
            'method': openapi.Schema(type=openapi.TYPE_STRING, description='Method of payment (CASH/CARD) in CAPS'),
        }),
        responses={200: PaymentSerializer, 400: 'Bad Request'})  # for documentation
    def post(self, request):
        try:
            # Validate data then save
            serializer = PaymentSerializer(data=request.data)
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
            return Response({"status": "error", "result": "An error occurred", "message": str(e)},
                            status=status.HTTP_501_NOT_IMPLEMENTED)

    def delete(self, request, pk=None):
        try:
            payment = Payment.objects.get(pk=pk, user=request.user)
            payment.delete()
            return Response({"status": "success", "result": "Payment Deleted"}, status=status.HTTP_202_ACCEPTED)
        except Payment.DoesNotExist:
            exc = exceptions.NotFound()
            data = {'Payment details: ': exc.detail}
            return Response(data, exc.status_code)
