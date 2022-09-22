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
        # fields = ('id', 'buyer', 'product', 'ordered', 'quantity',)
        read_only_fields = ("ordered",)


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(read_only=True, many=True)
    buyer = UserSerializer(read_only=True)
    buyer_id = serializers.IntegerField()
    payment = PaymentSerializer()
    get_total = serializers.FloatField(read_only=True)

    # address = Address(read_only=True, many=True)

    class Meta:
        model = Order
        # fields = ('products',)
        fields = "__all__"
