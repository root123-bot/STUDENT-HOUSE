from django.db import models
from django.contrib.auth import get_user_model
import json

# Unavyo-send class kwenye frontend ninavyoadd in DB inabidi iwe hivi, HARDCODED
CLASSES = [
    "STD I",
    "STD II",
    "STD III",
    "STD IV",
    "STD V",
    "STD VI",
    "STD VII",
    "FORM I"
    "FORM II"
    "FORM III"
    "FORM IV"
    "FORM V"
    "FORM VI"
]


# Create your models here.
class InstituteProfile(models.Model):
    user = models.OneToOneField(get_user_model(), unique=True, on_delete=models.CASCADE, related_name="institute")
    phone = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=500, blank=True, null=True)
    region = models.CharField(max_length=500, blank=True, null=True)
    district = models.CharField(max_length=500, blank=True, null=True)
    type = models.CharField(max_length=500, blank=True, null=True) # pub/gov
    regno = models.CharField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=500, blank=True, null=True) 
    web = models.CharField(max_length=500, blank=True, null=True)
    headname = models.CharField(max_length=500, blank=True, null=True)
    ceo = models.CharField(max_length=500, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    opentime = models.CharField(max_length=500, blank=True, null=True)
    category = models.CharField(max_length=500, default="Institute")
    isComplete = models.BooleanField(default=False)
    school_level = models.CharField(max_length=50, blank=True, null=True)
    register_date = models.CharField(max_length=50, blank=True, null=True)
    logo = models.ImageField(upload_to="images/", blank=True, null=True)

    def __str__(self):
        return self.user.email + ' => ' + ' Institute' + ' => ' + str(self.id)
    
    @property
    def get_logo(self):
        if self.logo:
            return self.logo.url
        return None
    
    
    @property
    def organization_metadata(self):
        return {
            "id": self.id,
            "phone": self.phone,
            "country": self.country,
            "region": self.region,
            "district": self.district,
            "type": self.type,
            "regno": self.regno,
            "name": self.name,
            "web": self.web,
            "headname": self.headname,
            "ceo": self.ceo,
            "address": self.address,
            "opentime": self.opentime,
            "category": self.category,
            "isComplete": self.isComplete,
            "school_level": self.school_level,
            "register_date": self.register_date,
            
        }
    

    @property
    def org_classes(self):
        madarasa = []
        for darasa in self.darasa_set.all():
            obj = {
                "id": darasa.id,
                "name": darasa.name,
            }
            madarasa.append(obj)

        return madarasa


    @property
    def org_mikondo(self):
        madarasa = []
        mikondo = []
        for darasa in self.darasa_set.all():
            madarasa.append(darasa.id)
        if len(madarasa) > 0:
            for darasa_id in madarasa:
                darasa = Darasa.objects.get(id=int(darasa_id))
                for mkondo in darasa.mkondo.all():
                    obj = {
                        "id": mkondo.id,
                        "name": mkondo.stream_name,
                        "darasa_id": mkondo.darasa.id,
                    }

                    mikondo.append(obj)
        return mikondo
        

    
    @property
    def org_students(self):
        wanafunzi = self.wanafunzi.all()
        students = []
        for mwanafunzi in wanafunzi:
            obj = {
                "id": mwanafunzi.id,
                "full_name": mwanafunzi.full_name,
                "gender": mwanafunzi.gender,
                "mkondo": mwanafunzi.mkondo.stream_name if mwanafunzi.mkondo else None,
                "mkondo_id": mwanafunzi.mkondo.id if mwanafunzi.mkondo else None,
                "darasa": mwanafunzi.darasa.name if mwanafunzi.darasa else None,
                "darasa_id": mwanafunzi.darasa.id if mwanafunzi.darasa else None,
                "photo": mwanafunzi.photo.url if mwanafunzi.photo else None,
            }
            students.append(obj)
        
        return students
    






class Subject(models.Model):
    name = models.CharField(max_length=500)
    organization = models.ForeignKey(InstituteProfile, on_delete=models.CASCADE, null=True, blank=True)
    

# ina-bidi a-add mwalimu wa darasa.. haina relation na any model ni just kumsaidia mwalimu anavyoita attendancy
# hii ita-sync na attendacy kabila mwalimu hajaita ita-sync.... excuse tuta-refer ya attendancy na excuse
# wanafunzi wengi ruhusa moja... one to many... ku-sync nafanya in backend sindo naupdate DB..
class Excuse(models.Model):
    ruhusayanini = models.CharField(max_length=8000)
    # isstill = models.BooleanField(default=True) # ko atakapo-rudi inabidi aripoti kwa mwalimu wa darasa ili delete
    issued_at = models.CharField(max_length=50)
    # student tushalink kule chini so haina haja ya kuweka student wala darasa...
    organization = models.ForeignKey(InstituteProfile, related_name="ruhusa", on_delete=models.CASCADE, null=True, blank=True)


    @property
    def get_student(self):
        students = []
        if self.student.all():
            for student in self.student.all():
                students.append({f"{student.id}": f"{student.full_name}"})
            return students
        return None

# sync, kila mwaka unavyoisha admin/organization inabidi a-sync manually madarasa coz atujui ni lini
# ko-aki-click 'syc' to new year maanke wanafunzi madarasa yao ina-bidi yahame ya increment by one from 
#  the list of CLASSES above.. ko hii ina-change in students..
class Student(models.Model):
    full_name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="images/", blank=True, null=True)
    birth_date = models.CharField(max_length=500)
    gender = models.CharField(max_length=50)
    role = models.CharField(max_length=500) # either monitor, headbox etc
    # inakuepo mtu anavyo-add ruhusa... ndo hii field inakuepo..
    excuse = models.ForeignKey(Excuse, on_delete=models.SET_NULL, null=True, blank=True, related_name="student")
    register_date = models.CharField(max_length=50)
    mkondo = models.ForeignKey("Mkondo", on_delete=models.CASCADE, null=True, blank=True)
    darasa = models.ForeignKey("Darasa", on_delete=models.CASCADE, null=True, blank=True)
    organization = models.ForeignKey(InstituteProfile, related_name="wanafunzi", on_delete=models.CASCADE, null=True, blank=True)
    health = models.CharField(max_length=500, null=True, blank=True)
    religion = models.CharField(max_length=500, null=True, blank=True)
    nationality = models.CharField(max_length=500, null=True, blank=True)


    @property
    def get_photo(self):
        if (self.photo):
            return self.photo.url
        return None
    
    @property
    def get_darasa(self):
        if (self.darasa):
            return {f"{self.darasa.id}": f"{self.darasa.name}"}
        return None
    
    @property
    def get_mkondo(self):
        if (self.mkondo):
            return {f"{self.mkondo.id}": f"{self.mkondo.stream_name}"}
        return None

# validation in your apis, to check to check if the teacher ni mwalimu wa darasa husika asi-add mwanafunzi kama sio mwalimu wa darasa
class Darasa(models.Model):
    name = models.CharField(max_length=400)
    subjects = models.ManyToManyField(Subject, blank=True)
    # students = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    # organization = models.ForeignKey(InstituteProfile, related_name="events", on_delete=models.CASCADE, null=True, blank=True)
    organization = models.ForeignKey(InstituteProfile, on_delete=models.CASCADE, null=True, blank=True)


    @property
    def get_mikondo(self):
        streams = []
        for stream in self.mkondo.all():
            stream_metadata = {f"{stream.id}": f"{stream.stream_name}"}
            # last time tulikuwa tuna-return/append "stream.stream_name"
            streams.append(stream_metadata)

        return streams
    
    @property
    def get_students(self):
        students = []
        for student in self.student_set.all():

            students.append({
                "id": student.id,
                "name": student.full_name
                })

        return students

    @property
    def get_subjects(self):
        subjects = []
        for subject in self.subjects.all():
            subject_metadata = {f"{subject.id}": f"{subject.name}"}
            # last time tulikuwa tuna-append subject.name
            subjects.append(subject_metadata)

        return subjects


    # mwalimu wa darasa sio lazima afundishe shule ko kutambua mwalimu wa darasa hatuwezi tuka-consider wale wafundishaji 
    # kupitia .mfundishaji().... ko hii ni property nyingine ya nje inabidi iwe hivyo... Ko kwa hapa sisi kwenye mwalimu metadata
    # tutaishia ku-return madarasa anayofundisha na mikondo anayofundisha hivyo tu...inabidi tuwe na property nyingine ya ku-detect 
    # mwalimu wa darasa...
    @property
    def get_mwalimu_wa_darasa(self):
        mwalimu_wa_darasa = {}
        walimu = self.mwalimu.all()
        for mwalimu in walimu:
            if mwalimu.ni_mwalimu_wa_darasa:
                # then detect which darasa ni mwalimu wa darasa..
                if mwalimu.darasa_lake.id == self.id:
                    mwalimu_wa_darasa = {
                        "id": mwalimu.id,
                        "name": mwalimu.full_name
                    }

                    break
            
        return mwalimu_wa_darasa

    @property
    def get_walimu(self):
        teachers = []
        print('walimu ', self.mwalimu.all())  # in relation to mwalimu wa darasa.. mtu anaweza akawa mwalimu wa darasa ila asifundishe...

        print('walimu wanaofundisha hilo darasa ', self.mfundishaji.all())

        for mwalimu in self.mfundishaji.all():
            madarasa_anayofundisha_mwalimu = []
            mikondo_anayofundisha_mwalimu = []
            madarasa = mwalimu.madarasa_anoyofundisha.all()
            
            for darasa in madarasa:
                madarasa_anayofundisha_mwalimu.append(
                    {
                        "darasa_id": darasa.id,
                        "name": darasa.name
                    }
                )
            
            
            streams = mwalimu.mikondo.all()
            for mkondo in streams:
                mikondo_anayofundisha_mwalimu.append({
                    "mkondo_id": mkondo.id,
                    "mkondo_name": mkondo.stream_name
                })

            print('madarasa anayofundisha ', madarasa_anayofundisha_mwalimu,
                  "mikondo_anayofundisha", mikondo_anayofundisha_mwalimu,
                  )
            
            teachers.append({
                "id": mwalimu.id,
                "name": mwalimu.full_name,
                "madarasa_anayofundisha": madarasa_anayofundisha_mwalimu,
                "mikondo_anayofundisha": mikondo_anayofundisha_mwalimu
            })
        
        '''
            # print('amepita ', madarasa_anayofundisha_mwalimu)
            # mikondo anayofundisha...

            # metadata ya mwalimu format yake ni 
            # { "madarasa_anayofundisha", "mikondo_anayofundisha", "ni_mwalimu_wa_darasa", "darasa_lake" }
            # mikondo_anayofundisha_mwalimu = []
            # for mwalimu in self.mfundishaji.all():
            #     streams = mwalimu.mikondo.all()

            #     for mkondo in streams:
            #         mikondo_anayofundisha_mwalimu.append({
            #             "mkondo_id": mkondo.id,
            #             "mkondo_name": mkondo.stream_name
            #         })

            # print('mikondo ', mikondo_anayofundisha_mwalimu)


            # for teacher in self.mwalimu.all():
            #     if teacher.ni_mwalimu_wa_darasa:
            #         teachers.append({
            #             "id": teacher.id, 
            #             "name": teacher.full_name,
            #             "ni_mwalimu_wa_darasa": True, 
            #             "darasa_lake": teacher.darasa_lake.name, 
            #             "darasa_lake_id": teacher.darasa_lake.id,
            #             "madarasa_anayofundisha": madarasa_anayofundisha_mwalimu,
            #             "mikondo_anayofundisha": mikondo_anayofundisha_mwalimu
            #         })
                
            #     else:
            #         teachers.append({
            #             "id": teacher.id,
            #             "name": teacher.full_name,
            #             "ni_mwalimu_wa_darasa": False,
            #             "madarasa_anayofundisha": madarasa_anayofundisha_mwalimu,
            #             "mikondo_anayofundisha": mikondo_anayofundisha_mwalimu
            #         })
        '''

        return teachers

class Mkondo(models.Model):
    stream_name = models.CharField(max_length=400)
    darasa = models.ForeignKey(Darasa, related_name="mkondo", on_delete=models.CASCADE, blank=True, null=True)

# status iwe ni model 
class StudentSubjectAttendanceStatus(models.Model):
    status = models.CharField(max_length=50) # yupo, ana-ruhusa, hayupo, amechelewa, good-behaviour, bad-behaviour
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

# kila mwalimu anavyo-ingia darasani inabidi aite attendancy..... kwa siku zinaweza zikaitwa attendancy 10..
class Attendency(models.Model):
    day = models.CharField(max_length=50)  # tarehe ya siku hiyo kwa mfano 2020-12-12
    darasa = models.ForeignKey(Darasa, on_delete=models.CASCADE)
    mkondo = models.ForeignKey(Mkondo, on_delete=models.CASCADE, null=True, blank=True)
    status = models.ManyToManyField(StudentSubjectAttendanceStatus, blank=True)  # yupo, ana-ruhusa, hayupo, amechelewa, good-behaviour, bad-behaviour
    topic = models.CharField(max_length=50) # alichofundisha siku hiyo...
    subtopic = models.CharField(max_length=50, null=True, blank=True) # alichofundisha siku hiyo...
    # student = models.ManyToManyField(Student, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)  
    mwitaji = models.ForeignKey("MwalimuProfile", on_delete=models.CASCADE, null=True, blank=True, related_name="mahundurio")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    @property
    def get_status(self):
        statuses = []
        for status in self.status.all():
            statuses.append({
                "id": status.id,
                "status": status.status,
                "student": status.student.full_name,
                "student_id": status.student.id,
                "photo": status.student.photo.url if status.student.photo else None
            })

        return statuses
    
    @property
    def get_subject(self):
        if (self.subject):
            return {f"{self.subject.id}": f"{self.subject.name}"}
        return None
    
    @property
    def get_mwitaji(self):
        if (self.mwitaji):
            return {f"{self.mwitaji.id}": f"{self.mwitaji.full_name}"}
        return None
    
    @property
    def get_darasa(self):
        if (self.darasa):
            return {f"{self.darasa.id}": f"{self.darasa.name}"}
        return None

    @property
    def get_mkondo(self):
        if (self.mkondo):
            return {f"{self.mkondo.id}": f"{self.mkondo.stream_name}"}
        return None
    

# Mwalimu anakuwa created na Institute... By default in register we have 3 categories
# parent, org, and teacher, but the logic of 'teacher' when the submit the field to 
# create the user, we should check from this model if the email existed if its existed
# that's means the teacher have been added by Organization... and you should remember
# that the email we use it can't be used again to create another user/teacher so we 
# should have the field of 'is_user_created' to make sure its checked if there is a
# user of that email.... Easy logic
class MwalimuProfile(models.Model):
    email = models.CharField(max_length=500, unique=True) # we use this field as our user that's why it should be unique
    category = models.CharField(max_length=80, default="Teacher")
    is_user_created = models.BooleanField(default=False)
    full_name = models.CharField(max_length=300, null=True, blank=True)
    gender = models.CharField(max_length=500, null=True, blank=True)
    ni_mwalimu_wa_darasa = models.BooleanField(default=False)
    # if ni mwalimu wa darasa add, otherwise ni null
    darasa_lake = models.ForeignKey(Darasa, related_name='mwalimu', on_delete=models.SET_NULL, null=True, blank=True)
    # anafundisha madarasa mengi... .. haiwezekani ni mwalimu afu hauna darasa
    madarasa_anoyofundisha = models.ManyToManyField(Darasa, related_name="mfundishaji", blank=True) # nimeweka logic hii coz by default once org anavyo-add email isizuie
    # mwalimu wa darasa inabidi a-add student...
    register_date = models.CharField(max_length=50, blank=True, null=True)
    photo = models.ImageField(upload_to="images/", blank=True, null=True)
    isComplete = models.BooleanField(default=False)
    # one organization many teachers.. kuna walimu wanafundisha shule t
    organization = models.ManyToManyField(InstituteProfile, blank=True, related_name="mkufunzi")
    phone = models.CharField(max_length=50, null=True, blank=True)
    # mkondo uwe added, but its not mandatory.. admin/organization should add mkondo when he/she adding user
    # remember every mkondo has relation to darasa so from here we'll know which mkondo is associated with darasa.
    mikondo = models.ManyToManyField(Mkondo, blank=True, related_name="mwalimuprofile")

    def __str__(self):
        return f'{self.email} => 3'

    @property
    def get_photo(self):
        return self.photo.url
    
    @property
    def get_darasa_lake(self):
        return self.darasa_lake.id
    
    @property
    def get_madarasa_anayofundisha(self):
        madarasa = self.madarasa_anoyofundisha.all()
        ids = []
        for darasa in madarasa:
            ids.append(darasa.id)
        
        # return json.dumps(ids)
        return ids

    @property
    def get_mikondo_anayofundisha(self):
        mikondo = self.mikondo.all()
        ids = []
        for mkondo in mikondo:
            ids.append(mkondo.id)
        
        # return json.dumps(ids)
        return ids

    @property
    def get_masomo_anayofundisha_darasa(self):
        masomo_metadata = []
        for data in self.classtimetable.all():
            data = {f'{data.darasa.id}': f"{data.subject.name}"}
            masomo_metadata.append(data)

        return masomo_metadata

    @property
    def get_masomo_anayofundisha_mkondo(self):
        mikondo_metadata = []
        for data in self.classtimetable.all():
            data = {f'{data.mkondo.id}': f"{data.subject.name}", "darasa": data.mkondo.darasa.id}
            mikondo_metadata.append(data)

        return mikondo_metadata


    @property
    def get_organization(self):
        organizations = []
        for org in self.organization.all():
            organizations.append({
                "id": org.id,
                "name": org.name,
                "user_id": org.user.id
                })

        return organizations

'''
    tutatumia model hiihii ya ClassTimeTable in two ways, first as the 
    "MainModel" and the model which contains the metadata like day, subject
    time and so on... here lets say we want to have timetable of the same day sametime
    for given subject we can add as many as we want, but we should have validation b4 
    adding the timetable to make sure if user pass the 'mkondo' to make sure there is no
    timetable instance created of that day and same mkondo and same time and same subject
    .. here our unique together model is the day, subject, time, mkondo, and darasa
    so to get ClassTimeTable of let's say "Form I" we can fetch all the timetable where 
    the darasa is "Form I'
'''

class ClassTimeTable(models.Model):
    day = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    time = models.CharField(max_length=500)  # 8:00am - 9:00am
    darasa = models.ForeignKey(Darasa, related_name="ratibayadarasa", on_delete=models.CASCADE, null=True, blank=True)
    anaefundisha = models.ManyToManyField(MwalimuProfile, related_name="classtimetable", blank=True)
    mkondo = models.ForeignKey(Mkondo, related_name="ratibayaclass", on_delete=models.CASCADE, null=True, blank=True)    
    organization = models.ForeignKey(InstituteProfile, related_name="ratibayashule", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('day', 'subject', 'time', 'mkondo', 'darasa')


    @property
    def get_darasa(self):
        if (self.darasa):
            return {f"{self.darasa.id}": f"{self.darasa.name}"}
        return None

    @property
    def get_subject(self):
        if (self.subject):
            return {f"{self.subject.id}": f"{self.subject.name}"}
        return None


    @property
    def get_mfundishaji(self):
        if self.anaefundisha.all().count() > 0:
            # even if its many to many i expect to add only one teacher ..
            teacher = self.anaefundisha.all().last()

            return {f"{teacher.id}": f"{teacher.full_name}"}

        return None


    @property
    def get_mkondo(self):
        if self.mkondo:
            return {f"{self.mkondo.id}": f"{self.mkondo.stream_name}"} 
        return None

# Huyu mzazi model yake imekaa hapa basi tu inabidi iwe in parent app but because ina-relation na model ya Student here acha tuiache hapahapa
# mzazi anavyo-create account ni lazima tuwe na profile.. profile
class MzaziProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='mzazi')
    category = models.CharField(max_length=50, default="Mzazi") # mzazi... hii ndo muhimu kwa ajili ya kum-redirect user... 
    # relationship inabidi a-send "stringified" object since he can add as many as student he/she wants
    # mfano {"5": "Parent"}, {"20": "Guardian"} .. ko id of student to relations...
    relationship = models.CharField(max_length=500, default="Parent")
    # mzazi mmoja anaweza akawa na wanafunzi wengi kwenye organization tofauti...
    student = models.ManyToManyField(Student, blank=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    # mzazi is_completed inahitaji ili kuweza ku-add students to display...k o by default
    # aki-sha save/add students will 
    profile_is_completed = models.BooleanField(default=False)
    def __str__(self):
        return self.user.email
    
    @property
    def get_students(self):
        wanafunzi = self.student.all()
        ids = []
        for mwanafunzi in wanafunzi:
            obj = {
                "mwanafunzi_id": mwanafunzi.id,
                "org_user_id": mwanafunzi.organization.user.id,
            }
            ids.append(obj)
        
        return json.dumps(ids)

class SchoolExamTimeTable(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.CharField(max_length=50)
    end_date = models.CharField(max_length=50)
    is_finished = models.BooleanField(default=False)
    organization = models.ForeignKey(InstituteProfile, on_delete=models.CASCADE, related_name="school_timetables", null=True, blank=True)
    # Kama mtihani ratiba imeshafika mwisho basi itakuwa is_finished = True
    # usi-delete ratiba bali kupitia hii field ya is_finished itatuwezesha 
    # kujua kama mtihani umefika mwisho au la..
    # kupitia hii itakuwa rahisi ku-hide na ku-generate report za ratiba za nyuma
    # haito delete.... 
    # tunai-disable ratiba school table..
    # pale mtu ana-vyoclick add school_timetable for given organization inabidi ije icheck
    # available school timetable if there is one having the 'expire' date should make its
    # is_finished = True......



# uploaded by organization..
# hii ni darasa timetable ya mtihani, and many darasa timetable zinabelong to given block
# of SchoolTimetable()... so inakuwa rahisi ku-track timetable of given let's say "TimeTable"



# marked at lets us define the type/exam which resemble or made at the
# matokeo ya somo.. matokeo ya somo.... ana-add mwalimu
class SubjectResult(models.Model):
    # hii type ndo inayotofautisha aina ya mitihani tunaweza tukawa na 'Assignment, ....'
    # type ndo inayotufanya tusi-create another model of "OverallResult" coz we've got the type.
    type = models.CharField(max_length=50, blank=True, null=True) # either iwe mtihani au assignment, test, ujirani mwema, Homework, friend-exam ... etc iwe dropdown ili tuweze ku-generate report
    # unique code kujua mtiaani x-assignment ili kujua kwenye assigment fulani alikuwa wangapi.. unique code
    submitted_at = models.CharField(max_length=800) # siku ya ku-submit matokeo lini... hii ndo unique code ya mtihani specific...
    # muhula = models.CharField(max_length=50, null=True, blank=True) # mtihani unaweza ukawa test/assigment so no need to put the muhula.. Remember we have terminal, annual, mid-term exams

    somo = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="somoresults")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="studentresult")
    marked_by = models.ForeignKey(MwalimuProfile, on_delete=models.SET_NULL, blank=True, null=True, related_name="results")
    mark = models.CharField(max_length=50)
    totalMarks = models.PositiveIntegerField(default=100)
    # darasa la matokeo husika...
    darasa = models.ForeignKey(Darasa, on_delete=models.SET_NULL, blank=True, null=True, related_name="matokeo")
    mkondo = models.ForeignKey(Mkondo, on_delete=models.SET_NULL, blank=True, null=True, related_name="matokeoyasomo")
    # kwa mitihani midogo midogo like past papers, assignments, test, homework, ujirani mwema, friend-exam, etc
    # hii field ya SchoolExamTimetable haina maana hii field ina maana if 'mwalimu' anataka ku-add mitihani mikubwa 
    # hasahasa ile ya kishule sio mitihani midogomidogo, ko kama ni mitihani ya kishule kama mid-term, annual, terminal, etc
    # hii field ya SchoolExamTimetable ina maana if 'mwalimu' anataka ku-add mitihani mikubwa
    school_exam = models.ForeignKey(SchoolExamTimeTable, on_delete=models.SET_NULL, blank=True, null=True, related_name="school_exam_results")
    organization = models.ForeignKey(InstituteProfile, on_delete=models.CASCADE, related_name="majibu", null=True, blank=True)


    @property
    def get_somo(self):
        return {"id": self.somo.id, "name": self.somo.name}
    
    @property
    def get_student(self):
        return {"id": self.student.id, "name": self.student.full_name}

    @property
    def get_marked_by(self):
        return {"id": self.marked_by.id, "name": self.marked_by.full_name}

    @property
    def get_darasa(self):
        return {"id": self.darasa.id, "name": self.darasa.name}
    
    @property
    def get_mkondo(self):
        if self.mkondo:
            return {"id": self.mkondo.id, "name": self.mkondo.stream_name}
        return None
    
    @property
    def get_school_exam(self):
        if self.school_exam:
            return {"id": self.school_exam.id, "name": self.school_exam.name, "start": self.school_exam.start_date, "end": self.school_exam.end_date}
        return None
    
    @property
    def get_organization(self):
        return {"id": self.organization.id, "name": self.organization.name}
    

class ExamTimeTable(models.Model):
    date = models.CharField(max_length=50)
    # unaweza ukapunguza somo moja ila ukataka mengine yabaki..
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.CharField(max_length=500)
    end_time = models.CharField(max_length=500)
    darasa = models.ForeignKey(Darasa, on_delete=models.CASCADE)
    schoool_timetable = models.ForeignKey(SchoolExamTimeTable, on_delete=models.CASCADE, related_name="darasa_timetable", null=True, blank=True)
    # ni vizuri tuweke hapa organization field instead of school_timetable coz hii ndo yenye darasa..
    organization = models.ForeignKey(InstituteProfile, on_delete=models.CASCADE, related_name="ratiba_ya_mtihanidarasa", null=True, blank=True)

    @property
    def get_subject(self):
        return {
            "id": self.subject.id,
            "name": self.subject.name
        }
    
    @property
    def get_darasa(self):
        return {"id": self.darasa.id, "name": self.darasa.name}
    
    @property
    def get_school_timetable(self):
        return {"id": self.schoool_timetable.id, "name": self.schoool_timetable.name}

# anaepost ni admin/org e.g likizo au sikukuu, e.g likizo..
class Matukio(models.Model):
    name = models.CharField(max_length=50)
    starting_date = models.CharField(max_length=50)
    ending_date = models.CharField(max_length=50)
    # hii inakuwa specific endapo sio ya shule nzima.. if ni ya wote basi ni option.....
    darasa = models.ManyToManyField(Darasa, blank=True)
    organization = models.ForeignKey(InstituteProfile, on_delete=models.CASCADE, related_name="matukio", null=True, blank=True)


    @property
    def get_darasa(self):
        darasas = self.darasa.all()
        ids = []
        for darasa in darasas:
            ids.append({
                "id": darasa.id,
                "name": darasa.name
            })
        
        return json.dumps(ids)
    