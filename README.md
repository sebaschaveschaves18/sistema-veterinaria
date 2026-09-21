# Sistema de Gestión Veterinaria

Proyecto de Django y Django REST Framework para la práctica guiada integradora.

## 1. Instalación

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install "Django>=5.2,<5.3"
pip install djangorestframework
```

También se puede instalar desde `requirements.txt`:

```powershell
pip install -r requirements.txt
```

## 2. Migraciones

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata datos_iniciales.json
```

## 3. Superusuario

```powershell
python manage.py createsuperuser
```

Para trabajar con la sección de usuarios de la práctica, cree también un usuario regular desde el administrador y genere tokens para los usuarios necesarios.

## 4. Ejecutar el servidor

```powershell
python manage.py runserver
```

Ruta inicial:

`GET /clinica/`

Respuesta:

`API de Gestión Veterinaria activa`

## 5. ORM solicitado

Desde la consola:

```powershell
python manage.py shell
```

Consultas de práctica:

```python
from clinica.models import Propietario, Mascota, ConsultaVeterinaria

Mascota.objects.all()
Mascota.objects.all().order_by('nombre')
Mascota.objects.filter(activo=True)
Mascota.objects.filter(peso__gt=10)
Mascota.objects.filter(especie__iexact='Perro')
Propietario.objects.filter(nombre__icontains='Juan')
propietario = Propietario.objects.get(id=1)
propietario.mascotas.all()
mascota = Mascota.objects.get(id=1)
mascota.peso = 15
mascota.save()
consulta = ConsultaVeterinaria.objects.last()
consulta.delete()
```

`peso__gt=10` significa que el campo `peso` debe ser mayor que 10. El doble guion bajo se utiliza para indicar un lookup del ORM, en este caso `gt` de greater than.

## 6. Endpoints

| Método | URL | Descripción | Parámetros/Body | Respuesta | Códigos |
|---|---|---|---|---|---|
| GET | `/clinica/api/mascotas/` | Listar mascotas | `page`, `especie`, `activas`, `propietario` | Lista paginada | 200 |
| POST | `/clinica/api/mascotas/` | Registrar mascota | Datos de mascota | Mascota creada | 201 / 400 |
| GET | `/clinica/api/mascotas/<id>/` | Detalle | ID | Mascota | 200 / 404 |
| PUT/PATCH | `/clinica/api/mascotas/<id>/` | Actualizar | Datos de mascota | Mascota actualizada | 200 / 400 / 404 |
| DELETE | `/clinica/api/mascotas/<id>/` | Eliminar | ID | Sin contenido | 204 / 404 |
| GET | `/clinica/api/propietarios/` | Listar propietarios | Ninguno | Propietarios | 200 |
| POST | `/clinica/api/propietarios/` | Registrar propietario | Datos de propietario | Propietario creado | 201 / 400 |
| GET | `/clinica/api/consultas/` | Listar consultas | Ninguno | Consultas | 200 |
| POST | `/clinica/api/consultas/` | Registrar consulta | Datos de consulta | Consulta creada | 201 / 400 |
| GET | `/clinica/api/perfil/` | Perfil del usuario | Token | Datos del usuario | 200 / 401 |
| GET | `/clinica/api/estadisticas/` | Estadísticas | Token de administrador | Totales | 200 / 403 |
| GET | `/clinica/api/sesion/` | Contador de sesión | Ninguno | Contador | 200 |
| POST | `/api/token/` | Obtener token | `username`, `password` | Token | 200 / 400 |

## 7. Paginación y filtros

El listado de mascotas usa 5 registros por página.

```text
GET /clinica/api/mascotas/?page=1
GET /clinica/api/mascotas/?page=2
GET /clinica/api/mascotas/?especie=Perro
GET /clinica/api/mascotas/?activas=true
GET /clinica/api/mascotas/?propietario=3
```

También se pueden combinar los filtros.

## 8. Autenticación

Primero se obtiene el token:

```text
POST /api/token/
```

Body JSON:

```json
{
    "username": "usuario",
    "password": "clave"
}
```

Después se envía el encabezado:

```text
Authorization: Token <token>
```

`/clinica/api/perfil/` usa `IsAuthenticated` y `/clinica/api/estadisticas/` usa `IsAdminUser`.

## 9. Sesiones

`GET /clinica/api/sesion/` incrementa y devuelve `contador_accesos`. La sesión permite conservar ese valor entre solicitudes del mismo cliente aunque HTTP sea un protocolo sin estado.

## 10. Pruebas

```powershell
python manage.py test
```

Las pruebas incluyen:

- Peso 0 inválido para una mascota.
- Costo negativo inválido para una consulta.
- Perfil rechazado sin autenticación.
- Perfil exitoso con un usuario autenticado.

## 11. Pruebas manuales sugeridas en Postman

1. GET mascotas sin filtros -> 200.
2. POST mascota con datos válidos -> 201.
3. POST mascota con peso 0 -> 400.
4. GET mascota con un ID inexistente -> 404.
5. PATCH mascota cambiando peso -> 200.
6. GET mascotas con `page=2` -> 200 y metadatos.
7. GET mascotas con `especie=Perro` -> solo perros.
8. POST consulta con costo negativo -> 400.
9. GET perfil sin token -> acceso rechazado.
10. GET perfil con token válido -> 200.
11. GET estadísticas con usuario regular -> acceso rechazado.
12. GET estadísticas con administrador -> 200.
13. DELETE mascota con ID válido -> 204.

## 12. Datos iniciales para Administración

El archivo `datos_iniciales.json` incluye 4 propietarios, 8 mascotas y 8 consultas. Después de ejecutar `python manage.py migrate`, puede cargar esos datos con `python manage.py loaddata datos_iniciales.json`. También se pueden crear y revisar desde `/admin/`. Las relaciones deben respetar Propietario -> Mascota -> ConsultaVeterinaria.

## 13. Git

```powershell
git switch -c feature/sistema-veterinaria
git status
git add .
git commit -m "Agrega modelos del sistema veterinario"
git commit -m "Implementa API REST veterinaria"
git commit -m "Agrega autenticacion permisos y pruebas"
git push -u origin feature/sistema-veterinaria
```

No subir `.venv/`, `__pycache__/`, archivos `.pyc`, `.env`, tokens ni credenciales. Las migraciones sí deben versionarse.

## 14. Reflexión final

Postman envía el POST a la URL del endpoint y Django dirige la solicitud a la View. La View recibe los datos y los pasa al Serializer. El Serializer realiza la validación de los campos y, si los datos son correctos, guarda mediante el Model y el ORM. El ORM comunica la operación a la base de datos. Finalmente, la View construye un Response con los datos serializados y el código HTTP correspondiente.
