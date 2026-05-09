from django.db import models
from store.models import Product
import secrets , string 
from django.utils import timezone
from django.core.validators import MinValueValidator
from coupons.models import Coupon
from decimal import Decimal


def generate_order_id(length = 8):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters)for i in range(8))
class Order(models.Model):
    order_id = models.CharField(max_length= 8 , unique = True , editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length= 250)
    postal_code = models.PositiveIntegerField()
    city = models.CharField(max_length=100) 
    discount = models.ForeignKey(Coupon, related_name='orders', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default = False)
    class Meta: 
        ordering = ['-created_at']
        indexes = [
            models.Index(fields = ['-created_at'])
        ]

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
    
    def __str__(self):
        return f'Order ID: {self.order_id}'
        
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())   # type: ignore
    
    def get_discount_amount(self):
        if self.discount:
            return Decimal(self.get_total_cost() * self.discount.discount / 100)
        return 0 
    
    def get_tax(self):
        return Decimal(10) 
    
    def get_tax_amount(self):
        return Decimal(self.get_total_cost() * self.get_tax() / 100) 
    
    def get_total_cost_with_discount_and_tax(self):
        total_cost = self.get_total_cost()
        discount_amount = self.get_discount_amount()
        tax_amount = self.get_tax_amount()
        return Decimal(total_cost - discount_amount + tax_amount)
   
    def save(self ,*args , **kwargs): 
        if not self.order_id:
            new_id = generate_order_id()
            while Order.objects.filter(order_id = new_id).exists():
                new_id = generate_order_id()
            self.order_id = new_id 
        super().save(*args , **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order , related_name = 'items' , on_delete= models.CASCADE)
    product = models.ForeignKey(Product , related_name='order_item' , on_delete=models.CASCADE)
    price = models.DecimalField(max_digits = 9 , decimal_places=2 , validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(default = 1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
    
    def get_cost(self):
        return self.price * self.quantity 
    
class OrderPay(models.Model):
    order = models.ForeignKey(Order , on_delete= models.CASCADE)
    pay_phone = models.CharField(max_length=11)
    pay_image = models.ImageField(upload_to = 'payment_image')
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta: 
        ordering = ['-created_at']
    def __str__(self) -> str : 
        return f"Payment for order ID: {self.order.order_id}"
