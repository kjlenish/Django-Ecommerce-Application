from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UpdateCustomerAddressForm
from .models import Address
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


@login_required
def manage_addresses(request):
    user = User.objects.get(username=request.user)
    addresses = Address.objects.filter(user=user)
    
    context = {'addresses': addresses}
    
    return render(request, 'shipping/addresses.html', context)


@login_required
def update_address(request, id):
    address = Address.objects.get(user=request.user, id=id)
    address_form = UpdateCustomerAddressForm(request.POST or None, instance=address)
            
    context = {
        'address_form':address_form
    }
    
    if request.POST:
        if address_form.is_valid():
            address_form.save()
            messages.success(request, "Your Address has been updated")
            return redirect('manage_addresses')
        else:
            messages.warning(request, "Invalid details... Please try again !!")
        
    return render(request, 'shipping/update_address.html', context)


@login_required
def remove_address(request, id):
    address = Address.objects.get(user=request.user, id=id)
    address.delete()
    messages.success(request, "Your Address has been removed")
    return redirect('manage_addresses')