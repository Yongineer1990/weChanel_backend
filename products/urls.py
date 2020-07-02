from django.urls import path
from .views import (
    LookWishlist,
    ProductWishlist,
    AllLook,
    LookDetail
)

urlpatterns = [
    path('/cruise-2019-20', AllLook.as_view()),
    path('/cruise-2019-20/<int:look_num>', LookDetail.as_view()),
    path('/wishlist/look/<int:look_id>', LookWishlist.as_view()),
    path('/wishlist/prod/<int:product_id>', ProductWishlist.as_view())
]
