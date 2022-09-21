from django.db import models

# from django.contrib.auth.models import User
from drf_user.models import User
import datetime
from django.conf import settings


class Profile(models.Model):
    gender_options = (
        ("M", "Male"), ("F", "Female"), ("U", "Unspecified")
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=20, null=False, blank=False)
    profile_pic = models.ImageField(upload_to="profiles/%Y/%m/%d", null=True, blank=True)
    name = models.CharField(max_length=250, null=False, blank=False)
    city = models.CharField(max_length=250, null=True, blank=True)
    gender = models.CharField(max_length=11, choices=gender_options, null=True, blank=True, default="Unspecified")
    occupation = models.CharField(max_length=100, null=True, blank=True)
    street_address = models.CharField(max_length=100, null=True, blank=True)
    apartment_address = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=100, null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True, null=True)
    update_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    title = models.CharField(max_length=250)
    category = models.CharField(max_length=250)
    price = models.FloatField()
    description = models.TextField()
    slug = models.SlugField()
    product_image = models.ImageField(upload_to="products/%Y/%m/%d", null=True)
    available = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True, null=True)
    update_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("client:product", kwargs={
    #         'slug': self.slug
    #     })


class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)

    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Product added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_final_price()

        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    charge_id = models.CharField(max_length=50)  # payment provider id eg stripe
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
