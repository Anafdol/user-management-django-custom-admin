from django.urls import path, include
from rest_framework.routers import DefaultRouter
from people.views.person import PersonViewSet, dashboard_view, exportar_pacientes_pdf
from people.views import checkin, home_services, professional_service 

 
router = DefaultRouter()
router.register('people', PersonViewSet)
# Ajuste os nomes abaixo conforme a estrutura real dos seus arquivos de view
# router.register('checkins', checkin.CheckinViewSet)
# router.register('home_services', home_services.HomeServicesViewSet)


urlpatterns = [
  
    path('', include(router.urls)),
    
    path('dashboard/', dashboard_view, name='dashboard_visual'),

    # Rota da Melhoria 1 (Exportação PDF)
    path('exportar-pdf/', exportar_pacientes_pdf, name='exportar_pdf'),
]