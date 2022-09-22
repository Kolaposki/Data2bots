from rest_framework import serializers
from drf_user.models import User
from client.models import Order, OrderProduct, Address, Product, Payment


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        """Passing model metadata"""

        model = User
        fields = (
            "id",
            "username",
            "name",
            "email",
            "mobile",
            "password",
        )
        read_only_fields = ("is_superuser", "is_staff")
        extra_kwargs = {"password": {"write_only": True}}


class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField()

    class Meta:
        model = Payment
        fields = "__all__"


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField()
    buyer = UserSerializer(read_only=True)
    buyer_id = serializers.IntegerField()

    class Meta:
        model = OrderProduct
        fields = "__all__"
        read_only_fields = ("ordered",)
        extra_kwargs = {"buyer_id": {"write_only": True}, "product_id": {"write_only": True}}


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(read_only=True, many=True)
    # products_id = serializers.IntegerField()
    # products_id = serializers.ListField(write_only=True)
    buyer = UserSerializer(read_only=True)
    buyer_id = serializers.IntegerField()

    payment = PaymentSerializer(read_only=True)
    payment_id = serializers.IntegerField()

    address = AddressSerializer(read_only=True)
    address_id = serializers.IntegerField()
    get_total = serializers.FloatField(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        extra_kwargs = {"buyer_id": {"write_only": True}, "products_id": {"write_only": True},
                        "payment_id": {"write_only": True}}
