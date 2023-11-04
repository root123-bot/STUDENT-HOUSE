from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .serializers import *
from rest_framework.response import Response
from StudentHouse.organization.models import *
import datetime
from django.urls import reverse
from rest_framework import generics

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

'''
    on sending data to any api don't add the ',' at the
    end of last key value pair, it will bring you an error
    i experienced this.. najua umezoea kufanya hivyo kwenye 
    django in 'Arrays' where you have sth like [1,2,3,]
    but in object/dictionary don't do that on sending data
    this is not allowed 
        { 
            "name": "Paschal Costa",
            "age": 28,    # this comma at last value is not allowed, you will get an error
        }
'''


# {
# "email": "mwali@gmail.com",
# "password": "paschal123",
# "usergroup"
# }     make sure email if registeri Mwalimu should be existed in DB
class CreateUserAPIView(APIView):
    def post(self, request, *args, **kwargs):
        print('request data ', request.data)
        password = request.data.get('password')
        user_group = request.data.get('usergroup')
        print(password, user_group)
        try:
            if password:
                password_hash = make_password(password)
            
                if user_group == "Institute":
                    user = get_user_model().objects.create(email=request.data['email'], password=password_hash)
                    profile = InstituteProfile.objects.create(
                        user=user,
                        register_date=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    )
                    user.save()
                    serializer = RegistrationSerializer(user)
                    profile.save()
                    return Response(serializer.data)
                
                if user_group == "Mwalimu":
                    email = request.data['email']
                    try:
                        if MwalimuProfile.objects.filter(email = email).count() > 0:
                            profile = MwalimuProfile.objects.get(email = email)
                            if profile.is_user_created == False:
                                user = get_user_model().objects.create(email=email, password=password_hash)
                                profile.is_user_created=True
                                user.save()
                                serializer = RegistrationSerializer(user)
                                profile.save()
                                return Response({"success": "User have been created successful"})
                            return Response({"error": "There is a user associated with that email"})
                        return Response({"error": "The email is not added by administrator"})
                    except Exception as err:
                        print('error ', err)
                        return Response({"error ": str(err)})
                
                if user_group == "Parent":
                    user = get_user_model().objects.create(email=request.data['email'], password=password_hash)
                    profile = MzaziProfile.objects.create(user=user)
                    user.save()
                    serializer = RegistrationSerializer(user)
                    profile.save()
                    return Response(serializer.data)
                

            return Response({"error": 'Sorry password field should not be empty'}) # , status=status.HTTP_400_BAD_REQUEST
        
        except Exception as err:
            return Response({'err': str(err)})
    


register = CreateUserAPIView.as_view()


class PasswordReset(generics.GenericAPIView):
    print('IM GET CALLED')
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']
        user = get_user_model().objects.filter(email=email).first()

        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))

            token = PasswordResetTokenGenerator().make_token(user)
            print("IM ABOVE ALL")
            reset_url = reverse(
                "password_reset_confirm", kwargs={'uidb64': encoded_pk, 'token': token}
            )
            print('IM HERE NOW')
            # If we have the domain name we can use it here instead of http://localhost:8000
            reset_url = f"138.197.114.27{reset_url}"

            # then you should send this url to the user via email
            send_mail(
                "Password Reset",
                f'Hi {user.email}, Please use this link to reset your password {reset_url}',
                settings.EMAIL_HOST_USER,
                [user.email],
            )

            return Response({
                "detail": "Password reset link has been sent to your email"
            }, status=status.HTTP_200_OK)
        
        else:
            return Response({
                "detail": "User does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)
        

password_reset = PasswordReset.as_view()