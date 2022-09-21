from django.urls import path

from client.views import HelloView, ProductsView, OrderProductView

urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
    path("product/", ProductsView.as_view(), name="product"),
    path("product/<int:pk>/", ProductsView.as_view(), name="product_detail"),

    # CartProductView
    path("ordered-product/", OrderProductView.as_view(), name="cart_product"),
    path("ordered-product/<int:pk>/", OrderProductView.as_view(), name="cart_product_detail"),
]
