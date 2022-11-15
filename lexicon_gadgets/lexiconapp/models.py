from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
            title= models.CharField(max_length=255)
            description= models.CharField(max_length=255)
            price=  models.FloatField()
            brand= models.CharField(max_length=255)
            category= models.CharField(max_length=255)
            images= models.URLField(max_length=255)
            def __str__(self):
                    return self.title
            
            
            
            
            
# class Basket(models.Model):
#             user = models.ForeignKey(User, on_delete=models.CASCADE)
#             product = models.ForeignKey(Product, on_delete=models.CASCADE)
#             quantity=models.IntegerField()
#             pass
#             def __str__(self):
#                     return self.title
    
    

# class Oreder(models.Model):
    
#             order_number=models.IntegerField()
#             products = models.ManyToManyField(Basket)
#             ordered = models.BooleanField(default=False)
#             user = models.ForeignKey(User, on_delete=models.CASCADE)
#             start_date = models.DateTimeField(auto_now_add=True)
#             oredered_date=models.DateTimeField()
#             user_discount=models.DecimalField()
#             total_price=models.IntegerField()
#             def __str__(self):
#                     return self.user.username
            
    
    


           