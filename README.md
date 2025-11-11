# API REST con Flask - EFI Python (Proyecto efiPytohn2)

Repositorio para la Evaluación Final Integradora de la materia Programación Python II.

## Resumen de funcionalidades

-   [x] **Arquitectura limpia** (Services + Repositories)
-   [x] **Autenticación** con Flask-JWT-Extended
-   [x] **Control de acceso** basado en roles (Admin, Moderator, User)
-   [x] **CRUDs completos** (Usuarios, Posts, Comentarios, Categorías)
-   [x] **Eliminado lógico** (desactivación de usuarios)
-   [x] **Endpoint de estadísticas** (`/api/stats`)
-   [x] **Protección de rutas** según rol (Decoradores personalizados)
-   [x] **Código modular**, escalable y mantenible

## Estructura del proyecto

/efiPytohn2 ├── app.py # Configuración principal y registro de rutas ├── extensions.py # Instancias de extensiones (db, migrate, jwt) ├── requirements.txt # Dependencias del proyecto ├── models.py # Modelos de SQLAlchemy (Tablas) ├── /decorators # Decoradores personalizados (ej. @roles_required) ├── /repositories # Lógica de acceso a datos (Queries a la DB) ├── /services # Lógica de negocio (orquestación) ├── /schemas # Schemas de Marshmallow (Serialización) ├── /views # Endpoints (MethodView) y registro de rutas └── /migrations # Migraciones de Alembic

* **models.py**: Define los modelos de SQLAlchemy.
* **schemas/**: Define los schemas de Marshmallow para validación y serialización.
* **repositories/**: Clases que manejan las consultas directas a la base de datos (Ej: `PostRepository`).
* **services/**: Clases que contienen la lógica de negocio (Ej: `PostService`).
* **views/**: Define los endpoints de la API (con `MethodView`) y registra las rutas.
* **decorators/**: Decoradores personalizados para verificar roles.

## Configuración e instalación (paso a paso)

### 1. Clonar el repositorio
```bash
git clone [https://github.com/Lucasaruza17/efiPytohn2.git](https://github.com/Lucasaruza17/efiPytohn2.git)
cd efiPytohn2

2. Crear y activar un entorno virtual

Bash

# En Linux/macOS
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
.\venv\Scripts\activate

3. Instalar dependencias

Bash

pip install -r requirements.txt

4. Configuración de la base de datos (MySQL)

    Crear la base de datos: Asegúrate de tener un servidor MySQL corriendo. Accede y crea una nueva base de datos llamada efipythonMyL (es el nombre que está en app.py).
    SQL

CREATE DATABASE efipythonMyL;

Configurar la conexión en Flask: El archivo app.py ya está configurado para conectarse a mysql+pymysql://root:@localhost/efipythonMyL. Si tu usuario root de MySQL tiene contraseña, ajústalo: "mysql+pymysql://root:TU_CONTRASEÑA@localhost/efipythonMyL"

Crear las tablas: El proyecto ya incluye la carpeta migrations. Solo necesitas ejecutar la migración:
Bash

    flask db upgrade

    Esto creará todas las tablas (user, post, comentario, etc.) en tu base de datos.

5. Ejecutar la aplicación

Bash

flask run

Por defecto, la API se ejecutará en http://127.0.0.1:5000.

Tecnologías utilizadas

    Flask (Framework principal)

    Flask-JWT-Extended (Autenticación JWT)

    Flask-SQLAlchemy (ORM)

    Flask-Migrate (Migraciones de base de datos)

    Marshmallow (Serialización y validación)

    PyMySQL (Conector de MySQL)

    Werkzeug (Hash de contraseñas)

Endpoints principales

Recurso	Método	Ruta	Descripción	Rol requerido
Auth	POST	/api/register	Registrar un nuevo usuario	Público
	POST	/api/login	Iniciar sesión (obtener token)	Público
				
Usuarios	GET	/api/users	Listar todos los usuarios	Admin
	GET	/api/users/<id>	Ver un usuario por id	Admin o Usuario (dueño)
	PATCH	/api/users/<id>/role	Cambiar rol de un usuario	Admin
	DELETE	/api/users/<id>	Desactivar un usuario (Borrado lógico)	Admin
				
Posts	GET	/api/posts	Listar todos los posts públicos	Público
	GET	/api/posts/<id>	Ver un post específico	Público
	POST	/api/posts	Crear un nuevo post	User+
	PUT	/api/posts/<id>	Editar un post	Autor o Admin
	DELETE	/api/posts/<id>	Eliminar un post	Autor o Admin
				
Comentarios	GET	/api/posts/<id>/comments	Listar comentarios de un post	Público
	POST	/api/posts/<id>/comments	Crear un comentario	User+
	DELETE	/api/comments/<id>	Eliminar un comentario	Autor, Moderator o Admin
				
Categorías	GET	/api/categories	Listar categorías	Público
	POST	/api/categories	Crear una categoría	Moderator o Admin
	PUT	/api/categories/<id>	Editar una categoría	Moderator o Admin
	DELETE	/api/categories/<id>	Eliminar una categoría	Admin
				
Estadíst.	GET	/api/stats	Ver estadísticas del sitio	Moderator o Admin

Roles y permisos

Acción	User	Moderator	Admin
Ver posts/comentarios	✅	✅	✅
Crear/editar propios posts	✅	✅	✅
Eliminar cualquier comentario	❌	✅	✅
Crear/editar categorías	❌	✅	✅
Eliminar categorías	❌	❌	✅
Cambiar roles / gestionar usuarios	❌	❌	✅
Ver estadísticas básicas	❌	✅	✅
Ver estadísticas completas (admin)	❌	❌	✅

Datos de prueba sugeridos

Para probar la API con diferentes roles, sigue estos pasos:

    Registra 3 usuarios usando el endpoint POST /api/register (puedes usar Thunder Client):

        {"username": "admin_user", "email": "admin@mail.com", "password": "admin123"}

        {"username": "mod_user", "email": "mod@mail.com", "password": "mod123"}

        {"username": "user_user", "email": "user@mail.com", "password": "user123"}

    Asigna los roles en MySQL: Por defecto, todos se crearán como "user". Conéctate a tu base de datos y ejecuta los siguientes comandos SQL para actualizar sus roles:
    SQL

    USE efipythonMyL;
    UPDATE user SET role = 'admin' WHERE email = 'admin@mail.com';
    UPDATE user SET role = 'moderator' WHERE email = 'mod@mail.com';

    Ahora puedes iniciar sesión con cada uno y obtener tokens con diferentes permisos.

Ejemplos de peticiones (Body)

Registro de usuario

POST /api/register
JSON

{
    "username": "nuevo_usuario",
    "email": "nuevo@example.com",
    "password": "pass123"
}

Login de usuario

POST /api/login
JSON

{
    "email": "nuevo@example.com",
    "password": "pass123"
}

Respuesta:
JSON

{
    "access_token": "eyJ0eXAiOiJKV1QiLCJh..."
}

Crear un comentario (Requiere Token)

POST /api/posts/1/comments
JSON

{
    "texto": "¡Excelente artículo, muy útil!"
}

Modificar rol de usuario (Solo Admin)

PATCH /api/users/3/role
JSON

{
    "role": "moderator"
}

Actualizar post (Autor o Admin)

PUT /api/posts/1
JSON

{
    "titulo": "Post actualizado sobre Flask",
    "contenido": "Ahora incluye JWT, Marshmallow y migraciones con Alembic."
}
