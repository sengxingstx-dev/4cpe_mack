from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import json
import datetime
from django.contrib import messages
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
from . import forms
from .forms import UserForm


def registration(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserForm()
    
    return render(request, 'registration/signup.html', {'form': form})


def dashboard(request):
    return render(request, 'dashboard/main.html')


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


def orders(request):
    orders = Order.objects.all()
    context = {
        'orders': orders,
    }
    return render(request, 'dashboard/orders.html', context)


def edit_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        form = forms.OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orders')
    else:
        form = forms.OrderForm(instance=order)
        print(form.errors)
    
    return render(request, 'dashboard/edit_order.html', {'form': form})


def delete_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        order.delete()
    except Order.DoesNotExist:
        messages.error(request, 'Order does not exist.')
        return redirect('store')  # Replace 'store' with the appropriate URL name for your store page

    # Handle the logic for deleting the order
    # ...

    # Redirect to a success page or render a template
    return redirect('orders')  # Replace 'store' with the appropriate URL name for your store page


def customers(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers,
    }
    return render(request, 'dashboard/customers.html', context)


def edit_customer(request, pk):
    customer = Customer.objects.get(id=pk)

    if request.method == 'POST':
        form = forms.CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers')
    else:
        form = forms.CustomerForm(instance=customer)
        print(form.errors)
    
    return render(request, 'dashboard/edit_customer.html', {'form': form})


def products(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'dashboard/products.html', context)


def edit_product(request, pk):
    product = Product.objects.get(id=pk)

    if request.method == 'POST':
        form = forms.ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = forms.ProductForm(instance=product)
        print(form.errors)
    
    return render(request, 'dashboard/edit_product.html', {'form': form})


def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        product.delete()
    except Product.DoesNotExist:
        messages.error(request, 'Product does not exist.')
        return redirect('products')

    return redirect('products')



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
    return render(request, 'dashboard/customer_orders.html', {'customer': customer, 'orders': orders})
