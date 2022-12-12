from locale import currency
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from django.contrib.auth.password_validation import validate_password
from decimal import Decimal




class User(AbstractUser):
    tip = models.DecimalField(max_digits=4, decimal_places=2)
    USERNAME_FIELD = 'email'
    username=models.CharField(max_length=1,blank=True, null=True, unique=False)
    first_name=models.CharField(max_length=50, blank=False)
    last_name=models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=100, unique=True) # changes email to unique and blank to false
    REQUIRED_FIELDS = [] # removes email from REQUIRED_FIELDS 
    password =  models.CharField(validators=[validate_password], max_length=128)   
  
    def __str__(self):
        return f"{self.email} {self.first_name} {self.last_name} {self.tip}"  

class Bill_Header(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="bill_owner")
    date = models.DateTimeField(default=datetime.utcnow)
    title = models.CharField(max_length=50)
    total = models.DecimalField(max_digits= 8, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits= 4, decimal_places=2, default=0.00)
    tip = models.DecimalField(max_digits= 4, decimal_places=2, default=0.00)
    split = models.BooleanField(default=False)
    image = models.FileField(upload_to='documents/', blank=True, null=True)
    currency_symbol = models.CharField(max_length=50, default='$')
    discount = models.PositiveIntegerField( default=0)

    def __str__(self):
        return f"{self.id} {self.user} {self.date} {self.title}" 

    def serialize(self):
        return {
            "bill_id": self.id,
            "user_id": self.user_id,
            "date": self.date,           
            "title": self.title,
            "total": self.total,
            "tax": self.tax, 
            "tip": self.tip,
            "split": self.split,
            "first_name":self.user.first_name,
            "last_name":self.user.last_name,
            "currency_symbol":self.currency_symbol,
            "total_lines": (self.bill_header_lines.values('bill').annotate(sum_total = Sum('total')))[0]['sum_total'],         
        }         


class Bill_User(models.Model):
    bill = models.ForeignKey(Bill_Header,on_delete=models.CASCADE, related_name="bill_header_user")
    user = models.ForeignKey(User, models.SET_NULL, related_name="bill_user",null=True)
    name = models.CharField(max_length=6)
    tip = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    addition = models.DecimalField(max_digits= 8, decimal_places=2, default=0.00) 
    color = models.CharField(max_length=7)

    def __str__(self):
        return f" {self.id} {self.name} {self.tip} {self.addition}" 

    def serialize(self):
        return{
           "user_id": self.id,
           "name": self.name,
           "tip": self.tip, 
           "bill_id": self.bill_id,
           "color": self.color,
           "tax": self.bill.tax
        }

class Bill_Lines(models.Model):
    bill = models.ForeignKey(Bill_Header, on_delete=models.CASCADE, related_name="bill_header_lines")    
    item = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField( default=1 )
    price = models.DecimalField(max_digits= 8, decimal_places=2, default=0.00) 
    total = models.DecimalField(max_digits= 8, decimal_places=2) 
    users = models.ManyToManyField(Bill_User,blank=True, related_name="bill_line")
    discount = models.PositiveIntegerField(default=0)

    
    def __str__(self):
        return f" {self.id} {self.bill} {self.item} {self.total}" 
    
    def serialize(self):
        return {
            "bill_id": self.bill_id,
            "line_id": self.id,
            "item": self.item,
            "quantity": self.quantity,
            "price": self.price,
            "total": self.total,
            "discount": self.discount,
            "line_users": [user.id for user in self.users.all()] , 
            "line_users_names": [user.name for user in self.users.all()] , 
            "line_users_count":  self.users.all().count(),
            "discount_amount": round(Decimal(self.total) * Decimal(int(self.discount)/100),2) if int(self.discount) else 0 
        }             











