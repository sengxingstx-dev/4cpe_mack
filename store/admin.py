from django.contrib import admin
from .models import (
    Customer,
    Product,
    Order,
    OrderItem,
    ShippingAddress,
    ConfirmPayment, Income, Outcome
)


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(ConfirmPayment)
admin.site.register(Income)
admin.site.register(Outcome)
