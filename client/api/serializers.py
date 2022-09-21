from rest_framework import serializers
from drf_user.models import User
from client.models import Order, OrderProduct, Address, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        # fields = ('products',)
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


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField()
    buyer = UserSerializer(read_only=True)
    buyer_id = serializers.IntegerField()

    class Meta:
        model = OrderProduct
        fields = "__all__"
        # fields = ('id', 'buyer', 'product', 'ordered', 'quantity',)
        read_only_fields = ("ordered",)
