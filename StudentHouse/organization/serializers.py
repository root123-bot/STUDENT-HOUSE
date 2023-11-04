
from rest_framework import serializers
from .models import *

class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteProfile
        fields = [
            'id',
            'get_logo',
            'organization_metadata',
            'org_classes',
            'org_mikondo',
            'org_students',
        ]

# hii "day" ndo imehold tarehe ya given attendancy
class AttendancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendency
        fields = [
            'id',
            'get_status',
            'get_subject',
            'get_darasa',
            'get_mkondo',
            'get_mwitaji',
            'topic',
            'subtopic',
            'day',
            # 'created_at',
        ]

class SubjectResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectResult
        fields = [
            'id',
            'type',
            'mark',
            'totalMarks',
            'submitted_at',
            'get_somo',
            'get_darasa',
            'get_mkondo',
            'get_student',
            'get_marked_by',
            'get_organization',
            'get_school_exam',
        ]

class StudentExcuseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excuse
        fields = [
            'id',
            'get_student',
            'issued_at',
            'ruhusayanini'
        ]

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'full_name',
            'get_photo',
            'birth_date',
            'gender',
            'role',
            'register_date',
            'get_darasa',
            'get_mkondo',
            'nationality',
            'health',
            'religion'
        ]

class ClassExamTimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamTimeTable
        fields = [
            'id',
            'date',
            'get_subject',
            'start_time',
            'end_time',
            'get_darasa',
            'get_school_timetable',
        ]

class MatukioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matukio
        fields = [
            'id',
            'name',
            'starting_date',
            'ending_date',
            'get_darasa',
        ]

class SchoolExamTimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolExamTimeTable
        fields = [
            'id',
            'name',
            'start_date',
            'end_date',
        ]

class ClassTimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassTimeTable
        fields = [
            'id',
            'day',
            'get_subject',
            'time',
            'get_darasa',
            'get_mfundishaji',
            'get_mkondo'
        ]

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Darasa
        fields = [
            'id',
            'name',
        ]

# create Darasa serializer
class DarasaSerializer(serializers.ModelSerializer):
    # create meta class
    class Meta:
        # specify model to be used
        model = Darasa
        # specify fields to be serialized
        fields = [
            'id',
            'name',
            'get_mikondo',
            'get_subjects',
            'get_students',
            'get_mwalimu_wa_darasa',
            'get_walimu',
        ]

class MzaziSerializer(serializers.ModelSerializer):
    class Meta:
        model = MzaziProfile
        fields = [
            'id',
            'category',
            'get_students',
            'profile_is_completed',
            'relationship'

        ]

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteProfile
        fields = [
            'id',
            'phone',
            'country',
            'region',
            'district',
            'type',
            'regno',
            'name',
            'web',
            'headname',
            'ceo',
            'address',
            'opentime',
            'category',
            'isComplete',
            'school_level',
            'register_date',
            'get_logo',
        ]

class MwalimuProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MwalimuProfile
        fields = [
            'get_organization',
            'id',
            'email',
            'category',
            'full_name',
            'gender',
            'ni_mwalimu_wa_darasa',
            'darasa_lake',
            'register_date',
            'get_madarasa_anayofundisha',
            'get_mikondo_anayofundisha',
            'photo',
            'isComplete',
            'get_masomo_anayofundisha_darasa',
            'get_masomo_anayofundisha_mkondo',
            'phone',
        ]

class MkondoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mkondo
        fields = [
            'id',
            'stream_name',
        ]
