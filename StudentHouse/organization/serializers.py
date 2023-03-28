
from rest_framework import serializers
from .models import *

class MzaziSerializer(serializers.ModelSerializer):
    class Meta:
        model = MzaziProfile
        fields = [
            'id',
            'category',
            'get_students'
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
            'regnon',
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
        ]

class MwalimuProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MwalimuProfile
        fields = [
            'id',
            'email',
            'category',
            'full_name',
            'gender',
            'ni_mwalimu_wa_darasa',
            'register_date',
            'get_madarasa_anayofundisha',
            'photo',
            'is_complete'
        ]