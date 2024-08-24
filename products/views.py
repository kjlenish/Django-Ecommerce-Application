from django.shortcuts import render
from . models import Category, Product

# Create your views here.

def HomeView(request):
    featured_products = Product.objects.filter(is_featured=True)
    new_arrivals = Product.objects.order_by('-date_created')

    context = {"featured_products": featured_products, "new_arrivals": new_arrivals}
    return render(request, 'products/home.html', context)


def ProductView(request, filter_category=None):
    if filter_category:
        category = Category.objects.get(slug=filter_category)
        products = Product.objects.filter(category=category)
    
    else:
        products = Product.objects.all()
    
    context = {'products': products}
    
    return render(request, 'products/products.html', context)


def OrderByProductView(request, sequence):
    if sequence == 'exclusive':
        products = Product.objects.filter(is_featured=True)
    
    elif sequence == 'new':
        products = Product.objects.order_by('-date_created')
    
    else:
        products = Product.objects.all()
    
    context = {'products': products}
    
    return render(request, 'products/products.html', context)


def CategoryView(request, parent=None):
    if parent:
        categories = Category.objects.filter(parent_category__slug=parent)
        
        if categories:
            context = {"categories": categories}
            return render(request, 'products/categories.html', context)
        
        return ProductView(request, parent)
        
    categories = Category.objects.filter(parent_category__isnull=True)
    context = {"categories": categories}
    return render(request, 'products/categories.html', context)


def get_categories(child_category, category_list = None):
    if category_list is None:
        category_list = []
        
    category_list.append(child_category)
    if child_category.parent_category:
        return get_categories(child_category.parent_category, category_list)
    
    category_list.reverse()
    return category_list
        

def ProductDetails(request, pk):
    product = Product.objects.get(id=pk)
    all_categories = get_categories(product.category)
    
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)

    context = {"product": product, "all_categories": all_categories, "related_products": related_products}

    return render(request, 'products/product_details.html', context)