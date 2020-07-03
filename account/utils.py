import json
import requests
import jwt

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from chanel.settings import SECRET_KEY, ALGORITHM
from .models import Account

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get('Authorization', None)
        
        if token:

            try:
                payload          = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
                userinfo         = Account.objects.get(email=payload['email'])
                request.userinfo = userinfo

                return func(self, request, *args, **kwargs)

            except jwt.exceptions.DecodeError:
                return JsonResponse({'message' : 'INVALID_TOKEN' }, status=400)

            except Account.DoesNotExist:
                return JsonResponse({'message' : 'ACCOUNT_DOES_NOT_EXIST'}, status=400)
            
            return JsonResponse({'message' : 'LOGIN_REQUIRED'}, status=401)
    return wrapper
