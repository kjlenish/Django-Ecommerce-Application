from .models import Payment

# Create your views here.

def initialize_payment(order, razor_payment):
    payment, created = Payment.objects.get_or_create(order=order, payment_status='Payment Initiated')
    payment.billing_amount = razor_payment['amount']
    payment.billing_address = order.customer.addresses.get(is_primary=True)
    payment.save()
    

def get_payment_status(payment_id, response, client):
    payment = Payment.objects.get(id=payment_id)

    razorpay_payment_id = response['razorpay_payment_id']
    razorpay_signature = response['razorpay_signature']
    
    
    payment_success = client.utility.verify_payment_signature({
        'razorpay_order_id': payment.order.razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
        })
    
    if payment_success:
        payment.razorpay_payment_id = razorpay_payment_id
        
        payment_details = client.payment.fetch(razorpay_payment_id)
        payment.payment_method = payment_details['method']
        
        if payment_details['status'] == "captured":
            payment.payment_status = 'Payment Received'
        else:
            payment.payment_status = 'Payment Not Received'
            
        payment.save()
        
        return True
    else:
        return False
