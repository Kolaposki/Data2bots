from django.contrib import admin
from .models import Product, Order, OrderProduct, Payment, Address

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['client',
                    'ordered',
                    'address',
                    'payment',
                    ]
    list_display_links = [
        'client',
        'address',
        'payment',
    ]
    list_filter = ['ordered', ]

    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'default'
    ]
    list_filter = ['default', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Address, AddressAdmin)
