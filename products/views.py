from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import  *
from attributes.models import *
import json

class BagView(View):
    def get(self, request):

        total_bag_info = []
        bag_list = Product.objects.filter(name__contains="CHANEL 19").prefetch_related('texture', 'productimage_set')

        for bag in bag_list:
            bag_code            = bag.product_code
            bag_img             = bag.productimage_set.all()
            if bag_img.exists():
                bag_img         = bag_img[0].url
                bag_name        = bag.name
                bag_price       = bag.price
                each_bag        = Product.objects.get(product_code=bag_code)
                textures        = each_bag.texture.all()
                texture_list    = []
                bag_info = {}
                for texture in textures:
                    texture = texture.name
                    texture_list.append(texture)
                bag_info['bag_img']     = bag_img
                bag_info['bag_name']    = bag_name
                bag_info['bag_price']   = bag_price
                bag_info['texture']     = texture_list
                total_bag_info.append(bag_info)

        return JsonResponse({'bag_info':total_bag_info}, status=200)



class DetailView(View):
    def get(self, request, bag_num):
        detail_bag_info = {}
        product_list = Product.objects.prefetch_related(
                                                        'productimage_set',
                                                        'sizeproduct_set',
                                                        'meterial',
                                                        'texture',
                                                        'color'
                                                        ).filter(
                                                                name__contains='CHANEL 19'
                                                                ).exclude(
                                                                            id__lt=400
                                                                         )
        bag_num -= 1
        try:
            bag      = product_list[bag_num]
            bag_image_all       = [ image.url for image in bag.productimage_set.all() ]
            bag_texture         = [ texture.name for texture in bag.texture.all() ]
            bag_size_main       = bag.sizeproduct_set.all()[0].size.size_main
            bag_size_sub        = bag.sizeproduct_set.all()[0].size.size_sub
            bag_color           = [color.name for color in bag.color.all() ]
            bag_code            = bag.product_code
            bag_price           = bag.price
            bag_name            = bag.name
            leather_bag_images  = []
            tweed_bag_images    = []
            other_bag_images    = []

            leather_bags    =  Product.objects.filter(
                                                        meterial__name='Leather'
                                                     ).filter(name=bag.name)
            if leather_bags.exists():
                leather_bag_images = [ leather_bag.productimage_set.all()[0].url for leather_bag in leather_bags ]


            tweed_bags      = Product.objects.filter(
                                                        meterial__name='트위드 & 패브릭'
                                                    ).filter(name=bag.name)
            if tweed_bags.exists():
                tweed_bag_images = [ tweed_bag.productimage_set.all()[0].url for tweed_bag in tweed_bags ]


            other_bags      = Product.objects.filter(
                                                        meterial__name='기타 재질'
                                                    ).filter(name=bag.name)
            if other_bags.exists():
                other_bag_images = [ other_bag.productimage_set.all()[0].url for other_bag in other_bags ]

            detail_bag_info['bag_image_all']        = bag_image_all
            detail_bag_info['bag_texture']          = bag_texture
            detail_bag_info['bag_size_main']        = bag_size_main
            detail_bag_info['bag_size_sub']         = bag_size_sub
            detail_bag_info['bag_color']            = bag_color
            detail_bag_info['bag_code']             = bag_code
            detail_bag_info['bag_price']            = bag_price
            detail_bag_info['bag_name']             = bag_name
            detail_bag_info['leather_bag_images']   = leather_bag_images
            detail_bag_info['tweed_bag_images']     = tweed_bag_images
            detail_bag_info['other_bag_images']     = other_bag_images

            return JsonResponse({'detail_bag_info':detail_bag_info}, status=200)

        except IndexError:
            return JsonResponse({'NO MORE':'BAGS'}, status=405)
        except AssertionError:
            return JsonResponse({'NEGATIVE':'LIST_INDEXIMG'}, status=406)

