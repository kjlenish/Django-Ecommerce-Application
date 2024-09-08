from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UpdateCustomerAddressForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def add_address(request):
    user = User.objects.get(username=request.user)
    
    if request.method == "POST":
            address_form = UpdateCustomerAddressForm(request.POST)

            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = user
                address.save()
                messages.success(request, "Successfully added new address")
                return redirect('check_out')
            else:
                messages.warning(request, "Failed to add address !!")
    else:
        address_form = UpdateCustomerAddressForm()
        
    context = {'address_form':address_form}
    return render(request, 'shipping/add_address.html', context)