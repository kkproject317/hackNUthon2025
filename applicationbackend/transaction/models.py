from django.db import models


class transaction(models.Model):
    customerId = models.CharField(max_length=14)
    amount = models.DecimalField(max_digits=9,decimal_places=2)
    timeStamp = models.DateTimeField(auto_now_add=True)
    transactionType = models.CharField(max_length=9)
    IP_address = models.GenericIPAddressField(null=True, blank=True)
    transactionStatus = models.CharField(max_length=15)
    fraudScore = models.IntegerField()
    latitude = models.DecimalField(max_digits=29,decimal_places=20,null=True,blank=True)
    longitude = models.DecimalField(max_digits=29,decimal_places=20,null=True,blank=True)
    
class Customer(models.Model):
    customerId = models.CharField(max_length=14)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    balance = models.DecimalField(max_digits=15,decimal_places=2,default=0.00)
