from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.views import Token
from rest_framework import status
from django.contrib.auth import authenticate
from .serializer import UserSerializer



@api_view(['POST'])
@parser_classes([JSONParser])
def LoginApi(request):
    if request.method == 'POST':
        data = request.data
        provided_token = request.META.get('HTTP_AUTHORIZATION')


        if provided_token and provided_token.startswith('Bearer '):
            token_key = provided_token.split(' ')[1]
            try:
                token = Token.objects.get(key=token_key)
                user = token.user
                return JsonResponse({
                "first_name": user.first_name
                }, status=status.HTTP_200_OK)

            except Token.DoesNotExist:
                    return JsonResponse({
                        "message": "Invalid token"
                    }, status=status.HTTP_401_UNAUTHORIZED)

        elif data:
            username = data.get('username')
            password = data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                if created == False:
                    token.delete()
                    token = Token.objects.create(user=user)
                return JsonResponse({

                    "message": True,
                    "token" : token.key
                }, status=status.HTTP_200_OK)

            else:
                return JsonResponse({

                    "message": False,
                }, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return JsonResponse({

            "message": "User name and password doesn't exist:",
            }, status=status.HTTP_400_BAD_REQUEST)


        # data = request.data
        # provided_token = request.META.get('HTTP_AUTHORIZATION')
        #
        #
        # if data:
        #
        #     username = data.get('username')
        #     password = data.get('password')
        #     user = authenticate(username=username, password=password)
        #
        #     if user:
        #
        #         token, created = Token.objects.get_or_create(user=user), created = Token.objects.get_or_create(user=user)
        #         if created==False:
        #             token.delete()
        #             token = Token.objects.create(user=user)
        #         Reserver = reserver.objects.filter(userId=user.id).first()
        #
        #
        #         user_info = {
        #             "is_superuser": user.is_superuser,
        #             "first_name": user.first_name,
        #             "last_name": user.last_name,
        #             "email": user.email
        #         }
        #         if Reserver:
        #             reserver_info = {
        #                 "carNo": Reserver.carNo,
        #                 "phnNo": Reserver.phnNo
        #             }
        #             return JsonResponse({
        #                 "user":user_info,
        #                 "reserver": reserver_info,
        #                 "token": token.key,
        #                 "message": True,
        #             }, status=status.HTTP_200_OK)
        #         else:
        #             return JsonResponse({
        #                 "user": user_info,
        #                 "token": token.key,
        #                 "message": True,
        #             }, status=status.HTTP_200_OK)
        #
        #     else:
        #         return JsonResponse({
        #             'error': 'Invalid credentials or token',
        #         }, status=status.HTTP_401_UNAUTHORIZED)
        #
        # else:
        #     if provided_token and provided_token.startswith('Bearer '):
        #         token_key = provided_token.split(' ')[1]
        #
        #         try:
        #             token = Token.objects.get(key=token_key)
        #             user = token.user
        #             Reserver = reserver.objects.filter(userId=user.id).first()
        #
        #             user_info = {
        #                 "is_superuser": user.is_superuser,
        #                 "first_name": user.first_name,
        #                 "last_name": user.last_name,
        #                 "email": user.email
        #             }
        #
        #             if Reserver:
        #                 reserver_info = {
        #                     "carNo": Reserver.carNo,
        #                     "phnNo": Reserver.phnNo
        #                 }
        #                 return JsonResponse({
        #                     "user": user_info,
        #                     "reserver": reserver_info,
        #                     "token": token.key,
        #                     "message": True,
        #                 }, status=status.HTTP_200_OK)
        #             else:
        #                 return JsonResponse({
        #                     "user": user_info,
        #                     "token": token.key,
        #                     "message": True,
        #                 }, status=status.HTTP_200_OK)
        #
        #         except Token.DoesNotExist:
        #             return JsonResponse({
        #                 "message": "Invalid token"
        #             }, status=status.HTTP_401_UNAUTHORIZED)
        #
        #         return JsonResponse({
        #             "message": "Token not provided or invalid format"
        #         }, status=status.HTTP_401_UNAUTHORIZED)