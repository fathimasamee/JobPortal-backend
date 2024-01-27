
from .serializer import UserSerializer, jobSeekerSerializer
from rest_framework.authtoken.views import Token
from rest_framework import status, viewsets
from .models import JobSeeker, User
from rest_framework.views import APIView
from rest_framework.response import Response




class userViewSet(APIView):
    def validateSuperToken(self,token):
        if token and token.startswith('Bearer '):
            token_key = token.split(' ')[1]
            try:
                token_obj = Token.objects.get(key=token_key)
                user = token_obj.user
                if user.is_superuser == 1:
                    return True
                else:
                    return False
            except Token.DoesNotExist:
                return False
        else:
            return False

    def validateToken(self,token):
        if token and token.startswith('Bearer '):
            token_key = token.split(' ')[1]
            try:
                token_obj = Token.objects.get(key=token_key)
                user = token_obj.user
                return user
            except Token.DoesNotExist:
                return False
        else:
            return False

    def get(self, request, *args, **kwargs):
        provided_token = request.META.get('HTTP_AUTHORIZATION')
        isValidToken = self.validateToken(provided_token)

        if isValidToken:
            userId = isValidToken.id
            userInstance = UserSerializer(instance=isValidToken)
            userData = userInstance.data
            try:
                JobseekerData = JobSeeker.objects.get(userId=userId)
                JobseekerInstance = jobSeekerSerializer(instance=JobseekerData)
                return Response({"Userdata": userData,
                                 "JobseekerData": JobseekerInstance.data}, status=status.HTTP_200_OK)
            except JobSeeker.DoesNotExist:
                return Response({"message": "jobseeker Not Found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)






    def put(self, request, *args, **kwargs):
        provided_token = request.META.get('HTTP_AUTHORIZATION')
        isValidToken = self.validateToken(provided_token)

        if isValidToken:
            userId = isValidToken.id
            user_data = request.data.get('Userdata', {})
            JobseekerData = request.data.get('JobseekerData', {})
            # return Response({"Userdata":reserverInstance.carNo})

            try:
                JobseekerInstance = JobSeeker.objects.get(userId=userId)
                userInstance = UserSerializer(instance=isValidToken, data=user_data, partial=True)
                if userInstance.is_valid():
                    userInstance.save()
                    JobseekerInstance = jobSeekerSerializer(instance=JobseekerInstance, data=JobseekerData, partial=True)
                    if JobseekerInstance.is_valid():
                        JobseekerInstance.save()
                        return Response({"message": "sec"}, status=status.HTTP_200_OK)
                    else:
                        return Response({"message": JobseekerInstance.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"Message": userInstance.errors}, status=status.HTTP_400_BAD_REQUEST)

            except JobSeeker.DoesNotExist:
                return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        provided_token = request.META.get('HTTP_AUTHORIZATION')
        isValidToken = self.validateToken(provided_token)
        if isValidToken:

            try:
                JobseekerInstance = JobSeeker.objects.get(userId=isValidToken.id)
                JobseekerInstance.delete()
                isValidToken.delete()
                return Response({"message": "user deleted successfully"}, status=status.HTTP_200_OK)

            except JobSeeker.DoesNotExist:
                return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)


        else:
            return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)