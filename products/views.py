import json

from django.views import View
from django.http import JsonResponse

from account.decorator import login_decorator
from .models import (
    Look,
    Product
)
from attributes.models import (
    LookImage,
    Color,
    Texture
)
from account.models import (
    Account,
    Look_wishlist,
    Product_wishlist
)

class LookWishlist(View):
    @login_decorator
    def post(self, request, look_id):
        looks           = Look.objects.all()
        user            = Account.objects.get(email=request.userinfo.email).id
        user_lookwish   = Look_wishlist.objects.filter(account_id = user)
        look            = looks.get(id=look_id)

        if user_lookwish.filter(look_id=look).exists():
            return JsonResponse({"message" : "이미 있는 아이템"}, status=200)
        else:
            Look_wishlist.objects.create(
                account_id  = user,
                look_id     = look.id
            )

        return JsonResponse({'message' : 'SUCCESS'}, status=200)

class ProductWishlist(View):
    @login_decorator
    def post(self, request, product_id):
        products        = Product.objects.all()
        user            = Account.objects.get(email=request.userinfo.email).id
        user_prodwish   = Product_wishlist.objects.filter(account_id=user)
        product         = products.get(id=product_id)

        if user_prodwish.filter(product_id=product).exists():
            return JsonResponse({"message" : "이미 있는 아이템"}, status=200)
        else:
            Product_wishlist.objects.create(
                account_id = user,
                product_id = product.id
            )

        return JsonResponse({'message' : 'SUCCESS'}, status=200)
