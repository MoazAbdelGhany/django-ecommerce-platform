from django.shortcuts import render , get_object_or_404 
from .models import Category , Product 
from django.contrib.postgres.search import SearchVector , SearchQuery , SearchRank
from cart.forms import CartAddProductForm
from django.core.cache import cache
from django.core.paginator import Paginator


def list_products(request , category_slug = None):
    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.all()
        cache.set('categories', categories , 60 * 30)
    cache_key = 'products_list'
    products = cache.get(cache_key)
    if not products:
        products = Product.objects.filter(status = Product.Status.AVAILABLE)
        cache.set('products_list',products , 60 * 30 )
    cart_product_form = CartAddProductForm()
    if category_slug:
        category = get_object_or_404(Category, slug = category_slug)
        products = products.filter(category = category)

    paginator = Paginator(products , 12 )
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'categories':categories,
        'cart_product_form': cart_product_form,
        'page_obj':page_obj ,
    }
    return render(request , 'store/list_products.html', context)


def product_details(request , product_slug):
    cache_key = f'product_{product_slug}'
    product = cache.get(cache_key)
    if product is None:
        product = get_object_or_404(Product , slug = product_slug ,status = Product.Status.AVAILABLE)
        cache.set(cache_key , product , timeout= 60 * 30)
        
    cart_product_form = CartAddProductForm()
    context = {
        'product_details':product , 
        'cart_product_form': cart_product_form,
    }
    return render(request , 'store/products_details.html', context )

def product_search(request):
    query= None 
    results = []
    if 'query' in request.GET:
        query = request.GET.get('query')
        search_vector = SearchVector('name', 'description','category__name')
        search_query = SearchQuery(query)
        results = Product.objects.annotate(
            search = search_vector,
            rank = SearchRank(search_vector, search_query)
        ).filter(search =search_query ,status = Product.Status.AVAILABLE).order_by('-rank')
    context = {
        'query':query,
        'results':results, 
    }
    return render(request , 'store/search_results.html', context)


def why_us(request):
    return render(request,'why.html')

def testimonial(request):
    return render(request, 'testimonial.html')

def about(request):
    return render(request,'about.html')