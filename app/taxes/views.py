from django.shortcuts import render
from rest_framework import viewsets
from . import models, serializers

class DocumentTypeViewSet(viewsets.ModelViewSet):
    queryset = models.DocumentType.objects.all()
    serializer_class = serializers.DocumentTypeSerializer

class BusinessSunatConfigViewSet(viewsets.ModelViewSet):
    queryset = models.BusinessSunatConfig.objects.all()
    serializer_class = serializers.BusinessSunatConfigSerializer

class PartyViewSet(viewsets.ModelViewSet):
    queryset = models.Party.objects.all()
    serializer_class = serializers.PartySerializer

class SunatDocumentViewSet(viewsets.ModelViewSet):
    queryset = models.SunatDocument.objects.all()
    serializer_class = serializers.SunatDocumentSerializer

class SunatDocumentItemViewSet(viewsets.ModelViewSet):
    queryset = models.SunatDocumentItem.objects.all()
    serializer_class = serializers.SunatDocumentItemSerializer

class SunatSubmissionViewSet(viewsets.ModelViewSet):
    queryset = models.SunatSubmission.objects.all()
    serializer_class = serializers.SunatSubmissionSerializer

