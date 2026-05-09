from django.conf import settings
from django.core.mail import send_mail , EmailMessage
from celery import shared_task 
from .models import Order 
from django.template.loader import render_to_string
import weasyprint
from io import BytesIO

@shared_task
def send_mails(order_id) -> int: 
    order = Order.objects.get(order_id = order_id)
    subject = f"Order ID: {order.order_id}"
    message = f"Dear {order.get_full_name()}, \n You have successfully placed an order.\n Your Order ID: {order.order_id}"
    from_email = settings.DEFAULT_FROM_EMAIL 
    mail_sent =  send_mail(subject , message, from_email , [order.email])
    return mail_sent 

@shared_task
def payment_completed(order_id):
    order = Order.objects.get(id = order_id)
    subject = f'My Shop - Invoice. {order.order_id}'
    message = f'Hello {order.get_full_name()}, \nPlease find attached the invoice for your recent purchase'
    from_email = settings.DEFAULT_FROM_EMAIL
    email_user = [order.email]

    html = render_to_string('orders/pdf.html',{'order':order})
    out = BytesIO()
    weasyprint.HTML(string=html).write_pdf(out)
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to= email_user,
    )
    mail.attach(f'order {order.order_id}.pdf', out.getvalue(), 'application/pdf')
    mail.send()
    return True