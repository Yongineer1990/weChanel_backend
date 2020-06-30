from .models import Look
from attributes.models import LookImage, Color, Texture
import json
from django.views import View
from django.http import JsonResponse

class AllLook(View):
    def get(self, request):
        look_info = {}
        look_image  = LookImage.objects.select_related('look').all()
        for qs in look_image:
            id      = qs.look.id
            name    = qs.look.name

            look_info[id]           = {}
            look_info[id]['name']   = name

            urls_list = []
            for urls in look_image.filter(look=qs.look.id):
                urls_list.append(urls.url.strip())
            look_info[id]['img'] = urls_list[0]

        return JsonResponse({"look" : look_info}, status=200)

class LookDetail(View):
    def post(self, request, look_num):
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
                    color_info.append(color.name)

                textures = product.texture.all()
                for texture in textures:
                    texture_info.append(texture.name)

                product_info.append({
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

