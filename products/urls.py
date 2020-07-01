from django.urls import path
from .views import (
    LookWishlist,
    ProductWishlist
)

urlpatterns = [
    path('/wishlist/look/<int:look_id>', LookWishlist.as_view()),
    path('/wishlist/prod/<int:product_id>', ProductWishlist.as_view())
]


