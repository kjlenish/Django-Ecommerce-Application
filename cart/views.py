from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from products.models import Product
from django.contrib import messages
# Create your views here.

def cart_view(request):
    try:
        if request.method == 'POST':
            update_cart(request)
            
        return render(request, 'cart/cart.html')
    
    except Exception as e:
        return render(request, 'lost.html')


def update_cart(request):
    try:
        cart = Cart(request)
        action = request.POST.get('action')
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        
        if action == 'remove':
            cart.remove(product)
            messages.success(request, f"{product.name} is removed from your cart")
        
        if action == 'update':
            quantity = int(request.POST.get('item_quantity'))
            cart.update(product, quantity)
            messages.success(request, "Your cart has been updated")
        
        return redirect('cart')
    
    except Exception as e:
        return render(request, 'lost.html')

def add_to_cart(request, product_id):
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.update(product)
        
        return redirect(product.get_absolute_url())
    
    except Exception as e:
        return render(request, 'lost.html')
