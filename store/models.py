from django.db import models
from django.contrib.auth.models import User



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    sirname = models.CharField(max_length=50, null=True, blank=True)
    birthday = models.DateTimeField(null=True, blank=True)
    sex = models.CharField(max_length=6, choices=(('Male', 'Male'), ('Female', 'Female')), null=True, blank=True)
    village = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    contry = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_code = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    digital = models.BooleanField(default=False)
    detail = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to="products/", null=True)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    @property
    def image_url(self):
        try:
            url = self.img.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.id}'

    @property
    def shipping(self):
        shipping = False
        order_items = self.orderitem_set.all()
        for i in order_items:
            if i.product.digital == False:
                shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    DELIVERY_BY = (
        ('Houng ah loun', 'Houng ah loun'),
        ('Ah nou sit', 'Ah nou sit')
    )

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50)
    tel = models.CharField(max_length=12, null=True, blank=True)
    delivery = models.CharField(max_length=30, choices=DELIVERY_BY, default='Houng ah loun', null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class ConfirmPayment(models.Model):
    date_payment = models.DateTimeField(auto_now_add=True)
    total = models.FloatField(default=0)
    comment = models.TextField()
    payment_photo = models.ImageField(upload_to="payment/", null=True)

    def __str__(self):
        return f'{self.total}'


class Income(models.Model):
    price = models.FloatField(default=0)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_received = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.price}'


class Outcome(models.Model):
    price = models.FloatField(default=0)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_received = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.price}'
