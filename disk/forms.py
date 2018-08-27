#encoding:utf-8
from django.forms import ModelForm
from models import UploadDownFile
from django import forms


class FileUploadDown(ModelForm):
    class Meta:
        model = UploadDownFile
        fields = '__all__'

