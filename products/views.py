from .models import Look
from attributes.models import LookImage, Color, Texture
import json
from django.views import View
from django.http import JsonResponse

class AllLook(View):
    def get(self, request):
        look_info = []
        images  = LookImage.objects.select_related('look').all()
        looks    = Look.objects.all()
        for look in looks:
            image = images.filter(look = look.id)[0]
            look_info.append({
                'id'    : look.id,
                'name'  : look.name,
                'image' : image.url
            })

        return JsonResponse({'look' : look_info}, status=200)

class LookDetail(View):
    def get(self, request, look_num):
        try:
            look_detail = []
            looks       = Look.objects.all().prefetch_related('product')
            look        = looks.get(id=look_num)
            products    = look.product

            for product in products.all():
                print(product.product_code)
                product_info    = []
                color_info      = []
                texture_info    = []

                colors = product.color.all()
                for color in colors:
                    color_info.append({
                        'id'    : color.id,
                        'name'  : color.name
                    })

                textures = product.texture.all()
                for texture in textures:
                    texture_info.append({
                        'id'    : texture.id,
                        'name'  : texture.name
                    })

                product_info.append({
                    'product_id'    : product.id,
                    'Product_code'  : product.product_code,
                    'Name'          : product.name,
                    'price'         : product.price,
                    'color'         : color_info,
                    'texture'       : texture_info

                })
                look_detail.append(product_info)

            look_images = LookImage.objects.filter(look_id=look_num)
            look_image  = []
            for image in look_images:
                look_image.append(image.url)

            return JsonResponse({
                'img'       : look_image,
                'products'   : look_detail,
            }, status=200)

        except KeyError as e:
            return JsonResponse({'Message': f"KEY ERROR! : {e}"}, status=400)

        except Look.DoesNotExist:
            return JsonResponse({'Message': f'잘못된 접근 - look_num : {look_num}'}, status=400)

