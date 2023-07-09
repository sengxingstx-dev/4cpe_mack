from django.contrib import admin
from .models import (
    Customer,
    Product,
    Order,
    OrderItem,
    ShippingAddress,
    ConfirmPayment, Income, Outcome
)


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'sirname','sex', 'village', 'district', 'province'
    )
    search_fields = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'price', 'detail', 'img', 'amount'
    )
    search_fields = ('name',)


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'customer', 'order', 'address', 'city', 'state',
        'zipcode', 'tel', 'delivery', 'date_added'
    )
    search_fields = ('name',)


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'customer', 'order', 'address', 'city', 'state',
        'zipcode', 'tel', 'delivery', 'date_added'
    )
    search_fields = ('name',)


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'customer', 'complete', 'date_ordered'
    )
    search_fields = ('customer',)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'product', 'order', 'quantity', 'date_added'
    )
    search_fields = ('product',)


class ConfirmPaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'date_payment', 'total', 'comment', 'payment_photo'
    )
    search_fields = ('comment',)


class IncomeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'price', 'user_id', 'date_received',
    )
    search_fields = ('price',)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(ConfirmPayment, ConfirmPaymentAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Outcome)
