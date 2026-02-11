from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Business
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Serializer para datos básicos del usuario"""
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'is_active', 'date_joined']
        read_only_fields = ['id', 'username', 'date_joined']

    def get_full_name(self, obj):
        """Retorna el nombre completo del usuario"""
        return obj.get_full_name() or obj.username


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer para el perfil con datos del usuario incluidos"""
    user = UserSerializer(read_only=True)
    business = BusinessSerializer(read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = models.Profile
        fields = [
            'id',
            'user',
            'business',
            'role',
            'role_display',
            'employee_id',
            'phone_number',
            'address',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProfileMeSerializer(serializers.ModelSerializer):
    """Serializer aplanado para el endpoint /me/ - estructura simplificada"""
    # Campos del usuario (aplanados)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    # Campos del negocio (aplanados) - pueden ser None para admins de plataforma
    business_id = serializers.SerializerMethodField()
    business_name = serializers.SerializerMethodField()
    
    # Campos del perfil
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = models.Profile
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'business_id',
            'business_name',
            'role',
            'role_display',
            'employee_id',
            'phone_number',
            'address',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_business_id(self, obj):
        """Retorna el ID del negocio o None si no existe"""
        return obj.business.id if obj.business else None

    def get_business_name(self, obj):
        """Retorna el nombre del negocio o None si no existe"""
        return obj.business.name if obj.business else None


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = '__all__'