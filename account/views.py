import bcrypt
import json
import jwt

from django.views import View
from django.http import JsonResponse

from chanel.settings import SECRET_KEY
from account.decorator import login_decorator
from .models import (
    Account,
    Look_wishlist,
    Product_wishlist
)
from products.models import (
    Look,
    Product,
    ProductCategory,
    Menu
)
from attributes.models import (
    LookImage,
    ProductImage,
    TextureProduct
)

class SignUpView(View):
    def post(self, request):
        user_data = json.loads(request.body)
        try:
            if Account.objects.filter(email = user_data['email']).exists():
                return JsonResponse({"message":"Already Exists"}, status = 400)

            password = user_data['password'].encode('utf-8')
            password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())
            password_crypt = password_crypt.decode('utf-8')

            Account(
                email      = user_data['email'],
                first_name = user_data['first_name'],
                last_name  = user_data['last_name'],
                password   = password_crypt
                ).save()

            return JsonResponse({"message":"SIGNUP_SUCCESS"}, status = 200)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)

class SignInView(View):
    def post(self, request):
        user_data = json.loads(request.body)

        try:
            if Account.objects.filter(email = user_data['email']).exists():
                user = Account.objects.get(email = user_data['email'])

                if bcrypt.checkpw(user_data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({'email' : user_data['email']}, SECRET_KEY, algorithm = "HS256")
                    token = token.decode('utf-8')
                    return JsonResponse({"Access Token": token }, status = 200)

                else:
                    return JsonResponse({"message":"INCORRECT_PASSWORD"}, status = 401)
            else:
                return JsonResponse({"message":"INCORRECT_EMAIL"}, status = 400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)

class Wishlist(View):
    @login_decorator
    def get(self, request):
        look_wishlist = []
        prod_wishlist = []

        uid             = Account.objects.get(email = request.userinfo.email).id
        lookwishes      = Look_wishlist.objects.filter(account_id = uid)
        productwishes   = Product_wishlist.objects.filter(account_id = uid)

        for lookwish in lookwishes:
            look_images = [look_img.url for look_img in LookImage.objects.filter(look_id = lookwish.look.id)]
            look_image  = look_images[0]

            look_wishlist.append({
                'collection_id'     : lookwish.look.collection.id,
                'collection_name'   : lookwish.look.collection.name,
                'look_id'           : lookwish.look.id,
                'look_name'         : lookwish.look.name,
                'look_image'        : look_image
            })

        for productwish in productwishes:
            product_images  = ProductImage.objects.filter(product_id = productwish.product.id).first().url
            product_texture = [prod_texture.texture.name for prod_texture in TextureProduct.objects.filter(product_id = productwish.product.id)]
            menu            = ProductCategory.objects.filter(product_id = productwish.product.id).first().category.menu.name

            prod_wishlist.append({
                'menu'              : menu,
                'product_id'        : productwish.product.id,
                'product_name'      : productwish.product.name,
                'product_price'     : productwish.product.price,
                'product_texture'   : product_texture,
                'image'             : product_images

            })

        return JsonResponse({
            'look_wishlist' : look_wishlist,
            'prod_wishlist' : prod_wishlist
        }, status=200)
