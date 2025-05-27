from django.contrib import admin
from . models import Contact
from . models import Register
from . models import Product
from . models import Cart
from . models import Order
from . models import Category
from . models import Subcategory
from . models import Wishlist




# Register your models here.

admin.site.register(Contact)
admin.site.register(Register)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Wishlist)
admin.site.register(Subcategory)



