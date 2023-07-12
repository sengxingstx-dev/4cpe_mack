from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import datetime
from django.contrib.auth.models import User
from .utils import cookie_cart, cart_data, guest_order
from .models import (
    Customer,
    Product,
    Order,
    OrderItem,
    ShippingAddress,
    ConfirmPayment,
    Income, Outcome,
)


def store(request):
    data = cart_data(request)
    cart_items = data['cart_items']

    products = Product.objects.all()
    context = {
        'products': products,
        'cart_items': cart_items
    }
    return render(request, 'store/store.html', context)


def cart(request):
    data = cart_data(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items
    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cart_data(request)
    items = data['items']
    order = data['order']
    cart_items = data['cart_items']

    context = {
        'items': items,
        'order': order,
        'cart_items': cart_items
    }
    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)
    
    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer,
            complete=False
        )

    else:
        customer, order = guest_order(request, data)

    # user or guest user checkout have to save to db
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    # print('Total1 == Total2:', total == float(order.get_cart_total))

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            tel=data['shipping']['tel'],
            delivery=data['shipping']['delivery'],
        )
        ConfirmPayment.objects.create(
            total=total,
            comment=data['shipping']['comment'],
            payment_photo=data['shipping']['qr']
        )
        Income.objects.create(
            price=total,
            user_id=request.user
        )

    return JsonResponse('Payment complete!', safe=False)


def customers(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers,
    }
    return render(request, 'store/customers.html', context)


# def customer_orders(request, pk):
#     try:
#         customer = User.objects.get(id=pk)
#         orders = Order.objects.filter(customer=customer)
#         return render(request, 'store/customer_orders.html', {'customer': customer, 'orders': orders})
#     except User.DoesNotExist:
#         # Handle case when customer with given ID doesn't exist
#         # You can redirect to an error page or return an appropriate response
#         return HttpResponse('<h1>Customer not found</h1>')

def customer_orders(request, pk):
    # user = User.objects.get(id=pk)
    customer = Customer.objects.get(id=pk)
    orders = Order.objects.filter(customer=customer)
    return render(request, 'store/customer_orders.html', {'customer': customer, 'orders': orders})
