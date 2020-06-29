import bcrypt
import json
import jwt

from chanel.settings import SECRET_KEY
from django.views import View
from django.http import JsonResponse
from .models import Account

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
