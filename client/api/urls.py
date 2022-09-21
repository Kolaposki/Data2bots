from django.urls import path

from client.views import HelloView, ProductsView

urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
    path("product/", ProductsView.as_view(), name="product"),
    path("product/<int:pk>/", ProductsView.as_view(), name="product_detail"),
]
