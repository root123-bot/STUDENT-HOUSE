from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from StudentHouse.organization.models import *
from rest_framework.response import Response
from StudentHouse.organization.serializers import *

# Create your views here.
class UserDetails(APIView):
    def post(self, request, *args, **kwargs):
        id = request.data['id']
        user = get_user_model().objects.get(id=id)

        # for organization, mzazi its the same for teacher it to check if the email  exist in anymodel of teacher..
        teacher = MwalimuProfile.objects.filter(email=user.email)
        if teacher.count() > 0:
            # the user is teacher
            serializer = MwalimuProfileSerializer(teacher)
            return Response(serializer.data)

        elif hasattr(user, 'institute'):
            profile = user.institute
            serializer = OrganizationSerializer(profile)
            return Response(serializer.data)
        
        elif hasattr(user, 'mzazi'):
            profile = user.mzazi
            serializer = MzaziSerializer(profile)
            return Response(serializer.data)
        
        else:
            return Response({"error": "Unexpected error occurred"})

user_details = UserDetails.as_view()