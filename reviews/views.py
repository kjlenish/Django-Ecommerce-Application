from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from products.models import Product
from .models import Review
from .forms import ProductReviewForm
# Create your views here.


@login_required
def add_review(request, pk):
    try:
        user = User.objects.get(username=request.user)
        product = Product.objects.get(id=pk)
        
        try:
            review = Review.objects.get(user=user, product=product)
            review_form = ProductReviewForm(request.POST or None, instance=review)
        except Review.DoesNotExist:
            review_form = ProductReviewForm(request.POST or None)
        
        context = {"review_form": review_form}
        
        if request.method == 'POST':
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = user
                review.product = product
                review.save()
                messages.success(request, f"Your review has been added")
                return redirect('all_orders')
            else:
                messages.warning(request, f"Failed to add your review")
            
        return render(request, 'reviews/add_review.html', context)
    
    except Exception as e:
        return render(request, 'lost.html')
