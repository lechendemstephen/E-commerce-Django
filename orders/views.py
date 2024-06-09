from django.shortcuts import render, redirect # type: ignore
from django.http import HttpResponse # type: ignore
from .forms import OrderForm
from .models import Order
import datetime
from django.contrib import messages # type: ignore
# Create your views here.
from carts.models import CartItem


def payments(request): 

    return render(request, 'BestStore/orders/payment.html')




def place_order(request, total=0, quantity=0): 
    current_user = request.user 
    
    # if the cart count is less than or equal zero , redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0 : 
        return redirect('store')
    if request.method == "POST": 
        form = OrderForm(request.POST)
        grand_total = 0 
        tax = 0 
        for cart_item in cart_items: 
            total += (cart_item.product.price * cart_item.quantity)
            quantity = cart_item.quantity
        tax = (2* total) / 100 
        grand_total = total + tax   

        if form.is_valid(): 
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note= form.cleaned_data['order_note']
            data.order_total =grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # generate order number 
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,dt,mt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            # end of generating order number 
            data.order_number = order_number
            data.save()
            messages.success(request, 'order Completed')
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            context = {
                'orders': order,
                'cart_items': cart_items,
                'tax': tax,
                'grand_total': grand_total

            }
            return render(request, 'BestStore/orders/payment.html', context)
        
        else: 
            messages.error(request, 'Order Failed')
            return redirect('checkout')
    

    

           
