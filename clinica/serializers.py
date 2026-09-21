from rest_framework import serializers
from .models import Propietario, Mascota, ConsultaVeterinaria


class PropietarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propietario
        fields = '__all__'

    def validate_nombre(self, value):
        nombre_limpio = value.strip()

        if len(nombre_limpio) < 2:
            raise serializers.ValidationError(
                'El nombre debe tener al menos 2 caracteres.'
            )
        return nombre_limpio


class MascotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mascota
        fields = '__all__'

    def validate_peso(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'El peso debe ser mayor que cero.'
            )
        return value

    def validate_nombre(self, value):
        nombre_limpio = value.strip()

        if len(nombre_limpio) == 0:
            raise serializers.ValidationError(
                'El nombre de la mascota es obligatorio.'
            )
        return nombre_limpio


class ConsultaVeterinariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultaVeterinaria
        fields = '__all__'

    def validate_costo(self, value):
        if value < 0:
            raise serializers.ValidationError(
                'El costo no puede ser negativo.'
            )
        return value

    def validate_motivo(self, value):
        motivo_limpio = value.strip()

        if len(motivo_limpio) == 0:
            raise serializers.ValidationError(
                'El motivo de la consulta es obligatorio.'
            )
        return motivo_limpio
