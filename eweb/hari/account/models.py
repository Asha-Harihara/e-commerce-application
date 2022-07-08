
from django.db import models
from django.contrib.auth.models import User


STATUS_CHOICES=(
    
     ("PENDING", "PENDING"),
     ("OUT FOR DELIVERY", "OUT FOR DELIVERY"),
     ("DELIVERED", "DELIVERED"),

)
class Adress(models.Model):
     apartment=models.CharField(max_length=200, null=True)
     pincode=models.CharField(max_length=200, null=True)
     area=models.CharField(max_length=200, null=True)
     city=models.CharField(max_length=200, null=True)
     state=models.CharField(max_length=200, null=True)
     country=models.CharField(max_length=200, null=True)

     def __str__(self):
         return str(self.id)

     
class Product(models.Model):
    name=models.CharField(max_length=200, null=True)
    price=models.FloatField()
    seller=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity=models.IntegerField()
    shop=models.ForeignKey(Adress, on_delete=models.SET_NULL, blank=True, null=True)
    image=models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url=self.image.url 
        except:
            url=''
        return url

class Tags(models.Model):
    name=models.CharField(max_length=200,null=True)
    products=models.ManyToManyField(Product)

    def __str__(self):
        return self.name

class Order(models.Model):
    buyer=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
   
    completed=models.BooleanField(default=False, null=True, blank=False)
    delivery_address=models.ForeignKey(Adress, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    
    @property 
    def get_order_total(self):
         items=self.orderitem_set.all()
         total=sum([item.get_total for item in items])
         return total 

class PresentCart(models.Model):
     buyer=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
     product=models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
     quantity=models.IntegerField(default=0)
     

     def __str__(self):
         return str(self.id)
    
     @property
     def get_total(self):
         total=self.product.price*self.quantity
         return total

class OrderedItems(models.Model):
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL , blank=True, null=True)
    quantity=models.IntegerField()
    status=models.CharField(max_length=200, choices=STATUS_CHOICES, default="PENDING")
    
    def __str__(self):
        return str(self.id)
    
    @property
    def get_total(self):
         total=self.product.price*self.quantity
         return total


    


    