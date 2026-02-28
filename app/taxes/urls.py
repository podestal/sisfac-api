from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'document-types', views.DocumentTypeViewSet)
router.register(r'business-sunat-configs', views.BusinessSunatConfigViewSet)
router.register(r'parties', views.PartyViewSet)
router.register(r'sunat-documents', views.SunatDocumentViewSet)
router.register(r'sunat-document-items', views.SunatDocumentItemViewSet)
router.register(r'sunat-submissions', views.SunatSubmissionViewSet)

urlpatterns = router.urls