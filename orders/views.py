from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from cart.cart import Cart
from django.contrib.auth.models import User
from .models import Order, OrderItem
from products.models import Product
from shipping.models import Address
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from payments.views import initialize_payment, get_payment_status
import razorpay
import math

# Create your views here.

@login_required
def place_order(request):
    try:
        cart = Cart(request)
        user = User.objects.get(username=request.user)
        
        order, created = Order.objects.get_or_create(customer=user, order_status='In Cart')
        order.order_amount = cart.get_final_price()
        
        if request.POST:
            address_id = request.POST.get('address_id')
            make_default = request.POST.get('make_default')
            
            address = Address.objects.get(id = address_id)
            
            if make_default:
                address.save(is_default=True)
            
            order.shipping_address = address
            order.save()
            
            return process_order(request, order.id)
        

        for product_id, attribute in cart.cart.items():
            product = Product.objects.get(id=product_id)
            price = product.price
            if product.is_sale:
                price = product.sale_price
                
            order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
            order_item.quantity = attribute['quantity']
            order_item.price = price
            order_item.save()
        order.save()
        
        cart_products = [product_id for product_id in cart.cart.keys()]
        order_items = OrderItem.objects.filter(order=order).exclude(product__id__in=cart_products)
        for order_item in order_items:
            order_item.delete()
        
        try:
            default_address = Address.objects.get(user=user, is_default=True)
        except Address.DoesNotExist:
            default_address = None
        addresses = Address.objects.filter(user=user).exclude(is_default=True)
            
        context = {'order': order, 'default_address': default_address , 'addresses': addresses}
        
        return render(request, 'orders/delivery_details.html', context)
    
    except Exception as e:
        return render(request, 'lost.html')
 
 
def round_up_amount(amount):
    rounded_amount = math.ceil(amount) * 100

    if rounded_amount % 10 != 0:
        rounded_amount = ((rounded_amount // 10) + 1) * 10

    return rounded_amount
       

@login_required 
def process_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        order_items = OrderItem.objects.filter(order=order)
        client = razorpay.Client(auth=(settings.RAZORPAY_ID_KEY, settings.RAZORPAY_SECRET_KEY))
        
        amount = round_up_amount(order.order_amount)
        data = {"amount": amount, "currency": "INR"}
        razor_payment = client.order.create(data=data)
        
        if razor_payment['status'] == 'created':
            order.razorpay_order_id = razor_payment['id']
            order.save()
            
            initialize_payment(order, razor_payment)

        else:
            messages.warning(request, "Payment gateway down... Please try again !!")
            return redirect('cart')

        
        context = {'order': order, 'order_items': order_items, 'razorpay_key_id': settings.RAZORPAY_ID_KEY, 
                'amount': amount}
        
        return render(request, 'orders/order_summary.html', context)
    
    except Exception as e:
        return render(request, 'lost.html')


@login_required
@csrf_exempt
def order_summary(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        client = razorpay.Client(auth=(settings.RAZORPAY_ID_KEY, settings.RAZORPAY_SECRET_KEY))
        
        if request.method == 'POST':
            response = request.POST
            payment_success = get_payment_status(order.payment.id, response, client)
            
            if payment_success:
                order.order_status = 'Order Confirmed'
                order.save()          
                
                cart = Cart(request)
                cart.clear()

                messages.success(request, "Your order has been confirmed")
                return redirect('all_orders')
            
            
            
        messages.warning(request, "Payment failed... Try again")
        return redirect('cart')  
    
    except Exception as e:
        return render(request, 'lost.html')  
        

@login_required
def view_orders(request):
    try:
        user = User.objects.get(username=request.user)
        orders = Order.objects.filter(customer=user).exclude(order_status='In Cart')
        
        context = {'orders': orders}
        
        return render(request, 'orders/orders.html', context)
    
    except Exception as e:
        return render(request, 'lost.html')


@login_required
def order_details(request, pk):
    try:
        order = Order.objects.get(id=pk)
        context = {'order': order}
        
        return render(request, 'orders/order_details.html', context)
    
    except Exception as e:
        return render(request, 'lost.html')
