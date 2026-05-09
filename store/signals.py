from django.db.models.signals import post_save , post_delete
from django.core.cache import cache 
from django.dispatch import receiver 
from .models import Product,Category

@receiver(post_save, sender=Product)
def clear_products_cache_on_save(sender,instance,**kwargs):
    cache.delete("products_list")

@receiver(post_delete,sender=Product)
def clear_products_cache_on_delete(sender , instance , **kwargs):
    cache.delete("products_list")

@receiver(post_save , sender=Category)
def clear_category_cache_on_save(sender,instance , **kwargs):
    cache.delete("categories")

@receiver(post_delete,sender=Category)
def clear_category_cache_on_delete(sender , instance, **kwargs):
    cache.delete("categories")