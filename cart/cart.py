from decimal import Decimal
from django.conf import settings
from products.models import Product
from django.contrib import messages
from coupons.models import Coupon

class Cart:
    
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart
    
    def __len__(self):
        return len(self.cart)
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            cart_item = self.cart[str(product.id)]
            cart_item_copy = cart_item.copy()
            cart_item_copy['product'] = product
            yield cart_item_copy
    
    
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    
    def update(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id] = {'quantity': quantity}
        
        if self.cart[product_id]['quantity'] > product.max_quantity:
            self.cart[product_id]['quantity'] = product.max_quantity
            messages.warning(self.request, f"You have reached the maximum purchase limit for {product.name}")
        if self.cart[product_id]['quantity'] > product.stock:
            self.cart[product_id]['quantity'] = product.stock
            messages.warning(self.request, f"{product.name} running low on stock")
        if self.cart[product_id]['quantity'] < 0:
            self.cart[product_id]['quantity'] = 1
            messages.warning(self.request, "Minimum one quantity required")
        
        self.save()


    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]

        self.save()
    
    def get_total_price(self):
        total_price = 0
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        for product in products:            
            quantity = self.cart[str(product.id)]['quantity']
            item_price = product.price * quantity
            
            total_price += item_price
        
        if total_price < 0:
            total_price = 0
        
        return total_price
    
    def get_total_discount(self):
        total_discount = 0
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        for product in products:
            if product.is_sale:
                price_diff = product.price - product.sale_price
                quantity = self.cart[str(product.id)]['quantity']
        
                discount = price_diff * quantity
                total_discount += discount
        
        if total_discount < 0:
            total_discount = 0
        
        return round(total_discount, 2)
    
    def get_coupon_discount(self):
        coupon_discount = 0
        coupon_id = self.session.get('coupon_id')
        final_price = Decimal(self.get_final_price())       

        if coupon_id:
            coupon = Coupon.objects.get(id=coupon_id)
            if coupon.is_valid()[0]:
                
                if coupon.discount_type == "Percentage":
                    discount = Decimal(coupon.discount / 100) * final_price
                else:
                    discount = coupon.discount
                
                coupon_discount += discount
                
        if coupon_discount < 0:
            coupon_discount = 0
        
        return round(coupon_discount, 2)
    
    def get_delivery_charge(self):
        delivery_charge = 0
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        for product in products:
            delivery_charge += product.delivery_charge
        
        return round(delivery_charge, 2)
    
    def get_discounted_price(self):
        total_price = self.get_total_price()
        total_discount = self.get_total_discount()
        discounted_price = total_price - total_discount
        
        if discounted_price < 0:
            discounted_price = 0
        
        return round(discounted_price, 2)
        
    
    def get_final_price(self):
        final_price = self.get_discounted_price()
        
        if final_price < 1500:
            delivery_charges = self.get_delivery_charge()
            final_price += delivery_charges
        
        if final_price < 0:
            final_price = 0
        
        return round(final_price, 2)
    
    def get_total_savings(self):
        total_savings = Decimal(self.get_total_discount())
        total_coupon_discount = Decimal(self.get_coupon_discount())
        final_price = Decimal(self.get_final_price())
        
        total_savings += total_coupon_discount
        
        if final_price > 1500:
            delivery_charges = Decimal(self.get_delivery_charge())
            total_savings += delivery_charges
            
        if total_savings < 0:
            total_savings = 0
        
        return round(total_savings, 2)
    
    def get_final_price_after_coupon(self):
        final_price = Decimal(self.get_final_price())
        coupon_discount = Decimal(self.get_coupon_discount())
        
        final_price -= coupon_discount
        
        if final_price < 0:
            final_price = 0
        
        return round(final_price, 2)
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
