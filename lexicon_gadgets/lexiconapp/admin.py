from django.contrib import admin

from lexiconapp.models import *


# Register your models here.

admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Contact)

