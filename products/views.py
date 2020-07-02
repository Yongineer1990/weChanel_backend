import json

from django.views import View
from django.http import JsonResponse

from .models import Look
from attributes.models import (
    LookImage,
    Color,
    Texture
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

