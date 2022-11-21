from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import reverse

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.FloatField()
    brand = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    images = models.URLField(max_length=255)
   
    

    def __str__(self):
        return self.title
    
    
    
class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=240)
    email = models.CharField(max_length=240, unique=True)

    def __str__(self):
        return self.name   


# class Basket(models.Model):
#             customer = models.ForeignKey(Customer, on_delete=models.CASCADE , default="test")
#             product = models.ForeignKey(Product, on_delete=models.CASCADE)
#             quantity=models.IntegerField()
#             pass
#             def __str__(self):
#                     return self.title


# class OrederDetail(models.Model):
#             products = models.ManyToManyField(Basket)
#             ordered = models.BooleanField(default=False)
#             customer = models.ForeignKey(Customer, on_delete=models.CASCADE , default="test" )
#             start_date = models.DateTimeField(auto_now_add=True)
           
           
           
#             def __str__(self):
#                     return self.user.username





class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.quantity} of {self.product.title}"


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=10)
    message = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        # return self.name
        return " Message from " + self.name + ' - ' + self.email

# user profile_pics


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=120)
    phone = models.CharField(max_length=10)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    

    def __str__(self):
        return f'{self.user.username} Profile'


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'phone', 'address','image']
class UserUpdateForm(forms.ModelForm):
   
    class Meta:
        model = User
        fields = ['email']

def get_add_to_basket_url(self):
    return reverse("add_to_basket", kwargs={"title": self.title})
