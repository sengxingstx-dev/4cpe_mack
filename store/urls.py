from django.urls import path
from . import views


urlpatterns = [ 
    path('', views.store, name='store'),

    #dashboard
    path('dashboard', views.dashboard, name='dashboard'),
    path('orders', views.orders, name='orders'),
    path('customers/', views.customers, name='customers'),
    path('products/', views.products, name='products'),

    path('edit-order/<int:pk>/', views.edit_order, name='edit-order'),
    path('edit-customer/<int:pk>/', views.edit_customer, name='edit-customer'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit-product'),

    path('delete-order/<int:pk>/', views.delete_order, name='delete-order'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete-product'),

    path('signup', views.registration, name='registration'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update-item/', views.update_item, name='update_item'),
    path('process-order/', views.process_order, name='process_order'),
    path('customer-orders/<int:pk>/', views.customer_orders, name='customer-orders'),
]