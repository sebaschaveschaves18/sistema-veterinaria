from django.urls import path
from . import views

urlpatterns = [
    path('clinica/', views.inicio, name='inicio'),

    path('clinica/api/propietarios/', views.api_propietarios, name='api_propietarios'),

    path('clinica/api/mascotas/', views.api_mascotas, name='api_mascotas'),
    path('clinica/api/mascotas/<int:pk>/', views.detalle_mascotas, name='detalle_mascota'),

    path('clinica/api/consultas/', views.api_consultas, name='api_consultas'),

    path('clinica/api/perfil/', views.perfil, name='api_perfil'),
    path('clinica/api/estadisticas/', views.estadisticas, name='api_estadisticas'),
    path('clinica/api/sesion/', views.sesion, name='api_sesion'),
]
