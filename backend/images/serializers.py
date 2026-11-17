from rest_framework import serializers
from .models import *
from authentications.serializers import *

class PatientSerializer(serializers.ModelSerializer):
    # owner = OwnerSerializer(read_only=True)
    # class Meta:
    #     model = Photo
    #     fields = [
    #         'id', 'media_file', 'description','date_posted','owner']
    #     #   add tags
    #     extra_kwargs = {
    #         'owner': {'read_only': True}}
    class Meta:
        model = Patient
        fields = '__all__'
        
class PhotoUploadSerializer(serializers.ModelSerializer):
    owner = PatientSerializer(read_only=True)
    # class Meta:
    #     model = Photo
    #     fields = [
    #         'id', 'media_file', 'description','date_posted','owner']
    #     #   add tags
    #     extra_kwargs = {
    #         'owner': {'read_only': True}}
    class Meta:
        model = Study
        fields = ['name', 'media_file','date_created',"owner","AD_percent","CN_percent","MCI_percent","predicted_class"]
        extra_kwargs = {
            'owner': {'read_only': True}}
