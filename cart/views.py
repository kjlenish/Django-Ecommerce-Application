import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from products.models import Product
# Create your views here.

def cart_view(request):
    try:
          
        return render(request, 'cart/cart.html')
    
    except Exception as e:
        return render(request, 'lost.html')


def update_cart(request):
    try:
        cart = Cart(request)
        data = json.loads(request.body)
        action = data.get('action')
        product_id = data.get('product_id')
        
        product = get_object_or_404(Product, id=product_id)
        
        if action == 'remove':
            cart.remove(product)
        
        if action == 'update':
            quantity = data.get('item_quantity')
            cart.update(product, quantity)
        
        cart_length = cart.__len__()
        total_price = cart.get_total_price()
        total_discount = cart.get_total_discount()
        delivery_charge = cart.get_delivery_charge()
        discounted_price = cart.get_discounted_price()
        final_price = cart.get_final_price()
        total_savings = cart.get_total_savings()
        

        delivery_charge_display = {
            'charge': delivery_charge,
            'is_free': discounted_price > 1500,
        }

        return JsonResponse({
            'success': True,
            'cart_length': cart_length,
            'total_price': total_price,
            'total_discount': total_discount,
            'delivery_charge': delivery_charge_display['charge'],
            'is_free_delivery': delivery_charge_display['is_free'],
            'final_price': final_price,
            'total_savings': total_savings
        })      
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def add_to_cart(request, product_id):
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.update(product)
        
        return redirect(product.get_absolute_url())
    
    except Exception as e:
        return render(request, 'lost.html')
