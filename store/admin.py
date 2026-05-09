from django.contrib import admin

from .models import Category , Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields =['slug']
    list_display = ['name' , 'created_at','pk']
    search_fields = ['name', 'price']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields =['slug']
    list_display = ['name' , 'price', 'status' , 'updated_at']
    search_fiedlds =['name']