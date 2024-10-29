from django.db import models
from django.utils import timezone
import os
import random
from django.utils import timezone

import uuid
from authentications.models import User
# Create your models here.
# Can be removed until upload() is implemented

def upload_to(instance, filename):
    base, extension = os.path.splitext(filename.lower())
    print(filename)
    return f"{filename}"

class Patient(models.Model):
    name= models.CharField(primary_key=True, max_length=255, unique=True)
    # Dates
    date_created = models.DateTimeField(auto_now_add=True)
    
    
# Create your models here.
class Study(models.Model):
    name = models.CharField( primary_key=True, max_length=255, unique=True)

    # Owner (relation)
    owner = models.ForeignKey(Patient, on_delete=models.CASCADE,
                              related_name='patient_studies')
    # Dates
    date_created = models.DateTimeField(auto_now_add=True)
    # Media
    media_file = models.FileField(upload_to=upload_to)
    
    AD_percent= models.FloatField( blank=True,null=True,default=0)
    CN_percent= models.FloatField( blank=True,null=True,default=0)
    MCI_percent= models.FloatField(blank=True,null=True,default=0)
    CLASS_CHOICES = (('CN','CN'),('MCI','MCI'),('AD','AD'))
    predicted_class= models.CharField(max_length=4,choices=CLASS_CHOICES,blank=True,null=True, default='CN')





