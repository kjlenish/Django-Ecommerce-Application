from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from products.models import Product
from django.contrib import messages

# Create your views here.


def CartView(request):
    if request.method == 'POST':
        UpdateCart(request)
        
    return render(request, 'cart/cart.html')


def UpdateCart(request):
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

def AddToCart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.update(product)
    return redirect('product', pk=product_id)