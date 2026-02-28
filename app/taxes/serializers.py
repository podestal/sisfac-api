from rest_framework import serializers
from . import models

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DocumentType
        fields = ['id', 'code', 'name']


class BusinessSunatConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BusinessSunatConfig
        fields = ['id', 'business', 'persona_id', 'persona_token', 'production_enabled']

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Party
        fields = ['id', 'business', 'doc_type', 'doc_number', 'name', 'address', 'email', 'phone', 'is_active']

class SunatDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SunatDocument
        fields = ['id', 'business', 'document_type', 'series', 'number', 'issue_date', 'party', 'order', 'currency', 'exchange_rate', 'payment_term', 'due_date', 'total_taxable', 'total_igv', 'total', 'status', 'ref_document']

class SunatDocumentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SunatDocumentItem
        fields = ['id', 'document', 'product', 'description', 'quantity', 'unit_price', 'discount', 'tax_affectation', 'igv_rate', 'line_total']


class SunatSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SunatSubmission
        fields = [
            'id', 
            'document', 
            'production', 
            'file_name', 
            'apisunat_document_id', 
            'status', 
            'xml_url', 
            'cdr_url', 
            'sunat_issued_at', 
            'sunat_responded_at', 
            'faults', 
            'notes', 
            'error_message', 
            'raw_request', 
            'raw_response',
            'created_at', 
            'updated_at',
        ]

