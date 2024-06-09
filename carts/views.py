from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from store.models import Product, Variations
from .models import Cart, CartItem
from django.http import HttpResponse # type: ignore
from django.core.exceptions import ObjectDoesNotExist # type: ignore # type: ignorm
from django.contrib.auth.decorators import login_required # type: ignore
# Create your views here.
# Creating the cart session from the browser using session and if it does not exist, you create one
def _cart_id(request): 
    cart = request.session.session_key
    if not cart: 
        cart = request.session.create()
    return cart

# adding items to cart using _cart_id, product, and Cartitem 
def add_cart(request, product_id): 
    # For logged in users 
    current_user = request.user
    product = Product.objects.get(id=product_id)
    if current_user.is_authenticated: 
        product_variation = []
        if request.method == "POST":   
            for item in request.POST: 
                key = item 
                value = request.POST[key]
                try: 
                    variation = Variations.objects.get(product=product, varation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(list(variation))
                except: 
                    pass
       # product = Product.objects.get(id=product_id)     
        is_cart_item_exist = CartItem.objects.filter(product=product, user=current_user).exists()    
        if is_cart_item_exist: 
            cart_item = CartItem.objects.filter(product=product, user=current_user) 
            ex_var_list = []
            id = []
            for item in cart_item: 
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list: 
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity +=1 
                item.save()
            else: 
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0 : 
                    item.variations.clear()
                    item.variations.add(*product_variation)         
                item.save()
        else: 
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,     
            )
            if len(product_variation) > 0 : 
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
      # None authenticated user
    else: 
        product_variation = []
        if request.method == "POST":   
            for item in request.POST: 
                key = item 
                value = request.POST[key]
                try: 
                    variation = Variations.objects.get(product=product, varation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except: 
                    pass
        product = Product.objects.get(id=product_id)
        try: 
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart ID present in the session 
        except Cart.DoesNotExist: 
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            ) 
            cart.save()
        
        is_cart_item_exist = CartItem.objects.filter(product=product, cart=cart).exists()    
        if is_cart_item_exist: 
            cart_item = CartItem.objects.filter(product=product, cart=cart)
        
            ex_var_list = []
            id = []
            for item in cart_item: 
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list: 
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity +=1 
                item.save()
            else: 
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0 : 
                    item.variations.clear()
                    item.variations.add(*product_variation)         
                    item.save()
        else: 
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,     
            )
            if len(product_variation) > 0 : 
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')

# reduce item quantity from cart

def remove_cart(request, product_id, cart_item_id): 
    product = get_object_or_404(Product, id=product_id)
    try: 
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else: 
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if cart_item.quantity > 1: 
            cart_item.quantity -= 1 
            cart_item.save()
        else: 
            cart_item.delete()
    except:
        pass
    return redirect('cart')
# delete item completely from cart 
def remove_cart_item(request, product_id, cart_item_id): 
   
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated: 
         cart_item = CartItem.objects.filter(product=product, user=request.user, id=cart_item_id)
         
    else: 
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.filter(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

# add to cart page 

def cart(request, total=0, quantity=0, cart_items=None): 
    try: 
        total = 0
        grand_total = 0
        tax = 0 
        if request.user.is_authenticated: 
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else: 
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items: 
            total += (cart_item.product.price * cart_item.quantity)
        tax = (2* total) / 100 
        grand_total = total + tax
    except ObjectDoesNotExist: 
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        
    }

    return render(request, 'BestStore/store/carts.html', context)

@login_required(login_url="login")
def checkout(request, total=0, quantity=0, cart_items=None): 
    try: 
        tax = 0
        grand_total = 0
        if request.user.is_authenticated: 
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else: 
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items: 
            total += (cart_item.product.price * cart_item.quantity)
        tax = (2* total) / 100 
        grand_total = total + tax
    except ObjectDoesNotExist: 
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        
    }
    return render(request, 'BestStore/store/checkout.html', context)