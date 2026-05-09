from django.urls import path 
from . import views 

app_name = 'store'
urlpatterns = [
    path('', views.list_products , name = 'list_products'),
    path('products/<slug:product_slug>/' , views.product_details , name ='product_details'),
    path('category/<slug:category_slug>/', views.list_products , name ='products_by_category'),
    path('search/', views.product_search , name = 'product_search'),
    path('why_us/',views.why_us ,name='why_us'),
    path('testimonial/',views.testimonial,name='testimonial'),
    path('about/',views.about , name='about'),
]
