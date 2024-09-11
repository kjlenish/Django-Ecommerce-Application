from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import CustomerProfile
from .forms import SignUpForm, CustomerProfileForm, LoginForm, CommonContactForm, UserUpdateForm, UpdateCustomerProfileForm, UpdatePasswordForm
from shipping.forms import CustomerAddressForm, UpdateCustomerAddressForm
from shipping.models import Address
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q
from products.models import Product
from cart.cart import Cart

# Create your views here.

def user_login(request):
    try:
        if request.method == 'POST':
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                
                cart = Cart(request)
                user_profile = CustomerProfile.objects.get(user = request.user)
                cart.cart = user_profile.previous_cart
                cart.save()

                messages.success(request, "Logged in successfully")
                
                return redirect(request.GET.get('next', 'home'))
                
            else:
                messages.warning(request, "Invalid details... Please try again !!")

        else:
            form = LoginForm()

        return render(request, 'accounts/login.html', {'form': form})
    
    except Exception as e:
        return render(request, 'lost.html')


@login_required
def user_logout(request):
    try:
        cart = Cart(request)       
        user_profile = CustomerProfile.objects.get(user = request.user)

        user_profile.previous_cart=cart.cart
        user_profile.save()
        
        logout(request)
        messages.success(request, "You have been logged out... Seen you soon")
        return render(request, 'accounts/logout.html')
    
    except Exception as e:
        return render(request, 'lost.html')


def user_register(request):
    try:
        if request.method == "POST":
            form = SignUpForm(request.POST)

            if form.is_valid():
                form.save()
                
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password1"]
                user = authenticate(username=username, password=password)
                login(request, user)
                
                messages.success(request, f"Account created for {username}... Please complete your profile information")
                return redirect('details')
            else:
                messages.warning(request, "Failed to create account !!")
        else:
            form = SignUpForm()
        
        context = {'form':form}
        return render(request, 'accounts/register.html', context)

    except Exception as e:
        return render(request, 'lost.html')


@login_required
def user_details(request):
    try:
        user = User.objects.get(username=request.user)
        
        try:
            profile = request.user.customer_profile
            profile_form = CustomerProfileForm(request.POST or None, instance=profile)
        except CustomerProfile.DoesNotExist:
            profile_form = CustomerProfileForm(request.POST or None)
            
        try:
            address = Address.objects.get(user=request.user, is_primary=True)
            address_form = CustomerAddressForm(request.POST or None, instance=address)
        except ObjectDoesNotExist:
            address_form = CustomerAddressForm(request.POST or None)
        
        contact_form = CommonContactForm(request.POST or None)
        
        context = {
            'profile_form': profile_form,
            'address_form': address_form,
            'contact_form': CommonContactForm(initial={
                'email': profile.email if profile.email is not None else '',
                'country_code': profile.country_code if profile.country_code is not None else '',
                'phone': profile.phone if profile.phone is not None else ''
            })
            }
        
        if request.method == 'POST':        
            if profile_form.is_valid() and address_form.is_valid() and contact_form.is_valid():
                profile = profile_form.save(commit=False)
                address = address_form.save(commit=False)
                profile.user = address.user = request.user
                
                profile.email = address.email = contact_form.cleaned_data['email']
                profile.country_code = address.country_code = contact_form.cleaned_data['country_code']
                profile.phone = address.phone = contact_form.cleaned_data['phone']
                
                
                address.first_name = address.user.first_name
                address.last_name = address.user.last_name
                address.is_primary = True
                address.save()
                
                profile.primary_address = address
                profile.save()
                
                user.email = contact_form.cleaned_data['email']
                user.save()
                
                messages.success(request, f"Your details has been added")
                return redirect('home')
            else:
                messages.warning(request, "Invalid details... Please try again !!")
        
        return render(request, 'accounts/user_details.html', context)

    except Exception as e:
        return render(request, 'lost.html')


@login_required
def user_profile(request, username):
    try:
        try:
           user = User.objects.get(username=username)
           
        except User.DoesNotExist:
            raise Http404()
            
        try:
            profile = user.customer_profile
        except ObjectDoesNotExist:
            profile = None
        
        context = {
            'user_obj': user,
            'profile_obj': profile,
        }
                       
        
        return render(request, 'accounts/profile.html', context)
        
    except Exception as e:
        return render(request, 'lost.html')


@login_required
def update_user_profile(request, username):
    try:    
        try:
           user = User.objects.get(username=username)
           user_form = UserUpdateForm(request.POST or None, instance=user)
        except User.DoesNotExist:
            user_form = UserUpdateForm(request.POST or None)
            
        try:
            profile = user.customer_profile
            profile_form = UpdateCustomerProfileForm(request.POST or None, instance=profile)
        except CustomerProfile.DoesNotExist:
            profile_form = UpdateCustomerProfileForm(request.POST or None)
                
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            }
        
        if request.POST:
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save(commit=False)
                user.email = profile_form.cleaned_data['email']
                
                profile_form.save()
                user.save()
                
                messages.success(request, "Your profile has been updated")
                return redirect('profile', username = username)
            else:
                messages.warning(request, "Invalid details... Please try again !!")
        
        return render(request, 'accounts/update_profile.html', context)
    
    except Exception as e:
        return render(request, 'lost.html')
    

@login_required
def update_primary_address(request, username):
    try:
        try:
            user = User.objects.get(username=username)
            address = Address.objects.get(user=user, is_primary=True)
            address_form = UpdateCustomerAddressForm(request.POST or None, instance=address)
        except Address.DoesNotExist:
            address_form = UpdateCustomerAddressForm(request.POST or None)
            
        context = {
            'address_form':address_form
        }
        
        if request.POST:
            if address_form.is_valid():
                address_form.save()
                messages.success(request, "Your Primary Address has been updated")
                return redirect('profile', username = username)
            else:
                messages.warning(request, "Invalid details... Please try again !!")
            
        return render(request, 'shipping/update_address.html', context)
    
    except Exception as e:
        return render(request, 'lost.html')


@login_required
def update_user_password(request, username):
    try:    
        user = User.objects.get(username=username)
        if request.method == "POST":
            user_form = UpdatePasswordForm(user, request.POST)

            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Your password has been updated....\nPlease Log in again")
                return redirect('login')
            else:
                messages.warning(request, "Invalid details... Please try again !!")
                return redirect("update_password", username = username)
        else:
            user_form = UpdatePasswordForm(user)
            context = {"user_form": user_form}
        return render(request, 'accounts/update_password.html', context)
    
    except Exception as e:
        return render(request, 'lost.html')
    

def search(request):
    try:
        if request.GET:
            search_element = request.GET.get('search_element')
            
            products = Product.objects.filter(Q(name__icontains=search_element) | Q(category__name__icontains=search_element) | Q(description__icontains=search_element))
                    
            context = {'products': products}
        
        return render(request, 'products/products.html', context)
    
    except Exception as e:
        return render(request, 'lost.html')