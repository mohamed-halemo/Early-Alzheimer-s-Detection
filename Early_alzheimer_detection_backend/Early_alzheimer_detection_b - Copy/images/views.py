from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .serializers import *
import numpy as np 
import nibabel as nib
from .functions import *
from .models import *
from os import listdir
from os.path import isfile, join
import operator

@api_view(['GET'])
# Create your views here.
def GetHistory(request):
        Studies=Study.objects.all()
        serializer = PhotoUploadSerializer(Studies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
# Create your views here.
@parser_classes((FormParser,MultiPartParser,FileUploadParser))
def upload_media(request):
    if ('media_file' not in request.data):
        return Response( {'message': "File is missing"}, status=status.HTTP_400_BAD_REQUEST)
    file_name= request.data["media_file"]
    if (file_name == ''):
        return Response( {'message': "empty"}, status=status.HTTP_200_OK)
    # img = load(str(file_name))
    # header = img.header
    file_name= str(file_name)

    print(file_name)
    Patient_id=re.search(r"ADNI_\d+_S_\d+",file_name)
    Patient_id=Patient_id.group()
    Patient_id=Patient_id.replace("ADNI","")
    Patient_id=Patient_id.replace("_","",1)

    Study_name=re.search(r"S\d+",file_name)
    study_id= Study_name.group()
    study_id= study_id.replace("S","")
    # Patient_id= str(header.get('db_name',''))
    path_folder="D:\\Graduation_project\\Github\\Early_alzheimer_detection_f\\public"
    path_folder=os.path.join(path_folder,Patient_id,study_id)
    # path_folder=os.path.join(Patient_id,study_id)

    try :   
        patient_obj=Patient.objects.get(name=Patient_id)
        _ = Study.objects.get(name=study_id, owner=patient_obj)

        # coronal_path=os.path.join(Patient_id,study_id,"coronal" )
        # sagittal_path=os.path.join(Patient_id,study_id,"sagittal" )
        # axial_path=os.path.join(Patient_id,study_id,"axial" )

        # coronal_Folder=os.path.join(path_folder,"coronal" )
        # sagittal_Folder=os.path.join(path_folder,"sagittal" )
        # axial_Folder=os.path.join(path_folder,"axial" )

        # coronalfiles = [os.path.join(coronal_path, f) for f in listdir(coronal_Folder) ]
        # new_coronal_path=  [f.replace("\\","/") for f in coronalfiles]
        # sagittalfiles = [os.path.join(sagittal_path, f) for f in listdir(sagittal_Folder) ]
        # new_sagittal_path=  [f.replace("\\","/") for f in sagittalfiles]
        # axialfiles = [os.path.join(axial_path, f) for f in listdir(axial_Folder) ]
        # new_axial_path=  [f.replace("\\","/") for f in axialfiles]

        # new_coronal_path.sort(key=lambda x: int(x.split('slice')[1].split('.dcm')[0]))
        # new_sagittal_path.sort(key=lambda x: int(x.split('slice')[1].split('.dcm')[0]))
        # new_axial_path.sort(key=lambda x: int(x.split('slice')[1].split('.dcm')[0]))

        # return Response({"axial":new_axial_path, "coronal":new_coronal_path , "sagittal": new_sagittal_path },status=status.HTTP_201_CREATED  )
        return Response({"id":study_id },status=status.HTTP_201_CREATED  )
    
    except ObjectDoesNotExist:
        serializer = PatientSerializer(data={"name":Patient_id})
        if serializer.is_valid():
            serializer.save()
        patient_obj=Patient.objects.get(name=Patient_id)

        data=request.data
        data["name"]=study_id

        serializer = PhotoUploadSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=patient_obj)
        file_name= os.path.join("./",str(file_name)) 

        ConvertNIFTI(file_name,"axial")
        ConvertNIFTI(file_name,"sagittal")
        ConvertNIFTI(file_name,"coronal")

        # coronal_path=os.path.join(Patient_id,study_id,"coronal" )
        # sagittal_path=os.path.join(Patient_id,study_id,"sagittal" )   
        # axial_path=os.path.join(Patient_id,study_id,"axial" )

        # coronal_Folder=os.path.join(path_folder,"coronal" )
        # sagittal_Folder=os.path.join(path_folder,"sagittal" )
        # axial_Folder=os.path.join(path_folder,"axial" )

        # coroalfiles = [os.path.join(coronal_path, f)  for f in listdir(coronal_Folder)]
        # sagittalfiles = [os.path.join(sagittal_path, f)  for f in listdir(sagittal_Folder)]
        # axialfiles = [os.path.join(axial_path, f)  for f in listdir(axial_Folder)]

        # new_coronal_path=  [f.replace("\\","/") for f in coroalfiles]
        # new_sagittal_path=  [f.replace("\\","/") for f in sagittalfiles]
        # new_axial_path=  [f.replace("\\","/") for f in axialfiles]

        # new_coronal_path.sort(key=lambda x: int(x.split('slice')[1].split('.dcm')[0]))
        # new_sagittal_path.sort(key=lambda x: int(x.split('slice')[1].split('.dcm')[0]))
        # new_axial_path.sort(key=lambda x: int(x.split('slice')[1].split('.dcm')[0]))
        ConvertToVTI(file_name)
        # return Response({"axial":new_axial_path, "coronal":new_coronal_path , "sagittal": new_sagittal_path },status=status.HTTP_201_CREATED  )
        return Response({"id":study_id },status=status.HTTP_201_CREATED  )

@api_view(['Get'])
# Create your views here.
def GetPrediction(request,id):
        study_obj = Study.objects.get(name=id)

        file_name= str(study_obj.media_file)

        # Specify the input image path and root folder
        root_folder = 'D:/Graduation_project/Dataset/Original_Dataset'
        # Call the function
        prcentage=find_matching_file_Slices_and_predict(file_name, root_folder)
        Patient_id=re.search(r"ADNI_\d+_S_\d+",file_name)
        Patient_id=Patient_id.group()
        Patient_id=Patient_id.replace("ADNI","")
        Patient_id=Patient_id.replace("_","",1)

        Study_name=re.search(r"S\d+",file_name)
        study_id= Study_name.group()
        study_id= study_id.replace("S","")
        patient_obj=Patient.objects.get(name=Patient_id)
        study_obj = Study.objects.get(name=study_id, owner=patient_obj)
        Study.objects.filter(name=study_id).update(AD_percent=prcentage["AD"] ,CN_percent=prcentage["CN"] , MCI_percent= prcentage["MCI"] ,predicted_class= max(prcentage.items(), key=operator.itemgetter(1))[0] ) 
        study_obj = Study.objects.get(name=study_id, owner=patient_obj)
        serializer = PhotoUploadSerializer(study_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
# Create your views here.
def GetStudy(request, id):
    study_obj = Study.objects.get(name=id)

    file_name= str(study_obj.media_file)

    print(file_name)
    Patient_id=re.search(r"ADNI_\d+_S_\d+",file_name)
    Patient_id=Patient_id.group()
    Patient_id=Patient_id.replace("ADNI","")
    Patient_id=Patient_id.replace("_","",1)

    Study_name=re.search(r"S\d+",file_name)
    study_id= Study_name.group()
    study_id= study_id.replace("S","")
    # Patient_id= str(header.get('db_name',''))
    path_folder="D:\\Graduation_project\\Github\\Early_alzheimer_detection_f\\public"
    path_folder=os.path.join(path_folder,Patient_id,study_id)
    # path_folder=os.path.join(Patient_id,study_id)
    patient_obj=Patient.objects.get(name=Patient_id)
    _ = Study.objects.get(name=study_id, owner=patient_obj)

    coronal_path=os.path.join(Patient_id,study_id,"coronal" )
    sagittal_path=os.path.join(Patient_id,study_id,"sagittal" )
    axial_path=os.path.join(Patient_id,study_id,"axial" )

    coronal_Folder=os.path.join(path_folder,"coronal" )
    sagittal_Folder=os.path.join(path_folder,"sagittal" )
    axial_Folder=os.path.join(path_folder,"axial" )

    coronalfiles = [os.path.join(coronal_path, f) for f in listdir(coronal_Folder) ]
    new_coronal_path=  [f.replace("\\","/") for f in coronalfiles]
    sagittalfiles = [os.path.join(sagittal_path, f) for f in listdir(sagittal_Folder) ]
    new_sagittal_path=  [f.replace("\\","/") for f in sagittalfiles]
    axialfiles = [os.path.join(axial_path, f) for f in listdir(axial_Folder) ]
    new_axial_path=  [f.replace("\\","/") for f in axialfiles]

    new_coronal_path.sort(key=lambda x: int(x.split('slice')[1].split('.dcm')[0]))
    new_sagittal_path.sort(key=lambda x: int(x.split('slice')[1].split('.dcm')[0]))
    new_axial_path.sort(key=lambda x: int(x.split('slice')[1].split('.dcm')[0]))

    return Response({"axial":new_axial_path, "coronal":new_coronal_path , "sagittal": new_sagittal_path , "selected_file": file_name },status=status.HTTP_201_CREATED  )

@api_view(['GET'])
# Create your views here.
def Getstudies(request, id):
    study_obj = Study.objects.get(name=id)

    # file_name= str(study_obj.media_file)

    # # Specify the input image path and root folder
    # root_folder = 'D:/Graduation_project/Dataset/Original_Dataset'
    # # Call the function
    # prcentage=find_matching_file_Slices_and_predict(file_name, root_folder)
    # Patient_id=re.search(r"ADNI_\d+_S_\d+",file_name)
    # Patient_id=Patient_id.group()
    # Patient_id=Patient_id.replace("ADNI","")
    # Patient_id=Patient_id.replace("_","",1)

    # Study_name=re.search(r"S\d+",file_name)
    # study_id= Study_name.group()
    # study_id= study_id.replace("S","")
    # patient_obj=Patient.objects.get(name=Patient_id)
    # study_obj = Study.objects.get(name=study_id, owner=patient_obj)
    # Study.objects.filter(name=study_id).update(AD_percent=prcentage["AD"] ,CN_percent=prcentage["CN"] , MCI_percent= prcentage["MCI"] ,predicted_class= max(prcentage.items(), key=operator.itemgetter(1))[0] ) 

    studies=Study.objects.filter(owner=study_obj.owner)   
    serializer = PhotoUploadSerializer(studies,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
