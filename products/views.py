from django.shortcuts import render
from django.db.models import Q
from .models import Category, Product
from reviews.models import Review

# Create your views here.

def home_view(request):
    try:
        featured_products = Product.objects.filter(is_featured=True)
        new_arrivals = Product.objects.order_by('-date_created')

        context = {"featured_products": featured_products, "new_arrivals": new_arrivals}
        
        return render(request, 'products/home.html', context)
    
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


def product_view(request, filter_category=None):
    try:
        if filter_category:
            category = Category.objects.get(slug=filter_category)
            products = Product.objects.filter(category=category)
        
        else:
            products = Product.objects.all()
        
        context = {'products': products}
        
        return render(request, 'products/products.html', context)
    
    except Exception as e:
        return render(request, 'lost.html')


def filter_product_view(request, sequence):
    try:
        if sequence == 'exclusive':
            products = Product.objects.filter(is_featured=True)
        
        elif sequence == 'new':
            products = Product.objects.order_by('-date_created')
        
        else:
            products = Product.objects.all()
        
        context = {'products': products}
        
        return render(request, 'products/products.html', context)
    except Exception as e:
        return render(request, 'lost.html')

def category_view(request, parent=None):
    try:
        if parent:
            categories = Category.objects.filter(parent_category__slug=parent)
            
            if categories:
                context = {"categories": categories}
                return render(request, 'products/categories.html', context)
            
            return product_view(request, parent)
            
        categories = Category.objects.filter(parent_category__isnull=True)
        context = {"categories": categories}
        
        return render(request, 'products/categories.html', context)
    
    except Exception as e:
        return render(request, 'lost.html')


def get_categories(child_category, category_list = None):
    if category_list is None:
        category_list = []
        
    category_list.append(child_category)
    if child_category.parent_category:
        return get_categories(child_category.parent_category, category_list)
    
    category_list.reverse()
    
    return category_list
        

def product_details(request, pk):
    try:
        product = Product.objects.get(id=pk)
        all_categories = get_categories(product.category)
        
        related_products = Product.objects.filter(category=product.category).exclude(id=product.id)
        
        reviews = Review.objects.filter(product=product)

        context = {"product": product, "all_categories": all_categories, "related_products": related_products, "reviews": reviews}

        return render(request, 'products/product_details.html', context)
    
    except Exception as e:
        return render(request, 'lost.html')
