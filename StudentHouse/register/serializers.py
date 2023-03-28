from rest_framework import serializers
from django.contrib.auth import get_user_model



class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']  

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        fields = ('email',)

