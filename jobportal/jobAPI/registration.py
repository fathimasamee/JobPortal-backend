from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from .serializer import UserSerializer, jobSeekerSerializer
from jobAPI import authview
from rest_framework.authtoken.views import Token
from .models import JobSeeker  # Import your JobSeeker model here

@api_view(['POST'])
@csrf_exempt
@parser_classes([JSONParser])
def RegisterApi(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)

        user_data = data.get('user', {})
        job_seeker_data = data.get('job_seeker', {})  # Assuming job_seeker is a nested object in your request





        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid():
            email = user_data.get('email')
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    "message": "Email already registered",
                }, status=400)

            user_instance = user_serializer.save()

            # Create a JobSeeker instance associated with the registered user
            job_seeker_data['userId'] = user_instance.id
            job_seeker_serializer = jobSeekerSerializer(data=job_seeker_data)
            if job_seeker_serializer.is_valid():
                job_seeker_serializer.save()
                token, created = Token.objects.get_or_create(user=user_instance)
            else:
                # Rollback the user creation if JobSeeker creation fails
                user_instance.delete()
                return JsonResponse({
                    "error": job_seeker_serializer.errors
                }, status=400)

            user_info = {
                "is_superuser": user_instance.is_superuser,
                "first_name": user_instance.first_name,
                "last_name": user_instance.last_name,
                "username": user_instance.username,  # Include username
                "email": user_instance.email,

            }

            return JsonResponse({
                "user": user_info,
                "job_seeker": job_seeker_serializer.data,
                "token": token.key,
                "message": True,
            }, status=200)



        return JsonResponse({
            "error": user_serializer.errors
        }, status=400)
