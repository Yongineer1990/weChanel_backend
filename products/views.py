from django.http import JsonResponse
from django.views import View
from .models import Product
import json

class BagView(View):
    def get(self, request):
        total_bag_info = []
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

        for bag in bag_list:
            bag_code                = bag.product_code
            bag_img                 = bag.productimage_set.all()
            bag_img                 = bag_img[0].url
            bag_name                = bag.name
            bag_price               = bag.price
            each_bag                = Product.objects.get(product_code=bag_code)
            textures                = each_bag.texture.all()
            texture_list            = [ texture.name for texture in textures ]

            bag_info                = {}
            bag_info['bag_img']     = bag_img
            bag_info['bag_name']    = bag_name
            bag_info['bag_price']   = bag_price
            bag_info['texture']     = texture_list
            bag_info['bag_code']    = bag_code.replace(' ','')
            total_bag_info.append(bag_info)

        return JsonResponse({'bag_info':total_bag_info}, status=200)

class DetailView(View):
    def get(self, request, bag_code):
        detail_bag_info = {}
        option_num      = 0
        product_list = Product.objects.prefetch_related(
                                                'productimage_set',
                                                'sizeproduct_set',
                                                'material',
                                                'texture',
                                                'color'
                                                ).filter(
                                                name__contains='CHANEL 19'
                                                ).exclude(id__lt=400)

        code_list = [ product.product_code.replace(' ','') for product in product_list ]
        try:
            index = code_list.index(bag_code)
            bag                 = product_list[index]
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
            leather_bag_codes   = []
            tweed_bag_codes     = []
            other_bag_codes     = []

            leather_bags        =  Product.objects.filter(
                                                            material__name='Leather'
                                                         ).filter(name=bag.name)
            leather_dict = {}
            if leather_bags.exists():
                leather_bag_images = [ leather_bag.productimage_set.all()[0].url for leather_bag in leather_bags ]
                leather_bag_codes  =  [leather.product_code.replace(' ','') for leather in leather_bags ]
                length = len(leather_bag_codes)
                option_num        += len(leather_bag_codes)
                for index in range(length):
                   leather_dict[leather_bag_codes[index]] = leather_bag_images[index]

            tweed_bags      = Product.objects.filter(
                                                        material__name='트위드 & 패브릭'
                                                    ).filter(name=bag.name)
            tweed_dict = {}
            if tweed_bags.exists():
                tweed_bag_images = [ tweed_bag.productimage_set.all()[0].url for tweed_bag in tweed_bags ]
                tweed_bag_codes  = [ tweed.product_code.replace(' ','') for tweed in tweed_bags ]
                length = len(tweed_bag_codes)
                option_num      += len(tweed_bag_codes)
                for index in range(length):
                   tweed_dict[tweed_bag_codes[index]] = tweed_bag_images[index]

            other_bags      = Product.objects.filter(
                                                      material__name='기타 재질'
                                                    ).filter(name=bag.name)
            other_dict = {}
            if other_bags.exists():
                other_bag_images = [ other_bag.productimage_set.all()[0].url for other_bag in other_bags ]
                other_bag_codes  = [ other.product_code.replace(' ','') for other in other_bags ]
                length = len(other_bag_codes)
                option_num      += len(other_bag_codes)
                for index in range(length):
                   other_dict[other_bag_codes[index]] = other_bag_images[index]

            detail_bag_info['bag_image_all']        = bag_image_all
            detail_bag_info['bag_texture']          = bag_texture
            detail_bag_info['bag_size_main']        = bag_size_main
            detail_bag_info['bag_size_sub']         = bag_size_sub
            detail_bag_info['bag_color']            = bag_color
            detail_bag_info['bag_code']             = bag_code
            detail_bag_info['bag_price']            = bag_price
            detail_bag_info['bag_name']             = bag_name
            detail_bag_info['opton_num']            = option_num
            detail_bag_info['leather_dict']         = leather_dict
            detail_bag_info['tweed_dict']           = tweed_dict
            detail_bag_info['other_dict']           = other_dict
            return JsonResponse({'detail_bag_info':detail_bag_info}, status=200)

        except ValueError:
            return JsonResponse({'WRONG':'CODE'}, status=405)
