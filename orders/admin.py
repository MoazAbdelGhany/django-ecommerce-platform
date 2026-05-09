from django.contrib import admin
from .models import Order , OrderItem
from django.http import HttpResponse
import csv
import datetime
from django.utils.safestring import mark_safe
from django.urls import reverse
from coupons.models import Coupon

def order_pdf(obj):
    url = reverse('orders:admin_order_pdf',args=[obj.id])
    return mark_safe(f'<a href="{url}" target="bland">PDF</a>')
order_pdf.short_discription = 'Invoice'  # type: ignore


def export_to_csv(modeladmin,request , queryset):
    #HTTP Response
    opts = modeladmin.model._meta
    content_diposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = content_diposition

    #Write into CSV file 
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow(field.verbose_name for field in fields)

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj , field.name)
            if isinstance(value , datetime.datetime):
                value = value.strftime('%d%m%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV' # type: ignore


class OrderItemInline(admin.TabularInline):
    list_display = ['order' , 'product', 'price' , 'quantity']
    model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id' , 'first_name' , 'paid' , 'postal_code', 'created_at',order_pdf]
    inlines = [OrderItemInline]
    actions = [export_to_csv]

