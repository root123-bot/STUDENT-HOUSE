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
        return self.user.email + ' => ' + ' Institute'
    
    @property
    def get_logo(self):
        return self.logo.url
    

class Mkondo(models.Model):
    stream_name = models.CharField(max_length=400)



class Subject(models.Model):
    name = models.CharField(max_length=500)


# ina-bidi a-add mwalimu wa darasa.. haina relation na any model ni just kumsaidia mwalimu anavyoita attendancy
# hii ita-sync na attendacy kabila mwalimu hajaita ita-sync.... excuse tuta-refer ya attendancy na excuse
# wanafunzi wengi ruhusa moja... one to many... ku-sync nafanya in backend sindo naupdate DB..
class Excuse(models.Model):
    ruhusayanini = models.CharField(max_length=8000)
    # isstill = models.BooleanField(default=True) # ko atakapo-rudi inabidi aripoti kwa mwalimu wa darasa ili delete
    issued_at = models.CharField(max_length=50)
    # student tushalink kule chini so haina haja ya kuweka student wala darasa...



# sync, kila mwaka unavyoisha admin/organization inabidi a-sync manually madarasa coz atujui ni lini
# ko-aki-click 'syc' to new year maanke wanafunzi madarasa yao ina-bidi yahame ya increment by one from 
#  the list of CLASSES above.. ko hii ina-change in students..
class Student(models.Model):
    full_name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="images/")
    birth_date = models.CharField(max_length=500)
    gender = models.CharField(max_length=50)
    role = models.CharField(max_length=500) # either monitor, headbox etc
    # inakuepo mtu anavyo-add ruhusa... ndo hii field inakuepo..
    excuse = models.ForeignKey(Excuse, on_delete=models.SET_NULL, null=True, blank=True)
    register_date = models.CharField(max_length=50)
    

# validation in your apis, to check to check if the teacher ni mwalimu wa darasa husika asi-add mwanafunzi kama sio mwalimu wa darasa
class Darasa(models.Model):
    name = models.CharField(max_length=400)
    subclass = models.ForeignKey(Mkondo, on_delete=models.SET_NULL, blank=True, null=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    students = models.ForeignKey(Student, on_delete=models.CASCADE)



# kila mwalimu anavyo-ingia darasani inabidi aite attendancy..... kwa siku zinaweza zikaitwa attendancy 10..
class Attendency(models.Model):
    day = models.CharField(max_length=50)
    darasa = models.OneToOneField(Darasa, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)  # yupo, ana-ruhusa, hayupo, amechelewa, good-behaviour, bad-behaviour
    topic = models.CharField(max_length=50) # alichofundisha siku hiyo...
    subtopic = models.CharField(max_length=50, null=True, blank=True) # alichofundisha siku hiyo...


    

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
    organization = models.ManyToManyField(InstituteProfile, blank=True)


    def __str__(self):
        return self.email 

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
        
        return json.dumps(ids)


# should be added only by the mwalimu wa darasa otherwise don't change/delelete
# hatupo kwenye shule nzima...
class ClassTimeTable(models.Model):
    day = models.CharField(max_length=50)
    # unaweza ukapunguza somo moja ila ukataka mengine yabaki..
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    time = models.CharField(max_length=500)
    darasa = models.OneToOneField(Darasa, on_delete=models.CASCADE, unique=True)
    anaefundisha = models.ManyToManyField(MwalimuProfile)


# Huyu mzazi model yake imekaa hapa basi tu inabidi iwe in parent app but because ina-relation na model ya Student here acha tuiache hapahapa
# mzazi anavyo-create account ni lazima tuwe na profile.. profile
class MzaziProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='mzazi')
    category = models.CharField(max_length=50, default="Mzazi")
    # mzazi mmoja anaweza akawa na wanafunzi wengi kwenye organization tofauti...
    student = models.ManyToManyField(Student, blank=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    profile_is_completed = models.BooleanField(default=False)
    def __str__(self):
        return self.user.email
    
    @property
    def get_students(self):
        wanafunzi = self.student.all()
        ids = []
        for mwanafunzi in wanafunzi:
            ids.append(mwanafunzi.id)
        
        return json.dumps(ids)

# marked at lets us define the type/exam which resemble or made at the
# matokeo ya somo.. matokeo ya somo.... ana-add mwalimu
class SubjectResult(models.Model):
    # hii type ndo inayotofautisha aina ya mitihani tunaweza tukawa na 'Assignment, ....'
    # type ndo inayotufanya tusi-create another model of "OverallResult" coz we've got the type.
    type = models.CharField(max_length=50) # either iwe mtihani au assignment, test, ujirani mwema, Homework, friend-exam ... etc iwe dropdown ili tuweze ku-generate report
    # unique code kujua mtiaani x-assignment ili kujua kwenye assigment fulani alikuwa wangapi.. unique code
    submitted_at = models.CharField(max_length=800) # siku ya ku-submit matokeo lini... hii ndo unique code ya mtihani specific...
    muhula = models.CharField(max_length=50, null=True, blank=True) # mtihani unaweza ukawa test/assigment so no need to put the muhula.. Remember we have terminal, annual, mid-term exams

    somo = models.OneToOneField(Subject, on_delete=models.CASCADE, related_name="somoresults")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="studentresult")
    marked_by = models.ForeignKey(MwalimuProfile, on_delete=models.SET_NULL, blank=True, null=True, related_name="results")
    mark = models.PositiveIntegerField()
    # darasa la matokeo husika...
    darasa = models.ForeignKey(Darasa, on_delete=models.SET_NULL, blank=True, null=True, related_name="matokeo")


# uploaded by organization..
class ExamTimeTable(models.Model):
    date = models.CharField(max_length=50)
    # unaweza ukapunguza somo moja ila ukataka mengine yabaki..
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.CharField(max_length=500)
    end_time = models.CharField(max_length=500)
    darasa = models.OneToOneField(Darasa, on_delete=models.CASCADE, unique=True)

# anaepost ni admin/org e.g likizo au sikukuu, e.g likizo..
class Matukio(models.Model):
    name = models.CharField(max_length=50)
    starting_date = models.CharField(max_length=50)
    ending_date = models.CharField(max_length=50)
    # hii inakuwa specific endapo sio ya shule nzima.. if ni ya wote basi ni option.....
    darasa = models.ManyToManyField(Darasa, blank=True)
    


    