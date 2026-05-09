from django.urls import path
from . import views

app_name = 'api' 

urlpatterns = [
    path('category/', views.category_api , name ='category_api'),
    path('category/<slug:slug>/', views.category_api , name ='category_api'),
    path('product/', views.product_api , name = 'product_api'),
    path('product/<slug:slug>/', views.product_api , name = 'product_api'),
    path('register/', views.registrationUserView , name = 'register'),
    path('activate/<uid64>/<token>', views.activationView , name = 'activatation_email'),
    path('logout/',views.logout , name='logout_api')
]