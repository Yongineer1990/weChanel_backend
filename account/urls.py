from django.urls import path
from .views import (
    SignUpView,
    SignInView,
    Wishlist
)

urlpatterns = [
    path('/sign-up', SignUpView.as_view()),
    path('/sign-in', SignInView.as_view()),
    path('/wishlist', Wishlist.as_view())
]
