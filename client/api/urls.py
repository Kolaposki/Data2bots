from django.urls import path

from client.views import HelloView, ProductsView, CartView, OrderView

urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
    path("product/", ProductsView.as_view(), name="product"),
    path("product/<int:pk>/", ProductsView.as_view(), name="product_detail"),

    # CartProductView
    path("cart/", CartView.as_view(), name="cart_product"),
    path("cart/<int:pk>/", CartView.as_view(), name="cart_product_detail"),

    # CartProductView
    path("orders/", OrderView.as_view(), name="order_products"),
    path("orders/<int:pk>/", OrderView.as_view(), name="order_products_detail"),

]
