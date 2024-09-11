from django.shortcuts import render, redirect
from cart.cart import Cart
from django.contrib.auth.models import User
from .models import Order, OrderItem
from products.models import Product
from shipping.models import Address
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def place_order(request):
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
        return order_summary(request, order)
    

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
        

@login_required 
def order_summary(request, order):
    order_items = OrderItem.objects.filter(order=order)
    context = {'order_items': order_items}
    
    return render(request, 'orders/order_summary.html', context)
    

@login_required
def view_orders(request):
    user = User.objects.get(username=request.user)
    orders = Order.objects.filter(customer=user).exclude(order_status='In Cart')
    
    context = {'orders': orders}
    
    return render(request, 'orders/orders.html', context)