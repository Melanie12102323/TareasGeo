TareasGeo – API REST de gestión de proyectos y tareas

API construida con Django y Django REST Framework para gestionar usuarios, equipos, proyectos, tareas, subtareas, etiquetas, comentarios, registros de tiempo, adjuntos y notificaciones.

Requisitos
Python 3.10 o superior
Git
Ejecutar el proyecto localmente (Windows CMD)

git clone <URL-DE-TU-REPOSITORIO>
cd TareasGeo
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Uso
Abre http://127.0.0.1:8000/api-auth/login/ e inicia sesión con el superusuario.
Entra a http://127.0.0.1:8000/api/ (índice de la API).
Panel de administración: http://127.0.0.1:8000/admin/.

Endpoints
Base: http://127.0.0.1:8000/api/
Autenticación

Todos los endpoints requieren sesión iniciada. En Postman usa Basic Auth con las credenciales del superusuario.

Notas
La contraseña de los usuarios se envía en el campo password_hash; la API la guarda hasheada y nunca la devuelve en las respuestas.
Orden sugerido para crear datos de prueba: users → teams → projects → tags → tasks → subtasks, comments, time-logs, attachments, notifications, team-members.
