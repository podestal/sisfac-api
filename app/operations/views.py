from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from . import models, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


# Create your views here.
class BusinessViewSet(viewsets.ModelViewSet):
    queryset = models.Business.objects.all()
    serializer_class = serializers.BusinessSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.select_related('business').all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filtra categorías por el negocio del usuario autenticado.
        """
        queryset = super().get_queryset()

        # Obtener el negocio del usuario desde su perfil
        try:
            profile = models.Profile.objects.get(user=self.request.user)
            # Si es admin de plataforma, puede ver todas las categorías
            if profile.is_platform_admin:
                business_id = self.request.query_params.get('business_id', None)
                if business_id:
                    queryset = queryset.filter(business_id=business_id)
            else:
                # Usuarios normales solo ven categorías de su negocio
                if profile.business:
                    queryset = queryset.filter(business=profile.business)
                else:
                    # Si no tiene negocio, no puede ver categorías
                    return models.Category.objects.none()
        except models.Profile.DoesNotExist:
            # Si no tiene perfil, no puede ver categorías
            return models.Category.objects.none()

        return queryset.order_by('name')


class ProductPagination(PageNumberPagination):
    """Paginación personalizada para productos"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.select_related('category', 'business').all()
    serializer_class = serializers.ProductSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticated]

    # Campos permitidos para ordenamiento
    ORDERING_FIELDS = ['name', 'code', 'stock', 'buy_price', 'sell_price', 'created_at']

    def get_queryset(self):
        """
        Filtra productos por:
        - Negocio del usuario autenticado (basado en su perfil)
        - Categoría (si se proporciona como query parameter)
        - Búsqueda por nombre o código (parámetro 'search')
        Ordena por el campo especificado en el parámetro 'ordering'
        """
        queryset = super().get_queryset()

        # Obtener el negocio del usuario desde su perfil
        try:
            profile = models.Profile.objects.get(user=self.request.user)
            # Si es admin de plataforma, puede ver todos los productos
            if profile.is_platform_admin:
                business_id = self.request.query_params.get('business_id', None)
                if business_id:
                    queryset = queryset.filter(business_id=business_id)
            else:
                # Usuarios normales solo ven productos de su negocio
                if profile.business:
                    queryset = queryset.filter(business=profile.business)
                else:
                    # Si no tiene negocio, no puede ver productos
                    return models.Product.objects.none()
        except models.Profile.DoesNotExist:
            # Si no tiene perfil, no puede ver productos
            return models.Product.objects.none()

        # Filtrar por categoría si se proporciona
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Búsqueda por nombre o código
        search = self.request.query_params.get('search')
        if search:
            # Limpiar espacios en blanco del término de búsqueda
            search = search.strip()
            if search:
                # Construir el filtro de búsqueda
                # Buscar en nombre O código
                search_filter = Q(name__icontains=search) | Q(code__icontains=search)
                # Aplicar el filtro
                queryset = queryset.filter(search_filter)

        # Ordenamiento dinámico
        ordering = self.request.query_params.get('ordering', '-created_at')
        
        # Validar que el campo de ordenamiento sea permitido
        # Remover el prefijo '-' si existe para validar
        ordering_field = ordering.lstrip('-')
        
        if ordering_field in self.ORDERING_FIELDS:
            queryset = queryset.order_by(ordering)
        else:
            # Si el campo no es válido, usar orden por defecto
            queryset = queryset.order_by('-created_at')

        return queryset


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = models.Profile.objects.select_related('user', 'business').all()
    serializer_class = serializers.ProfileSerializer
    # permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.action == 'get_my_profile':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    @action(detail=False, methods=['get'], url_path='me', url_name='me')
    def get_my_profile(self, request):
        """
        Retorna el perfil del usuario autenticado con sus datos de usuario.
        Retorna un objeto único (no un array) con estructura aplanada.
        """
        try:
            # Como es OneToOne, podemos usar get() directamente
            profile = models.Profile.objects.select_related(
                'user', 'business'
            ).get(user=request.user)
            # Usar el serializer aplanado para este endpoint
            serializer = serializers.ProfileMeSerializer(profile)
            # Retornar el objeto directamente, no dentro de un array
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Profile.DoesNotExist:
            return Response(
                {'detail': 'No se encontró un perfil para este usuario.'},
                status=status.HTTP_404_NOT_FOUND
            )
