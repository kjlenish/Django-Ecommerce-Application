from django.shortcuts import redirect, render
from .models import Coupon
from django.contrib import messages
from cart.cart import Cart


# Create your views here.

def apply_coupon(request):
    coupon_id = request.session.get('coupon_id')
    if coupon_id:
        coupon = Coupon.objects.get(id=coupon_id)
    else:
        coupon = None
    
    if request.method == "POST":
        code = request.POST.get('code')
        
        try:
            coupon = Coupon.objects.get(code=code)
            is_valid, message = coupon.is_valid()
            
            if is_valid:
                cart = Cart(request)
                cart_price = cart.get_final_price()
                
                if coupon.minimum_purchase_amount:
                    if cart_price < coupon.minimum_purchase_amount:
                        messages.warning(request, "Minimum cart value not met for this coupon")
                        return redirect('apply_coupon')
                
                request.session['coupon_id'] = coupon.id
                messages.success(request, "Coupon applied successfully!")
                
                return redirect('cart')

            else:
                messages.warning(request, str(message))
        
        except Coupon.DoesNotExist:
            messages.warning(request, "The Coupon is Invalid")
    
    context = {'coupon': coupon}
    return render(request, 'coupons/apply_coupon.html', context)
        

def remove_coupon(request):
    del request.session['coupon_id']
    return redirect('apply_coupon')
