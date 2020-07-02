from django.http import JsonResponse
from django.views import View
from .models import Product
import json

class BagView(View):
    def get(self, request):
        total_bag_info    = []
        collection_option = request.GET.getlist('collection_id__in')
        theme_option      = request.GET.getlist('theme__in')
        shape_option      = request.GET.getlist('shape__in')
        material_option   = request.GET.getlist('material__in')

        filters                      = {}
        filters['collection_id__in'] = collection_option
        filters['theme__in']         = theme_option
        filters['shape__in']         = shape_option
        filters['material__in']      = material_option

        new_filters = {}
        for key, value in filters.items():
            if value:
                new_filters[key] = value
        bag_list = Product.objects.filter(
            name__contains="CHANEL 19"
        ).prefetch_related(
                            'texture',
                            'productimage_set'
        ).exclude(id__lt=400).filter(**new_filters)

        total_bag_info = [
            {
                'bag_code'          : bag.product_code.replace(' ',''),
                'bag_img'           : bag.productimage_set.all()[0].url,
                'bag_name'          : bag.name,
                'bag_price'         : bag.price,
                'texture'           : [ texture.name for texture in bag.texture.all() ]
            } for bag in bag_list
        ]
        return JsonResponse({'bag_info':total_bag_info}, status=200)

class DetailView(View):
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
            return JsonResponse({'WRONG':'CODE'}, status=405)
