from rest_framework.views import APIView
from rest_framework.response import Response
from StudentHouse.organization.models import *
from StudentHouse.api.models import *
from StudentHouse.api.serializers import *
from django.contrib.auth import get_user_model
from StudentHouse.organization.serializers import *
import datetime
import json
from rest_framework import status

'''
    Hata kwenye postman unavyosend data haikubali utumie single quotes in any area the same to restful api....
    for example i want to send stringified array which inside it containing the string, lets say i used ..
     {"data": '[{"1": "present"}, {"2": "absent"}]'}
    hii itakataa kusend coz every data you should send by using "" double quotes and ili niifanye my array to
    look like the stringified one i need to enclose it inside the double quotes..NA ISHU INAYOJITOKEZA NI KWAMBA
    YOU CAN'T HAVE THE DUPLICATED DOUBLE QOUTE LIKE THIS 
        >>> "{"data": "[{"1": "present"}, {"2": "absent"}]"}"
    Hichi kitu hakiruhusiwi na ndo maana in last testing of your api when you send the data to the server
    ulikuwa unaget {"detail": "JSON parse error - Expecting value: line 1 column 1 (char 0)"} coz inashindwa kujua
    au ku-convert your data like this of "{"data": "[{"1": "present"}, {"2": "absent"}]"}" to the array...
    so hapa ili kuweza ku-send data of stringified array or objects/dictionary you should not have string
    ... ko kwa mfano hapa nilikua nataka kusend data of stringified array which inside it containing the string like
    this here in to create my subtopic... {1: "present"}, {2: "absent"}] hii ili nii-stringify ni-isend inakuwa ngumu
    coz inakuwa inaonekana hivi ili uistringify '{1: "present"}, {2: "absent"}]' na hii itakataa ku-send/parse coz
    unavyo-send haihitaji wewe kutumia single quotes in any area, na endapo ukisema labda unataka utumie double 
    quotes kama wanavyotaka pia inakuwa syntax error coz you have duplicates of the double quotes in your data
    "{1: "present"}, {2: "absent"}]", na endapo utasema basi nisend kama hivi
    "[{1: present}, {2: absent}]" hii itakataa kusend coz inakuwa inaonekana absent and presents are keywords..
    na hii ndo law on how restful api work if you receive JSON.parse error it means you tried to send single quoted string 
    NA HAPA NDO ERROR IN YOUR INTERFACE OF DJANGO RESTFUL API INAPOTOKEA BUT IF YOU TRIED TO SEND SINGLE QOUTED STRING
    IN POSTMAN ITAKATAA KU-SEND YAANI HAITO-SEND KABISA COZ INA-VALIDATE KABISA... NISHAELEWA HOW THINGS WORKS IN RESTFUL API 
    NA ITAKUWA VIGUMU SANA KUPATA ERROR YA DIZAINI HII.. HII YA 'detail': 'JSON parse error - Expecting value: line 1 column 1 (char 0)'

    Ko kwa hapa coz nataka ni-send status ya mwanafunzi inabidi nii-hardcode in my backend and ni-send integer coz inakuwa 
    rahisi ku-send integer coz ina-ondoa duplicated double quotes ko hapa kwa mfano naweza in my backend nika-hardcode
    status as 
        1 = present
        2 = absent
        3 = late
        4 = excused
        5 = absent with excuse
        6 = absent without excuse
        7 = absent with medical excuse
        8 = absent with medical excuse
    
    Ko endapo mtu atasend data of id of mwanafunzi na number ya status itakuwa rahisi kujua
    yaani "[{28: 8}, {12: 2}]" hii itakataa kusend coz inakuwa inaonekana absent and presents are keywords..
    
    But hii error inatokea if you send data manually like using the RESTful API Interface of Django/Postman coz it have no 
    ability to decode the data containing the string.. but if you have language like Javascript it have JSON.stringify for this
    purpose BUT SIO LANGUAGE ZOTE ZINAHII ABILITY YA KU-INCODE DATA VIZURI FLUTTER NAHISI INAYO ILA KAMA MTU HUIFAHAMU UTAPATA
    TABU SANA KU-SEND DATA LIKE THIS WHICH HAVE STRINGS INSIDE IT NDO ITAKULAZIMU UTUMIE MECHANISM KAMA YANGU HAPO JUU YA
    KU-HARDCODE NUMBER FOR GIVEN VALUE..BUT ALL IN ALL NISHAJUA HII ERROR KWANINI INATOKEA NA HII NI KUTOKANA NA KU-ANGALIA HOW 
    POSTMAN WORK ON SENDING DATA OF ARRAY/OBJECTS CONTAINING THE STRINGS INSIDE IT...
    ALL IN ALL NIMEJUA WHAT'S HAPPENED.. HII ERRO IMEONEKANA KWENYE PROJECT YA THABITI AMBAYO NILIWORK AS BACKEND DEVELOPER..
'''

'''
class FetchOrganizationClasses(APIView):
    def post(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        try:
            organization = get_user_model().objects.get(id=int(user)).institute
            classes = organization.darasa_set.all()
            serializer = DarasaSerializer(classes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({'detail': str(err)}, status=status.HTTP_400_BAD_REQUEST)

org_classes = FetchOrganizationClasses.as_view()

'''

class StudentSubjectResults(APIView):
    def post(self, request, *args, **kwargs):
        student_id = request.data.get('student_id')
        try:
            student = Student.objects.get(id=int(student_id))
            results = student.studentresult.all()
            serializer = SubjectResultSerializer(results, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({'detail': str(err)}, status=status.HTTP_400_BAD_REQUEST)

student_subject_results = StudentSubjectResults.as_view()

class FetchOrgAttendeny(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        try:
            user = get_user_model().objects.get(id=int(user_id))
            organization = user.institute
            # subject have the organization in attendency...
            org_attendencies = []
            attendencies = Attendency.objects.all()
            for attendency in attendencies:
                if attendency.subject.organization.id == organization.id:
                    org_attendencies.append(attendency)

            serializer = AttendancySerializer(org_attendencies, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({'detail': str(err)}, status=status.HTTP_400_BAD_REQUEST)

org_attendencies = FetchOrgAttendeny.as_view()

class CompleteParentProfileAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # what we expect is user_id of the parent, student_metadata(paid one), 
        # relationship, 
        user_id = request.data.get("user_id")
        relation = request.data.get("relation")
        metadata = request.data.get("student_metadata")
        name = request.data.get('name')

        try:
            user = get_user_model().objects.get(id=int(user_id))
            parent = user.mzazi

            parent.relationship = relation
            parent.name = name

            # i have metadata which looks like this { student_id, darasa_id, } i only care about student id sent in that array..
            for dt in json.loads(metadata):
                mwanafunzi = Student.objects.get(id=int(dt["student_id"]))
                parent.student.add(mwanafunzi)

            parent.profile_is_completed = True
            parent.save()   
            return Response({"details": "Profile have been created successful"}, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({"details": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
        
parent_complete_profile = CompleteParentProfileAPIView.as_view()



class ProjectMetadataAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            institutes = InstituteProfile.objects.all()

            serializer = InstituteSerializer(institutes, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as err:
            return Response({'detail': str(err)}, status=status.HTTP_400_BAD_REQUEST)
    

project_metadata = ProjectMetadataAPIView.as_view()

class FetchOrgSubjectResult(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        try:
            user = get_user_model().objects.get(id=int(user_id))
            organization = user.institute
            results = organization.majibu.all()
            serializer = SubjectResultSerializer(results, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({"detail": str(err)}, status=status.HTTP_400_BAD_REQUEST)

org_results = FetchOrgSubjectResult.as_view()

# sasa natak api za ku return assignment na ile ya attendence
class FetchTeacherSubjectResult(APIView):
    def post(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        try:
            user = get_user_model().objects.get(id=int(user))
            mwalimu = MwalimuProfile.objects.get(email=user.email)
            results = mwalimu.results.all()
            serializer = SubjectResultSerializer(results, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({"detail": str(err)}, status=status.HTTP_400_BAD_REQUEST)

mwalimu_subject_results = FetchTeacherSubjectResult.as_view()

class DeleteDeadlinedMatukio(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # to convert datetime to string dt.datetime.strptime("10/2/2023", "%m/%d/%Y") 
            for matukio in Matukio.objects.all():
                if datetime.datetime.strptime(matukio.ending_date, "%d/%m/%Y") < datetime.datetime.now():
                    matukio.delete()
            return Response({"success": "Deadlined matukio deleted successfully"}, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({"detail": str(err)}, status=status.HTTP_400_BAD_REQUEST)

delete_old = DeleteDeadlinedMatukio.as_view()

class DeleteExcuseAPIView(APIView):
    def post(self, request, *args, **kwargs):
        excuse_id = request.data.get("excuse_id")
        try:
            excuse = Excuse.objects.get(id=int(excuse_id))
            excuse.delete()

            return Response({"success": "Excuse deleted successfully"}, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({"detail": str(err)}, status=status.HTTP_400_BAD_REQUEST)

delete_excuse = DeleteExcuseAPIView.as_view()

class FetchTeacherAttendancy(APIView):
    def post(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        try:
            user = get_user_model().objects.get(id=int(user))
            mwalimu = MwalimuProfile.objects.get(email=user.email)
            attendancies = mwalimu.mahundurio.all()
            serializer = AttendancySerializer(attendancies, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"detail": str(err)}, status=status.HTTP_400_BAD_REQUEST)

teacher_attendancy = FetchTeacherAttendancy.as_view()

class FetchOrganizationExcuse(APIView):
    def post(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        try:
            organization = get_user_model().objects.get(id=int(user)).institute
            excuses = organization.ruhusa.all()
            serializer = StudentExcuseSerializer(excuses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({'detail': str(err)}, status=status.HTTP_400_BAD_REQUEST)

org_excuses = FetchOrganizationExcuse.as_view()

class CreateExcuseAPIView(APIView):
    def post(self, request, *args, **kwargs):
        student_id = request.data.get("student_id")
        issued_at = request.data.get("issued_at")
        reason = request.data.get("reason")

        try:
            student = Student.objects.get(id=int(student_id))
            excuse = Excuse.objects.create(
                ruhusayanini = reason,
                issued_at = issued_at,
                organization = student.organization,
            )
            excuse.save()

            student.excuse = excuse
            student.save()

            return Response({"success": "Excuse created successfully"}, status=status.HTTP_200_OK)              
        
        except Exception as err:
            return Response({"detail": str(err)}, status=status.HTTP_400_BAD_REQUEST)

create_excuse = CreateExcuseAPIView.as_view()



class FetchOrgStudentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.data.get('user_id')

        try:
            organization = get_user_model().objects.get(id=int(user)).institute
            students = organization.wanafunzi.all()
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({'detail': str(err)}, status=status.HTTP_400_BAD_REQUEST)

org_students = FetchOrgStudentAPIView.as_view()

class GetMwalimuInfo(APIView):
    def post(self, request, *args, **kwargs):
        user = request.data.get('user_id')

        try:
            current_user = get_user_model().objects.get(id=int(user))
            print('current user ', current_user)
            mwalimu = MwalimuProfile.objects.get(email=current_user.email)
            serializer = MwalimuProfileSerializer(mwalimu)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as err:
            return Response({'detail': str(err)}, status=status.HTTP_400_BAD_REQUEST)

mwalimu_info = GetMwalimuInfo.as_view()

class FetchOrgExamTimeTable(APIView):
    def post(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        try:
            organization = get_user_model().objects.get(id=int(user)).institute
            exams = organization.ratiba_ya_mtihanidarasa.all()
            serializer = ClassExamTimetableSerializer(exams, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({'detail': str(err)}, status=status.HTTP_400_BAD_REQUEST)

org_examtimetable= FetchOrgExamTimeTable.as_view()

class FetchOrgEvents(APIView):
    def post(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        try:
            organization = get_user_model().objects.get(id=int(user)).institute
            events = organization.matukio.all()
            serializer = MatukioSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({'detail': str(err)}, status=status.HTTP_400_BAD_REQUEST)

org_events = FetchOrgEvents.as_view()

# we only fetch alive/active timetable is_finished=False
class FetchOrganizationSchoolExamTimetable(APIView):
    def post(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        try:
            organization = get_user_model().objects.get(id=int(user)).institute
            stimetables = organization.school_timetables.filter(is_finished=False)

            serializer = SchoolExamTimeTableSerializer(stimetables, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as err:
            return Response({'detail': str(err)}, status=status.HTTP_400_BAD_REQUEST)

fetch_org_exam_timetable = FetchOrganizationSchoolExamTimetable.as_view()

# BADO HAIJA-TESTIWA.. even it have no url, hot topic how to serialize list of Queryset using django restful api serializers..
class GetOrganizationClassTimeTableAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        try:
            organization = get_user_model().objects.get(id=int(user)).institute
            timetables = organization.ratibayashule.all()
            serializer = ClassTimeTableSerializer(timetables, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as err:
            return Response({'detail': str(err)}, status=status.HTTP_400_BAD_REQUEST)

org_timetables = GetOrganizationClassTimeTableAPIView.as_view()

# return registered mwalimu => mwalimu, darasa, mikondo anayofundisha, get subjects..
class FetchOrganizationTeachers(APIView):
    def post(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        try:
            organization = get_user_model().objects.get(id=int(user)).institute
            teachers = organization.mkufunzi.all()
            serializer = MwalimuProfileSerializer(teachers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({'detail': str(err)}, status=status.HTTP_400_BAD_REQUEST)

org_teachers = FetchOrganizationTeachers.as_view()

class FetchOrganizationClasses(APIView):
    def post(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        try:
            organization = get_user_model().objects.get(id=int(user)).institute
            classes = organization.darasa_set.all()
            serializer = DarasaSerializer(classes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({'detail': str(err)}, status=status.HTTP_400_BAD_REQUEST)

org_classes = FetchOrganizationClasses.as_view()

class FetchOrganizationSubjects(APIView):
    def post(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        try:
            organization = get_user_model().objects.get(id=int(user)).institute
            subjects = Subject.objects.filter(organization=organization)
            serializer = SubjectSerializer(subjects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({'detail': str(err)}, status=status.HTTP_400_BAD_REQUEST)

org_subjects = FetchOrganizationSubjects.as_view()

class AddSubjectResults(APIView):
    def post(self, request, *args, **kwargs):
        name = request.data.get('name', None) # this will be none if the result added are of "SchoolExam" since it had the name, some u should pass "name" for example normal Test, Quiz, Assigment and so on "Assignment" because they not belong to the school exam 
        somo = request.data.get('subject') # receive the id of the subject
        darasa = request.data.get('class') # receive the id of the class
        mkondo = request.data.get('mkondo', None) # receive the id of the stream, some madarasa they don't have streams
        marked_by = request.data.get('marked_by') # receive the id of the teacher who marked the student
        school_exam = request.data.get('school_exam', None) # receive the id of the school exam, it can be none for small exams, tests, assignments etc schoolexam has "name" that's why we omit above name field sometimes to be "None", this come into play if someone need to add result of assignment and so on... 
        marksmetadata = request.data.get('metadata') # receive the metadata of the student and given score
        totalMarks= request.data.get('total')
        try:
            mm = json.loads(marksmetadata)
            counter = 0
            for metadata in mm:
                mwanafunzi = list(dict.keys(metadata))[0]
                score = list(dict.values(metadata))[0]
                student = Student.objects.get(id=int(mwanafunzi))
                dt = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

                sr = SubjectResult.objects.create(
                    submitted_at = dt,
                    mark = str(score),
                    darasa = Darasa.objects.get(id=int(darasa)),
                    somo = Subject.objects.get(id=int(somo)),
                    student = student,
                    totalMarks = int(totalMarks),
                    marked_by = MwalimuProfile.objects.get(id=int(marked_by)),
                    organization = student.organization
                )
            
                if school_exam:
                    # then we are adding the results of the school exam/big exam
                    se = SchoolExamTimeTable.objects.get(id=school_exam)
                    sr.school_exam = se

                if name:
                    sr.type = name
            
                if mkondo:
                    sr.mkondo = Mkondo.objects.get(id=mkondo)

                sr.save()
                counter += 1

            return Response({
                'success': 'SubjectResults Added Successfully'
            })
        
        except Exception as err:
            return Response({
                "error": str(err),
                "metadata": marksmetadata
            })
        
# hii ndo inayotumika sana..
add_subject_results = AddSubjectResults.as_view()

class CreateAttendacyAPI(APIView):
    def post(self, request, *args, **kwargs):
        day = request.data.get('day') # receive the date in this format 21-2-2020
        darasa = request.data.get('class')  # receive the id of the class 
        mkondo = request.data.get('mkondo', None)  # receive the id of the stream
        subject = request.data.get('subject') # receive the id of the subject
        status = request.data.get('status')  # This is the stringified array containing the 'dictionary' data it looks like [{"1": "present"}, {"2": "absent"}], the id is 
        topic = request.data.get('topic')
        subtopic = request.data.get('subtopic', None)
        user_id = request.data.get('user_id')
        try:
            teacher = MwalimuProfile.objects.get(email=get_user_model().objects.get(id=int(user_id)).email)

            created_student_status = []
            received_status = json.loads(status)
            for status in received_status:
                # https://bobbyhadz.com/blog/python-dict-keys-object-is-not-subscriptable
                # when you get the keys from dictionary in python using dict.keys() or dict.values()
                # the return type is not the array like we used to know in javascript/node js where we
                # have Object.keys() and Object.values().. so you should convert the return type in list/array
                # using list() function in order to access the element of that array like we used to in js...
                # https://bobbyhadz.com/blog/python-dict-keys-object-is-not-subscriptable
                # https://blog.finxter.com/python-typeerror-dict_keys-not-subscriptable-fix-this-stupid-bug/
                # https://stackoverflow.com/questions/26394748/nltk-python-error-typeerror-dict-keys-object-is-not-subscriptable

                student_id = list(dict.keys(status))[0]
                student_status = list(dict.values(status))[0]
                student = Student.objects.get(id=int(student_id))
                student_subject_status = StudentSubjectAttendanceStatus.objects.create(
                    student = student,
                    status = student_status
                )
                student_subject_status.save()
                created_student_status.append(student_subject_status)
            
            subject = Subject.objects.get(id=int(subject))
            darasa = Darasa.objects.get(id=int(darasa))
            # after this we should create the attendance
            attendacy = Attendency.objects.create(
                day = day,
                subject = subject,
                darasa = darasa,
                topic = topic,
                mwitaji = teacher
            )
            if (subtopic):
                attendacy.subtopic = subtopic

            if mkondo:
                mkondo = Mkondo.objects.get(id=int(mkondo))
                attendacy.mkondo = mkondo
            
            if len(created_student_status) > 0:
                '''
                    this is how to add multiple objects to many to many field at once just make
                    sure you pass data to your many to many field as a list of objects
                    for more read this docs... https://docs.djangoproject.com/en/3.0/topics/db/examples/many_to_many/
                    so this .set() keyword helps add to add many objects at once..
                '''
                attendacy.status.set(created_student_status)

            attendacy.save()

            return Response({"success": "attendance created successfully"})     
        except Exception as err:
            # , "detail": status, "metadata": json.loads(status), "objtype": type(json.loads(status))
            return Response({"error": str(err)})

create_attendacy = CreateAttendacyAPI.as_view()


class DisableCompletedSchoolTimeTable(APIView):
    def post(self, request, *args, **kwargs):
        org_id = request.objects.get('org_id')
        organization = InstituteProfile.objects.get(id=int(org_id))
        try:
            school_timetables = SchoolExamTimeTable.objects.filter(organization=organization)
            
            for school_timetable in school_timetables:
                deadline = school_timetable.end_date
                deadline = deadline.timeptime(deadline, "%d-%m-%Y")  # unitumie date in this format..21-2-2020  "as you notice here there is no space.."
                today = datetime.datetime.now()
                if deadline < today:
                    school_timetable.is_finished = True
                    school_timetable.save()
                
            return Response({"success": "school timetable disabled successfully"})

        except Exception as err:
            return Response({"error": err})

disable_school_exam_timetable = DisableCompletedSchoolTimeTable.as_view()

class CreateSchoolExamTimeTable(APIView):
    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        org_id = request.data.get('org_id')
                                                    
        try:
            organization = InstituteProfile.objects.get(id=int(org_id))
            timetable = SchoolExamTimeTable.objects.create(
                name = name,
                start_date = start_date,
                end_date = end_date,
                organization = organization
            )
            timetable.save()
            # serializer = SchoolExamTimeTableSerializer(timetable)
            return Response({"success": "school timetable created successfully"})
        
        except Exception as err:
            return Response({"error": str(err)})
        
create_school_timetable = CreateSchoolExamTimeTable.as_view()

class CreateClassExamTimeTable(APIView):
    def post(self, request, *args, **kwargs):
        date = request.data.get('date')  # pass date.. eg..
        subject = request.data.get('subject')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        darasa = request.data.get('class')
        school_timetable = request.data.get('stimetable')  # this is school class timetable
        try:
            # check if the class exists
            print(darasa, school_timetable, subject, type(darasa), type(school_timetable), type(subject))
            darasa = Darasa.objects.get(id=int(darasa))
            organization = darasa.organization
            school_timetable = SchoolExamTimeTable.objects.get(id=int(school_timetable))
            subject = Subject.objects.get(id=int(subject))
            timetable = ExamTimeTable.objects.create(
                date = date,
                subject = subject,
                start_time = start_time,
                end_time = end_time,
                schoool_timetable = school_timetable,
                darasa = darasa,
                organization = organization
            )
            timetable.save()
            return Response({"success": "class timetable created successfully"})
        
        except Exception as err:
            # print(darasa, school_timetable, subject, type(darasa), type(school_timetable), type(subject))
            return Response({"error": err})


create_class_timetable = CreateClassExamTimeTable.as_view()


# mwalimu wa darasa add student
class AddStudentAPI(APIView):
    def post(self, request, *args, **kwargs):
        full_name = request.data.get('full_name')
        photo = request.data.get('photo', None)
        birth_date = request.data.get('birth_date')
        gender = request.data.get('gender')
        role = request.data.get('role')
        health = request.data.get('health')
        religion = request.data.get('religion')
        nationality = request.data.get('nationality')

        darasa = request.data.get('class')  # pass integer not array b'coz its one realtion..
        mkondo = request.data.get('mkondo', None)  # pass integer not array b'coz its one realtion.. for stream it can be none
        # excuse = request.data.get('excuse', None) # ruhusa tuna-add baadae sana so inabidi isiwepo hapa..
        organization = None

        print(full_name, photo, birth_date, gender, role, darasa, mkondo)

        # if you duplicated the fields and try to add it twice you will get the error especially in amazon especially for 'file' field
        # the error will be Django uploaded file validation leads to "InMemoryUploadedFile is not supported"
        # imeniangaisha nilichokuja kujua ni kwamba nime-duplicate field of 'photo' first i added it to student and the
        # i added it again duh "I don't give the fuck"
        try:
            student = Student.objects.create(
                full_name = full_name,
                birth_date = birth_date,
                gender = gender,
                role = role,
                health = health,
                religion = religion,
                nationality = nationality
            )
            
            if darasa:
                darasa = Darasa.objects.get(id=int(darasa))
                student.darasa = darasa
                organization = darasa.organization
            if mkondo:
                mkondo = Mkondo.objects.get(id=int(mkondo))
                student.mkondo = mkondo
                # if we already set the 'organization' in class no need to deal with that in 'mkondo'
                if organization == None:
                    organization = mkondo.darasa.organization
            
            # there is no way to have nothing organization, if that then we've fatal error in class/mkondo we send...
            # rememeber that so there is no need to set here..
            student.organization = organization
            register_date = datetime.datetime.now().strftime("%Y-%m-%d")
            student.register_date = register_date
            if photo and photo != 'null' and photo != None:
                student.photo = photo
            student.save()
            return Response({"success": "Student created successfully"})
        except Exception as err:
            return Response({"error": str(err)})


add_student = AddStudentAPI.as_view()
            
        

class CompleteMzaziProfile(APIView):
    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        relationship = request.data.get('relationship')
        student = request.data.get('student')  # send student in form of stringified array of students ids since its many to many

        try:
            # check if the student exists
            students = json.loads(student)
            # create the parent
            mzazi = MzaziProfile.objects.create(
                name = name,
                relationship = relationship,
            )
            for student in students:
                student = Student.objects.get(id=int(student))
                mzazi.student.add(student)
            
            mzazi.profile_is_completed = True
            mzazi.save()
            return Response({"success": "Parent created successfully"})
        except Exception as err:
            return Response({"error": str(err)})

complete_mzazi_profile = CompleteMzaziProfile.as_view()

class CreateSubjectAPI(APIView):
    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        user = request.data.get('user_id')
        user = get_user_model().objects.get(id=int(user))

        organization = user.institute
        
        try:
            subject = Subject.objects.create(name=name)
            subject.organization = organization
            subject.save()
            return Response({"success": "Subject created successfully"})
        except Exception as err:
            return Response({"error": str(err)})
        
create_subject = CreateSubjectAPI.as_view()

''' create subjectresult model somo can be null'''
class CreateSubjectResult(APIView):
    def post(self, request, *args, **kwargs):
        type = request.data.get('type')
        submitted_at = request.data.get('submitted_at')
        muhula = request.data.get('muhula')
        somo = request.data.get('somo')
        student = request.data.get('student')
        marked_by = request.data.get('marked_by')
        mark = request.data.get('mark')
        darasa = request.data.get('class')

        try:
            # check if the class exists
            darasa = Darasa.objects.get(id=int(darasa))
            # check if the student exists
            student = Student.objects.get(id=int(student))
            # check if the teacher exists
            marked_by = MwalimuProfile.objects.get(id=int(market_by))
            # check if the subject exists
            if somo:
                somo = Subject.objects.get(id=int(somo))
            # create the result
            result = SubjectResult.objects.create(
                type = type,
                submitted_at = submitted_at,
                muhula = muhula,
                somo = somo,
                student = student,
                market_by = marked_by,
                mark = mark,
                darasa = darasa
            )
            result.save()
            return Response({"success": "Result created successfully"})
        except Exception as err:
            return Response({"error": str(err)})
        
create_subject_result = CreateSubjectResult.as_view()



class EditEventAPIView(APIView):
    def post(self, request, *args, **kwargs):
        event_id = request.data.get('event_id')
        name = request.data.get('name')
        starting_date = request.data.get('starting_date')
        ending_date = request.data.get('ending_date')
        madarasa = request.data.get('class')  # array of ids of madarasa yanayohitajika..... yanaweza yakawa madarasa mengimengi...

        try:
            event = Matukio.objects.get(id=int(event_id))
            event.name = name
            event.starting_date = starting_date
            event.ending_date = ending_date
            event.darasa.clear()
            for darasa in json.loads(madarasa):
                darasa = Darasa.objects.get(id=int(darasa))
                event.darasa.add(darasa)
            event.save()
            return Response({"success": "Event edited successfully"}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
edit_event = EditEventAPIView.as_view()

# create APIView class to create Matukio model
class CreateMatukioAPIView(APIView):
    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        starting_date = request.data.get('starting_date')
        ending_date = request.data.get('ending_date')
        madarasa = request.data.get('class')  # array of ids of madarasa yanayohitajika..... yanaweza yakawa madarasa mengimengi...

        try:
            matukio = Matukio.objects.create(
                name = name,
                starting_date = starting_date,
                ending_date = ending_date,
            )
            organization = None
            for darasa in json.loads(madarasa):
                darasa = Darasa.objects.get(id=int(darasa))
                organization = darasa.organization
                matukio.darasa.add(darasa)

            if(organization):
                matukio.organization = organization
            else:
                return Response({"detail": "Organization not found"}, status=status.HTTP_400_BAD_REQUEST)
            # darasa = Darasa.objects.get(id=int(darasa))
            # matukio.darasa.add(darasa)
            matukio.save()
            return Response({"success": "Matukio created successfully"}, status=status.HTTP_201_CREATED)    
        except Exception as err:
            return Response({"detail": str(err)}, status=status.HTTP_400_BAD_REQUEST)

create_event = CreateMatukioAPIView.as_view()


# create class timetable
class CreateClassTimetable(APIView):
    def post(self, request, *args, **kwargs):
        day = request.data.get('day')
        subject = request.data.get('subject', None)
        time = request.data.get('time')
        darasa = request.data.get('class')
        anaefundisha = request.data.get('anaefundisha')  # nitumie data in form of 'id' na sio stringified 'array'... koz hapa tuna-expect only one data
        mkondo = request.data.get('mkondo', None)

        try:
            # check if the class exists
            darasa = Darasa.objects.get(id=int(darasa))
            # check if the subject exists
            org = darasa.organization
            subject = Subject.objects.get(id=int(subject))
            # check if the teacher exists
            anaefundisha = MwalimuProfile.objects.get(id=int(anaefundisha))
            # check if the stream exists
            # isExisting = ClassTimeTable.objects.filter(day=day, time=time, darasa=darasa, subject.subj)
            if mkondo:
                mkondo = Mkondo.objects.get(id=int(mkondo))
            # create the timetable
            timetable = ClassTimeTable.objects.create(
                day = day,
                time = time,
                subject = subject,
            )

            timetable.mkondo = mkondo if mkondo else None
            timetable.darasa = darasa
            timetable.organization = org
            timetable.anaefundisha.add(anaefundisha)
            timetable.save()
            return Response({"success": "Timetable created successfully"})

        except Exception as err:
            return Response({"error": str(err)})

create_timetable = CreateClassTimetable.as_view()

# institute profile
# {
# "id": 6,
# "phone": "064371890",
#  "country": "Tanzania",
# "region": "Dar",
# "district": "Ilala",
# "type": "Private",
# "regno": "2398289KDLSS89",
# "name": "Institute of finance management",
# "headname": "Mwalimu Mkuu",
# "address": "Shaaban Robert",
# "school_level": "Advance Level"
# }
class InstituteProfileAPI(APIView):
    # create institute profile
    def post(self, request, *args, **kwargs):
        id = request.data.get('id')
        phone = request.data.get('phone')
        country = request.data.get('country')
        region = request.data.get('region')
        district = request.data.get('district')
        type = request.data.get('type')
        regno = request.data.get('regno')
        name = request.data.get('name')
        web = request.data.get('web', None)
        headname = request.data.get('headname')
        ceo = request.data.get('ceo', None)
        address = request.data.get('address')
        opentime = request.data.get('opentime', None)
        school_level = request.data.get('school_level')
        logo = request.data.get('logo', None)
        try:
            user = get_user_model().objects.get(id=int(id))
            if hasattr(user, 'institute'):
                profile = user.institute
                if phone and country and region and district and type and name and headname and address and school_level:
                    profile.phone = phone
                    profile.country = country
                    profile.region = region
                    profile.district = district
                    profile.type = type
                    # profile.regno = regno
                    profile.name = name
                    if regno:
                        profile.regno = regno
                    if web:
                        profile.web = web
                    profile.headname = headname
                    if ceo:
                        profile.ceo = ceo
                    profile.address = address
                    if opentime:
                        profile.opentime = opentime

                    profile.school_level = school_level
                    if logo:
                        profile.logo = logo
                    
                    profile.isComplete = True

                    # IF YOU COMPLETE THE PROFILE LETS GIVE YOU FREE 3 MONTH PAYMENT
                    payment = PaymentRecord.objects.create(
                        start_date = datetime.datetime.now(),
                        end_date = datetime.datetime.now() + datetime.timedelta(days=500),
                        mode = 'FREE',
                        user = user
                    )

                    payment.save()

                    profile.save()
                    return Response({"success": "Profile updated successfully"})
                else:
                    return Response({"error": "Please fill all the required fields"})
            else:
                return Response({"err": "User does not have an institute profile"})
        except Exception as err:
            return Response({"error": str(err)})

complete_institute_profile = InstituteProfileAPI.as_view()

# create add Mkondo API
class MkondoAPI(APIView):
    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        try:
            Mkondo.objects.create(
                stream_name = name
            )
            return Response({"success": "Mkondo created successfully"})
        except Exception as err:
            return Response({"error": str(err)})

create_mkondo = MkondoAPI.as_view()

class AddClassAPI(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('id')
        name = request.data.get('name')
        mkondo = request.data.get('mkondo', None)   # should be a name not id coz in most case mkonod... in this case, we'll receive names of mikondo like ['a', 'b', 'c']
        subjects = request.data.get('subjects', None) # should be a list of subjects id, stringified
        students = request.data.get('students', None) # should be a list of students id, stringified
        '''
            # "['a', 'b']" hii inakataa kuconvert in array using json.loads.. , '["a", "b"]' hii inakubali
            # hii ni sheria kuwa endapo una string inside array INABID ZIWE IN DOUBLE QUOTES THEN ARRAY ILI IWE
            # STRINGIFIED ARRAY INSTEAD OF STRING INABIDI IWE IMEZINGIRWA NA SINGLE QUOTES '[]' JSON.loads() ndo inayo-ielewa..
            #
            #
            # array of string of string.... single quotes inabidi
        '''
        institute = get_user_model().objects.get(id=int(user_id)).institute

        try:
            darasa = Darasa.objects.create(
                name = name
            )
            darasa.organization = institute
            if mkondo:
                mikondo = json.loads(mkondo)
                for stream in mikondo:
                    stream = Mkondo.objects.create(stream_name=str(stream))
                    stream.darasa = darasa
                    stream.save()
                    
            if subjects:

                masomo = json.loads(subjects)
                for subject in masomo:
                    subject = Subject.objects.get(id=int(subject))
                    darasa.subjects.add(subject)
                    
            if students:
                for student in json.loads(students):
                    student = Student.objects.get(id=int(student))
                    # darasa.save()
                    darasa.students.add(student)
            
            darasa.save()
            serialize = DarasaSerializer(darasa)
            return Response(serialize.data)
        
        except Exception as err:
            return Response({"error": str(err)})


add_class = AddClassAPI.as_view()

# '''
# {
# "id": 6,
# "email": "mwali@gmail.com",
# "name": "mwamba",
# "mwalimuwadarasa": "true",
# "phone": "0634489239",
# "myclass": 1,
# "gender": "female",
# "madarasa": "[1, 2]"
# }
# '''
class FetchOrganizationTeacher(APIView):
    def post(self, request, *args, **kwargs):
        id = request.data.get('id', None)
        user = get_user_model().objects.get(id=int(id))
        org = user.institute
        




class AdminAddTeacherAPI(APIView):
    def post(self, request, *args, **kwargs):
        try:
            id = request.data.get('id', None) # id of organization...
            teacher_email = request.data.get('email', None)
            full_name = request.data['name']
            ni_mwalimu_wa_darasa = request.data.get('mwalimuwadarasa', None)
            phone_no = request.data['phone']
            darasa_lake = request.data.get('myclass', None)
            gender = request.data['gender']
            madarasa_anayofundisha = request.data.get('madarasa', None) # array stringified..
            mkondo = request.data.get('mkondo', None) # ids of mikondo to add coz its manytomany field
            user = get_user_model().objects.get(id=int(id))
            org = user.institute


            if (org.category == "Institute"):
                if (teacher_email):
                    mwalimu = MwalimuProfile.objects.create(
                        email = teacher_email,
                        register_date = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                        full_name = full_name,
                        phone = phone_no,
                        gender = gender,
                    )
                    if ni_mwalimu_wa_darasa == "true":
                        mwalimu.ni_mwalimu_wa_darasa = True
                        # then ni mwalimu wa darasa
                        darasa = Darasa.objects.get(id=int(darasa_lake))
                        mwalimu.darasa_lake = darasa

                    mwalimu.organization.add(org)

                    # if mkondo is provided just add it to our mwalimu
                    if mkondo:
                        mikondo = json.loads(mkondo)
                        for mkondo in mikondo:
                            mkondo = Mkondo.objects.get(id=int(mkondo))
                            mwalimu.mikondo.add(mkondo)


                    # just add the madarasa anayofundisha..
                    if madarasa_anayofundisha:
                        madarasa = json.loads(madarasa_anayofundisha)
                        for darasa in madarasa:
                            darasa = Darasa.objects.get(id=int(darasa))
                            mwalimu.madarasa_anoyofundisha.add(darasa)

                    mwalimu.save()

                    MwalimuProfileSerializer(mwalimu)

                    return Response({"success": "mwalimu email added successful"})
                return Response({"error": "Provide mwalimu email"})
            else:
                return Response({"error": "You have no permission to create teacher profile"})
            
        except Exception as err:
            return Response({"error": str(err)})
        
        
admin_addteacher = AdminAddTeacherAPI.as_view()


# {"email": "teacher@test.com"} make sure you updated server after saving, also see on how to send 'image' via http.. like we did this in react..
class AddTeacherProfile(APIView):
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email', None)
            user = get_user_model().objects.get(email=email)
            # if user does not exist this .get method bring error
            profile = MwalimuProfile.objects.get(email=email)

            photo = request.data.get('photo', None)
            # if photo and photo != 'null':
            profile.photo = photo
            
            profile.isComplete = True
            profile.save()
            serialize = MwalimuProfileSerializer(profile)
            return Response(serialize.data)
        except Exception as err:
            return Response({"err": str(err)})
        
teacher_profile = AddTeacherProfile.as_view()

class EditSubject(APIView):
    def post(self, request, *args, **kwargs):
        try:
            id = request.data.get('id', None)
            name = request.data.get('name', None)
            subject = Subject.objects.get(id=int(id))
            subject.name = name
            subject.save()
            serialize = SubjectSerializer(subject)
            return Response(serialize.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
edit_subject = EditSubject.as_view()

# add mkondo,
class AddMkondo(APIView):
    def post(self, request, *args, **kwargs):
        try:
            class_id = request.data.get('class_id', None)
            darasa = Darasa.objects.get(id=int(class_id))
            name = request.data.get('name', None)
            mkondo = Mkondo.objects.create(
                stream_name = name,
                darasa = darasa
            )
            serialize = MkondoSerializer(mkondo)
            return Response(serialize.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
add_mkondo = AddMkondo.as_view()

# edit mkondo,
class EditMkondo(APIView):
    def post(self, request, *args, **kwargs):
        try:
            id = request.data.get('id', None)
            name = request.data.get('name', None)
            mkondo = Mkondo.objects.get(id=int(id))
            mkondo.stream_name = name
            mkondo.save()
            serialize = MkondoSerializer(mkondo)
            return Response(serialize.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

edit_mkondo = EditMkondo.as_view()

# delete mkondo
class DeleteMkondo(APIView):
    def post(self, request, *args, **kwargs):
        try:
            id = request.data.get('id', None)
            mkondo = Mkondo.objects.get(id=int(id))
            mkondo.delete()
            return Response({"success": "mkondo deleted successful"}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

delete_mkondo = DeleteMkondo.as_view()

class EditOrganizationView(APIView):
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        country = request.data.get('country')
        region = request.data.get('region')
        district = request.data.get('district')
        type = request.data.get('type')
        regno = request.data.get('regno')
        name = request.data.get('name')
        web = request.data.get('web', None)
        headname = request.data.get('headname')
        ceo = request.data.get('ceo', None)
        address = request.data.get('address')
        opentime = request.data.get('opentime', None)
        school_level = request.data.get('school_level')
        logo = request.data.get('logo', None)
        orgid = request.data.get('orgid', None)

        try:
            org = InstituteProfile.objects.get(id=int(orgid))
            org.phone = phone
            org.country = country
            org.region = region
            org.district = district
            org.type = type
            org.regno = regno
            org.name = name
            org.web = web
            org.headname = headname
            org.ceo = ceo
            org.address = address
            org.opentime = opentime
            org.school_level = school_level
            org.logo = logo
            org.save()

            serialize = OrganizationSerializer(org)
            return Response(serialize.data, status=status.HTTP_200_OK)
    
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
edit_organization = EditOrganizationView.as_view()

class EditDarasa(APIView):
    def post(self, request, *args, **kwargs):
        try:
            id = request.data.get('id', None)
            name = request.data.get('name', None)
            darasa = Darasa.objects.get(id=int(id))
            if name:
                darasa.name = name
            darasa.save()
 
            serialize = DarasaSerializer(darasa)
            return Response(serialize.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

edit_darasa = EditDarasa.as_view()

class EditMwalimu(APIView):
    def post(self, request):
        mwalimu_id = request.data.get('mwalimu_id', None)
        name = request.data.get('name', None)
        phone = request.data.get('phone', None)
        gender = request.data.get('gender', None)
        is_class_teacher = request.data.get('is_class_teacher', None)
        darasa_lake = request.data.get('darasa_lake', None)
        photo = request.data.get('photo', None)
        mwalimu = MwalimuProfile.objects.get(id=int(mwalimu_id))
        madarasa_anayofundisha = request.data.get('madarasa_anayofundisha', None)
        mkondo = request.data.get('mkondo', None)

        try:
            mwalimu.full_name = name
            mwalimu.phone = phone
            mwalimu.gender = gender
            mwalimu.ni_mwalimu_wa_darasa = is_class_teacher

            if (is_class_teacher == "True") and darasa_lake:
                darasa = Darasa.objects.get(id=int(darasa_lake))
                mwalimu.darasa_lake = darasa

            if photo and photo != 'null':
                mwalimu.photo = photo

            # if mkondo is provided just add it to our mwalimu
            # lets first clear all mikondo
            if mkondo:
                mwalimu.mikondo.clear()
                mikondo = json.loads(mkondo)
                for mkondo in mikondo:
                    mkondo = Mkondo.objects.get(id=int(mkondo))
                    mwalimu.mikondo.add(mkondo)


            # just add the madarasa anayofundisha..
            # lets first clear all classes
            if madarasa_anayofundisha:
                mwalimu.madarasa_anoyofundisha.clear()
                madarasa = json.loads(madarasa_anayofundisha)
                for darasa in madarasa:
                    venue = Darasa.objects.get(id=int(darasa))
                    mwalimu.madarasa_anoyofundisha.add(venue)


            mwalimu.save()
            serialize = MwalimuProfileSerializer(mwalimu)
            return Response(serialize.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

edit_mwalimu = EditMwalimu.as_view()

class EditClassTimeTable(APIView):
    def post(self, request):
        timetable_id = request.data.get('timetable_id', None)
        day = request.data.get('day', None)
        subject = request.data.get('subject', None)
        time = request.data.get('time', None)
        mkondo = request.data.get('mkondo', None)
        darasa = request.data.get('darasa', None)
        mwalimu = request.data.get('mwalimu', None)
        timetable = ClassTimeTable.objects.get(id=int(timetable_id))

        try:
            timetable.day = day
            timetable.subject = Subject.objects.get(id=int(subject))
            timetable.time = time
            timetable.darasa = Darasa.objects.get(id=int(darasa))
            # check if added darasa have mkondo kama halina mkondo basi futa mkondo
            # check if darasa have mkondo...
            if mkondo and timetable.darasa.mkondo.all().count() > 0:
                timetable.mkondo = Mkondo.objects.get(id=int(mkondo))
            elif timetable.darasa.mkondo.all().count() == 0:
                timetable.mkondo = None
            # if not timetable.darasa.mkondo:
            #     timetable.mkondo = None
            timetable.anaefundisha.clear()
            timetable.anaefundisha.add(MwalimuProfile.objects.get(id=int(mwalimu)))
            timetable.save()
            serialize = ClassTimeTableSerializer(timetable)
            return Response(serialize.data, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

edit_class_timetable = EditClassTimeTable.as_view()

class EditSchoolExamTimeTable(APIView):
    def post(self, request):
        stimetable = request.data.get('stimetable', None)
        name = request.data.get('name')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        try:
            timetable = SchoolExamTimeTable.objects.get(id=int(stimetable))
            timetable.name = name
            timetable.start_date = start_date
            timetable.end_date = end_date
            timetable.save()
            serialize = SchoolExamTimeTableSerializer(timetable)
            return Response(serialize.data, status=status.HTTP_200_OK)

        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)   

edit_school_exam_timetable = EditSchoolExamTimeTable.as_view()

class EditClassExamTimetable(APIView):
    def post(self, request):
        date = request.data.get('date')  # pass date.. eg..
        subject = request.data.get('subject')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        darasa = request.data.get('class')
        school_timetable = request.data.get('stimetable')
        exam_timetable = request.data.get('exam_timetable')

        try:
            timetable = ExamTimeTable.objects.get(id=int(exam_timetable))
            timetable.date = date
            timetable.subject = Subject.objects.get(id=int(subject))
            timetable.start_time = start_time
            timetable.end_time = end_time
            timetable.darasa = Darasa.objects.get(id=int(darasa))
            timetable.school_timetable = SchoolExamTimeTable.objects.get(id=int(school_timetable))
            timetable.save()
            return Response({"message" :"edited successful"}, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
edit_class_exam_timetable = EditClassExamTimetable.as_view()


class EditExcuse(APIView):
    def post(self, request):
        excuse_id = request.data.get('excuse_id', None)
        reason = request.data.get('reason', None)
        issued_at = request.data.get('issued_at', None)

        try:
            excuse = Excuse.objects.get(id=int(excuse_id))
            excuse.ruhusayanini = reason
            excuse.issued_at = issued_at
            excuse.save()
            return Response({"message": "Edited successful"}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
edit_excuse = EditExcuse.as_view()

class EditStudent(APIView):
    def post(self, request):
        full_name = request.data.get('full_name')
        photo = request.data.get('photo', None)
        birth_date = request.data.get('birth_date')
        gender = request.data.get('gender')
        role = request.data.get('role')
        health = request.data.get('health')
        religion = request.data.get('religion')
        nationality = request.data.get('nationality')
        darasa = request.data.get('class')  
        mkondo = request.data.get('mkondo', None)  
        student_id = request.data.get('student_id', None)

        try:
            student = Student.objects.get(id=int(student_id))
            student.full_name = full_name
            student.birth_date = birth_date
            student.gender = gender
            student.role = role
            student.health = health
            student.religion = religion
            student.nationality = nationality
            student.darasa = Darasa.objects.get(id=int(darasa))
            if mkondo:
                student.mkondo = Mkondo.objects.get(id=int(mkondo))
            else:
                student.mkondo = None
            if photo and photo != 'null' and photo != None:
                student.photo = photo
            student.save()
            serialize = StudentSerializer(student)
            return Response(serialize.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

edit_student = EditStudent.as_view()

class EditAttendancyAPIView(APIView):
    # day mkondo darasa
    def post(self, request):
        day = request.data.get('day') # receive the date in this format 21-2-2020
        darasa = request.data.get('class')  # receive the id of the class 
        mkondo = request.data.get('mkondo', None)  # receive the id of the stream
        subject = request.data.get('subject') # receive the id of the subject
        student_status = request.data.get('status')  # This is the stringified array containing the 'dictionary' data it looks like [{"1": "present"}, {"2": "absent"}], the id is 
        topic = request.data.get('topic')
        subtopic = request.data.get('subtopic', None)
        attendancy_id = request.data.get('attendancy_id', None)

        try:
            attendancy = Attendency.objects.get(id=int(attendancy_id))
            attendancy.day = day
            attendancy.darasa = Darasa.objects.get(id=int(darasa))
            if mkondo:
                attendancy.mkondo = Mkondo.objects.get(id=int(mkondo))
            else:
                attendancy.mkondo = None
            attendancy.subject = Subject.objects.get(id=int(subject))
            attendancy.topic = topic
            attendancy.subtopic = subtopic

            # status should look like {student_id, status, statusObjectId}
            received_status = json.loads(student_status)
            for sstatus in received_status:
                student_id = sstatus['student_id']
                student_status = sstatus['status']
                status_id = sstatus['statusObjectId']
                statusObj = StudentSubjectAttendanceStatus.objects.get(id=int(status_id))
                student = Student.objects.get(id=int(student_id))
                statusObj.student = student
                statusObj.status = student_status
                statusObj.save()

            attendancy.save()
            serialize = AttendancySerializer(attendancy)
            return Response(serialize.data, status=status.HTTP_200_OK)

        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

edit_attendancy = EditAttendancyAPIView.as_view()

class EditSubjectResult(APIView):
    def post(self, request):
        name = request.data.get('name', None) # this will be none if the result added are of "SchoolExam" since it had the name, some u should pass "name" for example normal Test, Quiz, Assigment and so on "Assignment" because they not belong to the school exam 
        somo = request.data.get('subject') # receive the id of the subject
        darasa = request.data.get('class') # receive the id of the class
        mkondo = request.data.get('mkondo', None) # receive the id of the stream, some madarasa they don't have streams
        marked_by = request.data.get('marked_by') # receive the id of the teacher who marked the student
        school_exam = request.data.get('school_exam', None) # receive the id of the school exam, it can be none for small exams, tests, assignments etc schoolexam has "name" that's why we omit above name field sometimes to be "None", this come into play if someone need to add result of assignment and so on... 
        mark = request.data.get("mark")
        totalMarks= request.data.get('total')
        result_id = request.data.get('result_id', None)

        try:
            result = SubjectResult.objects.get(id=int(result_id))
            result.somo = Subject.objects.get(id=int(somo))
            result.darasa = Darasa.objects.get(id=int(darasa))
            result.mark = mark
            if mkondo:
                result.mkondo = Mkondo.objects.get(id=int(mkondo))
            else:
                result.mkondo = None
            result.marked_by = MwalimuProfile.objects.get(id=int(marked_by))
            if school_exam:
                result.school_exam = SchoolExamTimeTable.objects.get(id=int(school_exam))
            else:
                result.school_exam = None

            if name:
                result.type = name
            result.totalMarks = totalMarks
            result.save()

            serialize = SubjectResultSerializer(result)
            return Response(serialize.data, status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

edit_subject_result = EditSubjectResult.as_view()