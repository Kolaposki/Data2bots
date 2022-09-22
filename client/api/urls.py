from django.urls import path

from client.views import ProductsView, CartView, OrderView, PaymentView

# api urls
urlpatterns = [
    # products urls
    path("product/", ProductsView.as_view(), name="product"),
    path("product/<int:pk>/", ProductsView.as_view(), name="product_detail"),

    # cart urls
    path("cart/", CartView.as_view(), name="cart_product"),
    path("cart/<int:pk>/", CartView.as_view(), name="cart_product_detail"),

    # Order urls
    path("orders/", OrderView.as_view(), name="order_products"),
    path("orders/<int:pk>/", OrderView.as_view(), name="order_products_detail"),

    # Order urls
    path("payment/", PaymentView.as_view(), name="payment"),
    path("payment/<int:pk>/", PaymentView.as_view(), name="payment_detail"),

]
