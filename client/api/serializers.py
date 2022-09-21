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
    """
    UserRegisterSerializer is a model serializer which includes the
    attributes that are required for registering a user.
    """

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
    product = ProductSerializer()
    buyer = UserSerializer()

    class Meta:
        model = OrderProduct
        fields = ('id', 'buyer', 'product', 'ordered', 'quantity',)
        # fields = "__all__"
