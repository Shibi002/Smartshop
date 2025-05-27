from django.db import models


# Create your models here.

class Contact(models.Model):
    con_name = models.CharField(max_length=255)
    con_email = models.EmailField(max_length=255)
    con_message = models.TextField()

    def __str__(self):
        return self.con_name


class Register(models.Model):
    reg_name = models.CharField(max_length=255)
    reg_email = models.EmailField(max_length=255)
    reg_phone = models.CharField(max_length=255)
    reg_user = models.CharField(max_length=255)
    reg_pswd = models.CharField(max_length=255)


    def __str__(self):
        return self.reg_name
    
class Product(models.Model):
    pro_id = models.IntegerField(null=True)
    pro_name = models.CharField(max_length=250) 
    pro_price = models.FloatField()
    cat = models.IntegerField(null=True)   
    pro_image = models.FileField(null=True,upload_to="products")
    # category_id = models.IntegerField(null=True)
    

    def __str__(self):
        return self.pro_name
    
class Cart(models.Model):
    cart_user = models.CharField(max_length=250,default=None)
    cart_proid = models.IntegerField(null=True)
    cart_name = models.CharField(max_length=250)
    cart_price = models.FloatField(max_length=250)
    cart_image = models.FileField(null=True)
    cart_qty = models.IntegerField()
    cart_amount = models.FloatField()

    def __str__(self):
        return self.cart_name
    
class Order(models.Model):
    order_user = models.CharField(max_length=250,default=None)
    order_proid = models.IntegerField(null=True)
    order_name = models.CharField(max_length=250)
    order_price = models.FloatField(max_length=250)
    order_image = models.FileField(null=True)
    order_qty = models.IntegerField()
    order_amount = models.FloatField()
    order_address = models.TextField(null=True)
    order_dlvtype = models.CharField(null=True,max_length=10)
    order_status = models.IntegerField(default=0)

    def __str__(self):
        return self.order_name
    
class Category(models.Model):
    # category_id = models.IntegerField(null=True)
    category_name = models.CharField(max_length=250)
    category_image = models.FileField(null=True,upload_to="category")  
    category_des = models.TextField(null=True)


    def __str__(self):
        return self.category_name 
    
class Wishlist(models.Model):
    wishlist_user = models.CharField(max_length=255)
    wishlist_productId = models.CharField(max_length=255, null=True)
    wishlist_name = models.CharField(max_length=250)
    wishlist_image = models.FileField(null=True, upload_to="wishlist") 
    wishlist_price = models.FloatField(max_length=250, null=True) 
    
    def __str__(self):
        return self.wishlist_name
    
class Subcategory(models.Model):
    subcate_user = models.CharField(max_length=255)
    subcate_id = models.CharField(max_length=255, null=True)
    subcate_name =  models.CharField(max_length=250)

    
    def __str__(self):
        return self.subcate_name








    

