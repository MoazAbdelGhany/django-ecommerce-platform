from django.contrib import admin
from django.urls import path , include 
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

#API
from rest_framework_simplejwt.views import (
    TokenObtainPairView ,
    TokenRefreshView ,
)


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('',include('store.urls', namespace='store')),
    path('accounts/', include('accounts.urls',namespace='accounts')),
    path('cart/',include('cart.urls', namespace = 'cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('coupons/', include('coupons.urls', namespace ='coupons')),

    # APIs 
    path('api/v1/', include('apis.urls' , namespace='api')),
    path('api/v1/token/',TokenObtainPairView.as_view() , name='token_obtain_pair'),
    path('api/v1/token/refresh/',TokenRefreshView.as_view() , name='token_refresh'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


