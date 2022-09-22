from django.db import models

# from django.contrib.auth.models import User
from drf_user.models import User
from django.conf import settings
from django.utils.text import slugify
import uuid


class Product(models.Model):
    title = models.CharField(max_length=250)
    category = models.CharField(max_length=250)
    picture = models.ImageField(upload_to="products/images", null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    quantity = models.IntegerField(default=10)  # available quantity of given product
    description = models.TextField()
    slug = models.SlugField(default='', editable=False, )
    available = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True, null=True)
    update_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_available(self):
        return self.quantity > 0

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-update_on',)
    # def get_absolute_url(self):
    #     return reverse("product_detail", kwargs={"slug": self.slug})


class OrderProduct(models.Model):
    """
    Order made on a single product
    """
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

    def get_total_product_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    """
    Total order of all Products
    """
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)

    # We assume there's only one delivery method. Home delivery
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.client.username}'s Order"

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_total_product_price()

        return total

    class Meta:
        ordering = ('-ordered_date',)


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.street_address} - {self.user.username}"

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    METHOD = (
        ("CARD", "Card"),
        ("CASH", "Cash"),
    )

    charge_id = models.CharField(max_length=50, blank=True, null=True)  # payment provider id eg stripe
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    method = models.CharField(max_length=10, choices=METHOD)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.charge_id:
            self.charge_id = uuid.uuid4()

        super(Payment, self).save(*args, **kwargs)
