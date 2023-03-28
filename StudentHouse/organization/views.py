from rest_framework.views import APIView
from rest_framework.response import Response
from StudentHouse.organization.models import *
from django.contrib.auth import get_user_model
from StudentHouse.organization.serializers import *
import datetime



class AdminAddTeacherAPI(APIView):
    def post(self, request, *args, **kwargs):
        try:
            id = request.data.get('id', None)
            teacher_email = request.data.get('email', None)
            print(request.data)
            user = get_user_model().objects.get(id=str(id))
            org = user.institute
            if (org.category == "Institute"):
                if (teacher_email):
                    mwalimu = MwalimuProfile.objects.create(
                        email = teacher_email,
                        register_date = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    )
                    mwalimu.organization.add(org)
                    mwalimu.save()
                    MwalimuProfileSerializer(mwalimu)

                    return Response({"success": "mwalimu email added successful"})
                return Response({"error": "Provide mwalimu email"})
            else:
                return Response({"error": "You have no permission to create teacher profile"})
            
        except Exception as err:
            # maybe email have been already existed.
            # its error look like this ""UNIQUE constraint failed: organization_mwalimuprofile.email""
            return Response({"error": str(err)})
        
        
admin_addteacher = AdminAddTeacherAPI.as_view()


class AddTeacherProfile(APIView):

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email', None)

            user = get_user_model().objects.get(email=email)
            # if user does not exist this .get method bring error
            profile = MwalimuProfile.objects.get(email=email)

            name = request.data.get('full_name', None)
            gender = request.data.get('gender', None)
            mwalimu_wa_darasa = request.data.get('mwalimudarasa', None)
            darasa_id = request.data.get('class_id', None)
            # you should send 'madarasa' in stringified array..
            madarasa = request.data.get('classes', None)
            photo = request.data.get('photo', None)
            
            if (name and gender and mwalimu_wa_darasa and darasa_id and
                json.loads(madarasa).length > 1 and photo != null):
                

                profile.full_name = name
                profile.gender = gender
                profile.ni_mwalimu_wa_darasa = mwalimu_wa_darasa == "true"

                darasa = Darasa.objects.get(id=int(darasa_id))
                profile.darasa_lake = darasa

                for dar in madarasa:
                    kimbweta = Darasa.objects.get(id=int(dar))
                    profile.madarasa_anoyofundisha.add(kimbweta)
                
                # if photo and photo != 'null':
                profile.photo = photo
                
                profile.isComplete = True
                profile.save()
                serialize = MwalimuProfileSerializer(profile)
                return Response(serialize.data)
            else:
                return Response({"error": "Incorrect data sent."})
        except Exception as err:
            return Response({"err": str(err)})
        
teacher_profile = AddTeacherProfile.as_view()