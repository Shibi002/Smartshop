from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from . models import Contact
from . models import Register
from . models import Product
from . models import Cart
from . models import Order
from . models import Category
from . models import Subcategory
from . models import Wishlist
from django.shortcuts import get_object_or_404
# from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    products = Product.objects.all().values()
    category = Category.objects.all().values()
    category1 = Category.objects.all().order_by('id')[:6] 
    
    context = {
    'Products': products,
    'category': category,
    'category1':category1,

        
    }
    
    template = loader.get_template("index.html")
    return HttpResponse(template.render(context,request))

def about(request):
    template = loader.get_template("about.html")
    return HttpResponse(template.render({},request))

def contact(request):
    if request.method == 'POST':
        #Store form  values into  variables
        
        cname = request.POST["contact_name"]
        cemail = request.POST["contact_email"]
        cmsg = request.POST["contact_message"]

        con = Contact(con_name = cname, con_email = cemail, con_message = cmsg)

        con.save()


    template = loader.get_template("contact.html")
    return HttpResponse(template.render({},request))



def register(request):
    if request.method == 'POST':
        rname = request.POST["register_name"]
        remail = request.POST["register_email"]
        rphone = request.POST["register_number"]
        ruser = request.POST["register_username"]
        rpswd = request.POST["register_password"]

        reg = Register(reg_name = rname, reg_email = remail, reg_phone = rphone, reg_user = ruser, reg_pswd = rpswd)
        reg.save()

    template = loader.get_template("register.html")
    return HttpResponse(template.render({},request))

def login(request):
    if 'user' in request.session:
        return HttpResponseRedirect("/account")

    if request.method == 'POST':
        luser = request.POST["login_username"]
        lpswd = request.POST["login_password"]

        log = Register.objects.filter(reg_user = luser, reg_pswd = lpswd)

        if(log):
            request.session['user'] = luser
            return HttpResponseRedirect('/account')



    template = loader.get_template("login.html") 
    return HttpResponse(template.render({},request))

def account(request):
    if 'user' not in request.session:
        return HttpResponseRedirect("/login")
     

    template = loader.get_template("account.html") 
    return HttpResponse(template.render({},request))

# @login_required
# def account_view(request):
#     return render(request, 'account.html')

# def account(request):
#     if 'user' not in request.session:
#         orders = Order.objects.filter(user=request.user)
#         wishlist_items = Wishlist.objects.filter(user=request.user)
#         return render(request, 'account.html', {
#             'orders': orders,
#             'wishlist_items': wishlist_items,
#         })
#     else:
#         return HttpResponseRedirect('/login')  # Redirect to login if not authenticated



def logout(request):
    if 'user' in request.session:
     del request.session["user"]
     return HttpResponseRedirect("/login")



def addproduct(request):
    if request.method == 'POST':
        pro_name = request.POST['pro_name']
        pro_price = request.POST['pro_price']
        cat = request.POST['cat']
        pro_image = request.FILES['pro_image']
       
        # category_id = request.POST['category_id']

        product = Product.objects.create(
            pro_name = pro_name,
            pro_price = pro_price,
            cat = cat,
            pro_image = pro_image,
            
            # category_id = category_id,


        )
        product.save()
    cats = Category.objects.all().values()
    context = {
         'cats':cats
    }
        # cate_name = Category.objects.all().values()
        # context = {
        #     'Category':cate_name
        # }
       
    template = loader.get_template("addproduct.html")
    return HttpResponse(template.render(context,request))
    
def product(request):
    if 'cid' in request.GET:
        cid = request.GET['cid']
        products = Product.objects.filter(cat=cid).values()
    else:
        products = Product.objects.all().values()

    category = Category.objects.all()
    context = {
        'Products':products,
        "category":category
    }
    template = loader.get_template("product.htmL")
    return HttpResponse(template.render(context,request))

def addtocart(request,id):
    if 'user' not in request.session:
        return HttpResponseRedirect('/login')
    
    exist = Cart.objects.filter(cart_proid = id,cart_user = request.session["user"])
    if exist:
        existcart = Cart.objects.filter(cart_proid = id,cart_user = request.session["user"])[0]
        existcart.cart_qty+=1
        existcart.cart_amount = existcart.cart_qty * existcart.cart_price
        existcart.save()
        return HttpResponseRedirect('/cart')
    else:
        pro = Product.objects.filter(id=id)[0]

        cart = Cart(cart_user = request.session["user"],
                    cart_proid = pro.id,
                    cart_name = pro.pro_name,
                    cart_price = pro.pro_price,
                    cart_image = pro.pro_image,
                    cart_qty=1,
                    cart_amount = pro.pro_price)
        cart.save()
        return HttpResponseRedirect("/cart")



def cart(request):
    if 'user' not in request.session:
        return HttpResponseRedirect('/login')
    
    # user = request.session['user']
    # cart = Cart.objects.filter(cart_user = user)
    # context = {
    #     'cart' : cart
    # }

    #delete cart item
    if 'del' in request.GET:
        id = request.GET['del']
        delcart = Cart.objects.filter(id=id)[0]
        delcart.delete()

    # change cart quantity
    if 'q' in request.GET:
        q = request.GET['q']   
        cp = request.GET['cp'] 
        cart3 = Cart.objects.filter(id=cp)[0]

        if q =='inc':
            cart3.cart_qty+=1
        elif q =='dec':
            if(cart3.cart_qty>1):
                cart3.cart_qty-=1
        cart3.cart_amount = cart3.cart_qty * cart3.cart_price
        cart3.save()    
    user = request.session["user"]  
    cart=Cart.objects.filter(cart_user=user).values()
    cart2=Cart.objects.filter(cart_user=user) 


    tot = 0
    for x in cart2:
        tot+=x.cart_amount


    shp = tot * 10/100
    gst = tot * 18/100


    gtot = tot+shp+gst

    request.session["tot"] = tot   
    request.session["gst"] = gst 
    request.session["shp"] = shp 
    request.session["gtot"] = gtot

    context = {
        'cart':cart,
        'tot':tot,
        'shp':shp,
        'gst':gst,
        'gtot':gtot
    }
         
        
    template = loader.get_template("cart.html")
    return HttpResponse(template.render(context,request))

def checkout(request):
    if 'user' not in request.session:
        return HttpResponseRedirect('/login')
    co = 0
    adrs = dtype = ""

    # Step4 : After order submit
    if 'dlv_adrs' in request.POST:
        adrs = request.POST["dlv_adrs"]
        dtype = request.POST["dlv_type"]
        co=1

    user = request.session["user"]    

    # Step1 : delete old data from orders

    oldodr = Order.objects.filter(order_user = user,order_status=0)
    oldodr.delete()

    # Step2 : add cart data to order table

    cart = Cart.objects.filter(cart_user = user)
    for x in cart:
        odr = Order(order_user = x.cart_user,
                    order_proid = x.cart_proid,
                    order_name = x.cart_name,
                    order_price = x.cart_price,
                    order_image = x.cart_image,
                    order_qty = x.cart_qty,
                    order_amount = x.cart_amount,
                    order_address = adrs,
                    order_dlvtype = dtype,
                    order_status = 0
                
                )
        odr.save()

        # Step3 : display order data
        
    order = Order.objects.filter(order_user = user,order_status = 0)

    tot = request.session["tot"]
    gst = request.session["gst"]
    shp = request.session["shp"]
    gtot = request.session["gtot"]

    context = {
            'order' : order,
            'tot' : tot,
            'shp' : shp,
            'gst' : gst,
            'gtot' : gtot,
            'co' : co

        }
    template = loader.get_template("checkout.html")
    return HttpResponse(template.render(context,request))

def confirmorder(request):
    user = request.session["user"]
    order = Order.objects.filter(order_user = user,order_status = 0)
    for x in order:
        x.order_status=1
        x.save()
        
    template = loader.get_template("confirmorder.html")
    return HttpResponse(template.render({},request))

def myorders(request):
    user = request.session["user"]
    order = Order.objects.filter(order_user = user,order_status = 1)
    context = {
        'order':order
    }
    template = loader.get_template("myorders.html")
    return HttpResponse(template.render(context,request))

def category(request):
    category = Category.objects.all().values()

    context = {
        'category': category
    }
    

    template = loader.get_template("category.html")
    return HttpResponse(template.render(context,request))

def subcategory(request):
    subcategory = Subcategory.objects.all().values()

    context = {
        'subcategory' : subcategory
    }

    template = loader.get_template("subcategory.html")
    return HttpResponse(template.render(context,request))

def addcategory(request):
    if request.method == 'POST':
        category_name = request.POST['category_name'] 
        category_image = request.FILES['category_image']
        category_des = request.POST['category_des']
        

        category = Category(
            category_name = category_name,    
            category_image = category_image,
            category_des = category_des,
           
        )
        category.save()

    template = loader.get_template("addcategory.html")
    return HttpResponse(template.render({},request))


# def wishlist(request):
#     wishlist, created = Wishlist.objects.get_or_create(user=request.user.userprofile)
#     return render(request, 'products/wishlist.html')



# def add_to_wishlist(request, product_id):
#     product = Product.objects.get(id=product_id)
#     return redirect('wishlist')


# def remove_from_wishlist(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     wishlist = Wishlist.objects.get(user=request.user.userprofile)
#     wishlist.products.remove(product)
#     return HttpResponseRedirect(reverse('add_to_wishlist'))

def wishlist(request):
    user = request.session.get("user")
    if 'del' in request.GET:
        id = request.GET['del']
        delwishlist = Wishlist.objects.filter(id=id)[0]
        delwishlist.delete()
    wishlist = Wishlist.objects.filter(wishlist_user=user)
    context = {
        'wishlist':wishlist
    }
    return render(request, 'wishlist.html',context)




def addtowishlist(request, id):
    # Retrieve the user from the session
    user = request.session.get("user")
    if not user:
        # Handle the case where the user is not logged in
        return HttpResponseRedirect("/login")

    # Fetch the product based on the provided id
    product = get_object_or_404(Product, id=id)

    # Check if the product is already in the user's wishlist
    if Wishlist.objects.filter(wishlist_user=user, wishlist_productId=id).exists():
        # If it exists, redirect to the product page or show a message
        return HttpResponseRedirect("/product")
    else:
        # Create a new Wishlist entry
        Wishlist.objects.create(
            wishlist_user=user,
            wishlist_productId=product.id,
            wishlist_name=product.pro_name,
            wishlist_image=product.pro_image,
            wishlist_price=product.pro_price
        )
        # Redirect to the wishlist page after adding the item
        return HttpResponseRedirect('/wishlist')



  


     

        



        
   

   




     






























































































































































    
    
        

        

