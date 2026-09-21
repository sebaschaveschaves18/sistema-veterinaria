from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Propietario, Mascota, ConsultaVeterinaria

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import (
    PropietarioSerializer,
    MascotaSerializer,
    ConsultaVeterinariaSerializer,
)


# Endpoint inicial
@api_view(['GET'])
def inicio(request):
    return HttpResponse('API de Gestión Veterinaria activa')


# ------------------------------------------------------------------
# Endpoint protegido
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def perfil(request):
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
    })


# ------------------------------------------------------------------
# Endpoint reservado para administrador
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def estadisticas(request):
    return Response({
        'total_propietarios': Propietario.objects.count(),
        'total_mascotas': Mascota.objects.count(),
        'mascotas_activas': Mascota.objects.filter(activo=True).count(),
        'total_consultas': ConsultaVeterinaria.objects.count(),
    })


# ------------------------------------------------------------------
# API Propietarios
@api_view(['GET', 'POST'])
def api_propietarios(request):
    if request.method == 'GET':
        propietarios = Propietario.objects.all().order_by('id')
        serializer = PropietarioSerializer(propietarios, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PropietarioSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ------------------------------------------------------------------
# API Mascotas
@api_view(['GET', 'POST'])
def api_mascotas(request):
    if request.method == 'GET':
        mascotas = Mascota.objects.all().order_by('id')

        especie = request.GET.get('especie')
        activas = request.GET.get('activas')
        propietario = request.GET.get('propietario')

        if especie:
            mascotas = mascotas.filter(especie__iexact=especie)

        if activas:
            valor_activo = activas.lower() == 'true'
            mascotas = mascotas.filter(activo=valor_activo)

        if propietario:
            mascotas = mascotas.filter(propietario_id=propietario)

        paginator = Paginator(mascotas, 5)
        pagina = request.GET.get('page', 1)
        page_obj = paginator.get_page(pagina)

        serializer = MascotaSerializer(page_obj.object_list, many=True)

        return Response({
            'pagina_actual': page_obj.number,
            'total_paginas': paginator.num_pages,
            'total_mascotas': paginator.count,
            'resultados': serializer.data,
        })

    if request.method == 'POST':
        serializer = MascotaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ------------------------------------------------------------------
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def detalle_mascotas(request, pk):
    try:
        mascota = Mascota.objects.get(pk=pk)
    except Mascota.DoesNotExist:
        return Response(
            {'error': 'Mascota no encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = MascotaSerializer(mascota)
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:
        serializer = MascotaSerializer(
            mascota,
            data=request.data,
            partial=(request.method == 'PATCH')
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    if request.method == 'DELETE':
        mascota.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ------------------------------------------------------------------
# API Consultas
@api_view(['GET', 'POST'])
def api_consultas(request):
    if request.method == 'GET':
        consultas = ConsultaVeterinaria.objects.all().order_by('id')
        serializer = ConsultaVeterinariaSerializer(consultas, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ConsultaVeterinariaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ------------------------------------------------------------------
# Sesiones
@api_view(['GET'])
def sesion(request):
    contador = request.session.get('contador_accesos', 0)
    contador += 1
    request.session['contador_accesos'] = contador

    return Response({
        'contador_accesos': contador
    })
