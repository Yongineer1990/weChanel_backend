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

class AllLook(View):
    def get(self, request):
        look_info = []
        looks     = Look.objects.all()

        for look in looks:
            image = look.lookimage_set.first()
            look_info.append({
                'id'    : look.id,
                'name'  : look.name,
                'image' : image.url
            })

        return JsonResponse({'look' : look_info}, status=200)

class LookDetail(View):
    def get(self, request, look_num):
        try:
            if Look.objects.filter(id=look_num).exists():
                looks       = Look.objects.prefetch_related('product').get(id=look_num)
                products    = looks.product.all()

                product_info = [{
                    'product_id'    : product.id,
                    'product_name'  : product.name,
                    'product_code'  : product.product_code,
                    'product_price' : product.price,
                    'color'         : [{
                        'color_id'      : color.id,
                        'color_name'    : color.name
                    } for color in product.color.all()],
                    'texture'       : [{
                        'texture_id'    : texture.id,
                        'texture_name'  : texture.name
                    } for texture in product.texture.all()]
                } for product in products]

                look_images = LookImage.objects.filter(look_id=look_num)
                look_image  = [image.url for image in look_images]

                return JsonResponse({
                    'img'        : look_image,
                    'products'   : product_info,
                }, status=200)

            else:
                return JsonResponse(
                    {'Message': f'잘못된 접근 - look_num : {look_num}'},
                    status=400
                )

        except KeyError as e:
            return JsonResponse({'Message': f"KEY ERROR : {e}"}, status=400)

class LookWishlist(View):
    @login_decorator
    def post(self, request, look_id):
        looks           = Look.objects.all()
        user            = Account.objects.get(email=request.userinfo.email).id
        user_lookwish   = Look_wishlist.objects.filter(account_id = user)
        look            = looks.get(id=look_id)

        if user_lookwish.filter(look_id=look).exists():
            Look_wishlist.objects.get(
                account_id = user,
                look_id = look.id
            ).delete()

            return JsonResponse({"message" : f'delete look:{look_id}'}, status=200)

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
            Product_wishlist.objects.get(
                account_id = user,
                product_id = product.id
            ).delete()

            return JsonResponse({"message" : "delete product:{product_id}"}, status=200)

        else:
            Product_wishlist.objects.create(
                account_id = user,
                product_id = product.id
            )

        return JsonResponse({'message' : 'SUCCESS'}, status=200)
