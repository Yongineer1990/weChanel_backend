import json
import requests
import jwt

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from chanel.settings import SECRET_KEY, ALGORITHM
from .models import Account


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token            = request.headers.get('Authorization', None)
            payload          = jwt.decode(token, SECRET_KEY, algorithm = ALGORITHM)
            userinfo         = Account.objects.get(email=payload['email'])
            request.userinfo = userinfo

        return func(self, request, *args, **kwargs)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN' }, status=400)

        except Account.DoesNotExist:
            return JsonResponse({'message' : 'This User Does Not Exist'}, status=400)

    return wrapper
