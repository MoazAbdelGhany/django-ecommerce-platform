from django.shortcuts import render , redirect , get_object_or_404 
from django.views.decorators.http import require_POST
from .cart import Cart 
from .forms import CartAddProductForm 
from store.models import Product 
from coupons.forms import CouponApplyForm


@require_POST 
def cart_add(request , product_id):
    cart = Cart(request)
    product = get_object_or_404(Product , id = product_id , status=  Product.Status.AVAILABLE)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data 
        cart.add(product=product , quantity = cd['quantity'] , update_quantity=cd['update'])
        next_url = request.POST.get("next")
        if next_url :
            return redirect(next_url)
    return redirect('cart:cart_details')
    
@require_POST    
def cart_remove(request , product_id):
    cart = Cart(request)
    product = get_object_or_404(Product , id = product_id , status = Product.Status.AVAILABLE)
    cart.remove(product=product)
    return redirect('cart:cart_details')

def cart_details(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial ={
            'quantity':item['quantity'],
            'update':True,
        })
    context= {
        'coupon_apply_form':CouponApplyForm()
    }

    return render(request , 'cart/cart_details.html',context )

