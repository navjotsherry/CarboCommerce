from types import CoroutineType
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=True)
    name= models.CharField(max_length=200, null=True)
    email= models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=200)
    price=models.FloatField()
    digital= models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url= self.image.url
        except:
            url= ''
        return url
        

class Order(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False)
    transaction_id= models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)
    @property
    def get_cart_total(self):
        orderItems= self.orderitem_set.all()
        total = sum([items.get_total for items in orderItems])
        return total
    @property
    def cart_list(self):
        orderItems = self.orderitem_set.all()
        list_n = sum([items.quantity for items in orderItems])
        return list_n
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank = True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank = True, null=True)
    quantity = models.IntegerField(default=0, null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        total= self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order= models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True) 
    address=models.CharField(max_length=200, null= True)
    city=models.CharField(max_length=200, null=True)
    state=models.CharField(max_length=200, null=True)
    zipcode=models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address