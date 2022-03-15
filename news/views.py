# from django.shortcuts import render

from rest_framework import viewsets
from .serializers import NewsitemSerializer, KeySerializer, CompanySerializer, PostingsiteSerializer
from .models import Newsitem, Key, Company, Postingsite

# Create your views here.

class NewsitemViewSet(viewsets.ModelViewSet):
    queryset = Newsitem.objects.all().order_by('date_posted')
    serializer_class = NewsitemSerializer

class KeyViewSet(viewsets.ModelViewSet):
    queryset = Key.objects.all()
    serializer_class = KeySerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class PostingsiteViewSet(viewsets.ModelViewSet):
    queryset = Postingsite.objects.all()
    serializer_class = PostingsiteSerializer