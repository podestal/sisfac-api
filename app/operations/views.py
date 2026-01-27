from rest_framework import viewsets
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
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = models.Profile.objects.select_related('user', 'business').all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

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
