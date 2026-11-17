from django.urls import path, include
from . import views

app_name = 'images'

urlpatterns = [
    path('upload', views.upload_media, name='upload_media'),
    path('history', views.GetHistory, name='GetHistory'),
    path('predict/<int:id>', views.GetPrediction, name='GetPrediction'),
    path('study/<int:id>', views.GetStudy, name='GetStudy'),
    path('studies/<int:id>', views.Getstudies, name='Getstudies'),

]
