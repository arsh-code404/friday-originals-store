from django.db import models
from django.utils import timezone 

# Create your models here.

class Contact(models.Model):
    first=models.CharField(max_length=80)
    last=models.CharField(max_length=80)
    service=models.CharField(max_length=30)
    email=models.EmailField()
    commnt= models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first
    

class Product(models.Model):
    name=models.CharField(max_length=80)
    price=models.DecimalField(max_digits=6, decimal_places=2)
    descp=models.CharField(max_length=280)
    set=models.CharField(max_length=80)
    image1 = models.ImageField(upload_to="products/")
    image2 = models.ImageField(upload_to="products/",  blank=True, null=True)
   
    def __str__(self):
        return self.name
    
class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    date=models.DateField(default = timezone.now)
    def __str__(self):
        return self.product.name