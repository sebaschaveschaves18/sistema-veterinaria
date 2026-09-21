# Sistema de Gestión Veterinaria

Proyecto realizado con Django y Django REST Framework.

## Instalación

Crear el entorno virtual:

python -m venv .venv

Activarlo:

.\.venv\Scripts\activate

Instalar Django:

python -m pip install "Django>=5.2,<5.3"

Instalar Django REST Framework:

pip install djangorestframework

## Base de datos

python manage.py makemigrations

python manage.py migrate

Crear administrador:

python manage.py createsuperuser

## Ejecutar

python manage.py runserver

Página:

http://127.0.0.1:8000/

Admin:

http://127.0.0.1:8000/admin/

## API

Propietarios:

/clinica/api/propietarios/

Mascotas:

/clinica/api/mascotas/

Consultas:

/clinica/api/consultas/

Perfil:

/clinica/api/perfil/

Estadísticas:

/clinica/api/estadisticas/

Sesión:

/clinica/api/sesion/

## Pruebas

python manage.py test

Las pruebas también se realizaron con Postman.

## GitHub

Rama:

feature/sistema-veterinaria

Repositorio:

https://github.com/sebaschaveschaves18/sistema-veterinaria
