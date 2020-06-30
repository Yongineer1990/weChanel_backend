from django.urls import path, include
from products.views import BagView

urlpatterns = [
                path('products', include('products.urls')),
              ]

