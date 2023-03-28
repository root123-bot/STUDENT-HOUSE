from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .serializers import *
from rest_framework.response import Response
from StudentHouse.organization.models import *
import datetime

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
                        # if there is record created by admin of that teacher email
                        if MwalimuProfile.objects.filter(email = email).count() > 0:
                            # email kama ipo inabidi ucheck tena if that profile is created
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