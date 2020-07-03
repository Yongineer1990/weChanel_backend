import json

from django.http import JsonResponse
from django.views import View

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

class BagView(View):
    def get(self, request):
        collection_option = request.GET.getlist('collection_id__in')
        theme_option      = request.GET.getlist('theme__in')
        shape_option      = request.GET.getlist('shape__in')
        material_option   = request.GET.getlist('material__in')

        filters                      = {}
        if collection_option:
            filters['collection_id__in'] = collection_option
        if theme_option:
            filters['theme__in']         = theme_option
        if shape_option:
            filters['shape__in']         = shape_option
        if material_option:
            filters['material__in']      = material_option

        bag_list = Product.objects.filter(
            name__contains="CHANEL 19"
        ).prefetch_related(
            'texture',
            'productimage_set'
        ).exclude(id__lt=400).filter(**filters)

        total_bag_info = [
            {
                'bag_code'          : bag.product_code.replace(' ',''),
                'bag_img'           : bag.productimage_set.all()[0].url,
                'bag_name'          : bag.name,
                'bag_price'         : bag.price,
                'texture'           : [texture.name for texture in bag.texture.all()]
            } for bag in bag_list
        ]
        return JsonResponse({'bag_info':total_bag_info}, status=200)

class BagDetail(View):
    def get(self, request, query_bag_code):
        product_list = Product.objects.prefetch_related(
            'productimage_set',
            'sizeproduct_set',
            'material',
            'texture',
            'color'
        ).filter(name__contains='CHANEL 19').exclude(id__lt=400)

        try:
            bag_list = [product.product_code.replace(' ','') for product in product_list]
            index    = bag_list.index(query_bag_code)
            req_bag  = product_list[index]

            detail_bag_info = {
                'bag_image_all'    : [image.url for image in req_bag.productimage_set.all()],
                'bag_texture'      : [texture.name for texture in req_bag.texture.all()],
                'bag_size_main'    : req_bag.sizeproduct_set.all()[0].size.size_main,
                'bag_size_sub'     : req_bag.sizeproduct_set.all()[0].size.size_sub,
                'bag_color'        : [color.name for color in req_bag.color.all()],
                'bag_code'         : req_bag.product_code,
                'bag_price'        : req_bag.price,
                'bag_name'         : req_bag.name,
                'option_num'       : product_list.filter(name=req_bag.name).count(),
                'leather_bag_info' : [
                    {
                        'code' : product.product_code.replace(' ',''),
                        'image': product.productimage_set.all()[0].url
                    }
                    for product in product_list.filter(
                        name=req_bag.name,
                        material__name='Leather'
                        )
                ],
                'tweed_bag_info'   : [
                    {
                        'code'  : product.product_code.replace(' ',''),
                        'image' : product.productimage_set.all()[0].url
                    }
                    for product in product_list.filter(
                        name=req_bag.name,
                        material__name='트위드 & 패브릭'
                        )
                ],
                'other_bag_info '  : [
                    {
                        'code' : product.product_code.replace(' ',''),
                        'image': product.productimage_set.all()[0].url
                    }
                    for product in product_list.filter(
                        name=req_bag.name,
                        material__name='기타 재질'
                        )
                ]
            }
            return JsonResponse({'detail_bag_info':detail_bag_info}, status=200)
        except ValueError:
            return JsonResponse({'Message':'WRONG_CODE'}, status=409)

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
