from django.shortcuts import render , redirect , get_object_or_404
from .models import OrderItem , Order , OrderPay
from .forms import OrderCreateForm , OrderPayForm
from cart.cart import Cart 
from django.contrib import messages
from .tasks import send_mails , payment_completed
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required 
import weasyprint


@staff_member_required
def admin_order_pdf(request , order_id):
    order = get_object_or_404(Order , id= order_id)
    html = render_to_string('orders/pdf.html',{'order':order})
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = f'attachment; filename=order_{order.order_id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response)
    return response


def cart_required(view_func):
    def wrapper(request,*args , **kwargs):
        cart = Cart(request)
        if cart.__len__() == 0:
            messages.error(request , "Your cart is empty")
            return redirect('cart:cart_details')
        return view_func(request , *args , **kwargs)
    return wrapper

@cart_required
def order_create(request):
    cart = Cart(request)
    success = False
    if request.method == "POST":
        form = OrderCreateForm(request.POST) 
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.discount = cart.coupon
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order = order , product = item['product'] , price = item['price'] , quantity = item['quantity'])
         
            cart.clear()
            order_id = order.order_id
            send_mails.delay(order_id)  # type: ignore
            success = True
            return redirect('orders:pay_order' , order_id =order.id)
    else:
        form = OrderCreateForm()
    return render(request , 'orders/created.html',{'form':form , 'success':success})

def order_pay_by_vodafone(request, order_id):
    order = get_object_or_404(Order , id= order_id)
    if request.method == 'POST':
        form = OrderPayForm(request.POST , request.FILES)
        if form.is_valid():
            order_pay:OrderPay = form.save(commit = False)
            order_pay.order = order
            order.paid = True
            order.save()
            order_pay.save()
            return redirect('orders:payment_success',order_id = order.pk)
    else:
        form = OrderPayForm(request.POST , request.FILES)
    context = {
        'form':form,
        'order':order ,
    }
    return render(request,'orders/pay_form.html', context)

def payment_success(request , order_id):
    order = get_object_or_404(Order, id = order_id)
    payment_completed.delay(order.pk) # type: ignore
    return render(request, 'orders/payment_success.html',{'order':order})
