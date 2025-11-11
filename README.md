# API REST con Flask - EFI Python (efiPython2)

Repositorio para la **Evaluación Final Integradora (EFI)** de la materia **Programación Python I**, creado por Lucas Aruza y Mateo Gonzalez.

---

## Resumen de funcionalidades

-   ✅ **Arquitectura limpia** (Services + Repositories)
-   ✅ **Autenticación** con Flask-JWT-Extended
-   ✅ **Control de acceso** basado en roles (Admin, Moderator, User)
-   ✅ **CRUDs completos** (Usuarios, Posts, Comentarios, Categorías)
-   ✅ **Eliminado lógico** (desactivación de usuarios)
-   ✅ **Endpoint de estadísticas** (`/api/stats`)
-   ✅ **Protección de rutas** según rol (Decoradores personalizados)
-   ✅ **Código modular**, escalable y mantenible

---

## Estructura del proyecto
¡Claro! Ese README.md de las imágenes es excelente.

Basándome en todo lo que hemos construido en tu proyecto (efiPytohn2), he creado esta versión del README.md que replica ese estilo profesional, pero adaptado 100% a tu código, tus nombres de archivo y tus endpoints.

Simplemente copia todo el bloque de código de abajo y pégalo en el archivo README.md de tu repositorio de GitHub.
Markdown

# API REST con Flask - EFI Python (efiPython2)

Repositorio para la **Evaluación Final Integradora (EFI)** de la materia **Programación Python I**, creado por Lucas Aruza y Mateo Gonzalez.

---

## Resumen de funcionalidades

-    ✅ **Arquitectura limpia** (Services + Repositories)
-    ✅ **Autenticación** con Flask-JWT-Extended
-    ✅ **Control de acceso** basado en roles (Admin, Moderator, User)
-    ✅ **CRUDs completos** (Usuarios, Posts, Comentarios, Categorías)
-    ✅ **Eliminado lógico** (desactivación de usuarios)
-    ✅ **Endpoint de estadísticas** (`/api/stats`)
-    ✅ **Protección de rutas** según rol (Decoradores personalizados)
-    ✅ **Código modular**, escalable y mantenible

---

## Estructura del proyecto

```
/EfiPython
  ├── /decorators
  ├── /migrations
  ├── /repositories
  ├── /schemas
  ├── /services
  ├── /views
  ├── app.py
  ├── extensions.py
  ├── models.py
  └── requirements.txt
```

- **models/** → Modelos de SQLAlchemy
- **schemas/** → Validaciones y serialización con Marshmallow
- **repositories/** → Acceso a datos (consultas directas a la base de datos)
- **services/** → Logica de negocio
- **views/** → Endpoints (MethodView) y registro de rutas
- **decorators/** → Decoradores personalizados

---
## Configuración e instalación (paso a paso)

### 1️⃣ Clonar el repositorio

```bash
git clone [https://github.com/Lucasaruza17/efiPython2.git](https://github.com/Lucasaruza17/efiPython2.git)
cd efiPython2
```
---

2️⃣ Crear y activar un entorno virtual

```bash
# En Linux/macOS
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
.\venv\Scripts\activate
```
---

3️⃣ Instalar dependencias


```bash
pip install -r requirements.txt
```
---

### Configuración de la base de datos (MySQL con XAMPP y phpMyAdmin)

1. **Instalar y abrir XAMPP**
   
   - Descargá e instalá **XAMPP** desde [https://www.apachefriends.org/es/index.html](https://www.apachefriends.org/es/index.html)
   - Iniciá los servicios de **Apache** y **MySQL** desde el panel de control o ejecuta en la consola:
     
     ```
     sudo /opt/lampp/lampp start
     ```
2. **Acceder a phpMyAdmin**
   
   - Abrí tu navegador y entrá a [http://localhost/phpmyadmin](http://localhost/phpmyadmin)
   - Creá una nueva base de datos llamada, por ejemplo:
     ```
     efipythonMyL
     ```
3. **Configurar la conexión en Flask**
   
   - En el archivo `app.py`, asegurate de tener configurada la URI de conexión como:
     
     ```python
     app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/efipythonMyL"
     ```
     
     🔹 *Nota:*- Si tu usuario MySQL tiene contraseña, agregala después de `root:`
     (por ejemplo, `"mysql+pymysql://root:tu_contraseña@localhost/efipythonMyL"`)- El nombre `efipythonMyL` debe coincidir exactamente con el de tu base creada en phpMyAdmin.
4. **Crear las tablas**
   
   - Desde la terminal, ubicándote en el directorio raíz del proyecto, ejecutá:
     ```bash
     flask db init
     flask db migrate -m "Migración inicial"
     # Si la carpeta 'migrations' ya existe (como en el repo):
     flask db upgrade
     ```
   - Esto creará automáticamente las tablas en tu base de datos.
5. **Verificar en phpMyAdmin**
   
   - Volvé a [http://localhost/phpmyadmin](http://localhost/phpmyadmin)
   - Ingresá a tu base `efipythonMyL` y comprobá que se hayan creado las tablas (`user`, `post`, `comentario`, `categoria`, etc.)

---

### 4️⃣ Ejecutar la aplicación

```bash
flask run
```

Por defecto se ejecutará en (http://127.0.0.1:5000)

---
Tecnologías utilizadas

   - **Flask** (Framework principal)

   - **Flask-JWT-Extended** (Autenticación JWT)

   - **Flask-SQLAlchemy** (ORM)

   - **Flask-Migrate** (Migraciones)

   - **Marshmallow** (Serialización y validación)

   - **PyMySQL** (Conector MySQL)

   - **Werkzeug** (Hash de contraseñas)

---
## Endpoints principales

| Recurso           | Método | Ruta           | Descripción                     | Rol requerido         |
| ----------------- | ------- | -------------- | -------------------------------- | --------------------- |
| **Auth**          | POST    | `/api/register`    | Crear usuario                    | Público              |
|                   | POST    | `/api/login`       | Iniciar sesión                  | Público              |
| **Usuarios**      | GET     | `/api/users`    | Listar todos los usuarios                  | Admin                 |
|                   | GET     | `/api/users/<id>`      | Ver usuario por id               | Usuario o Admin       |
|                   | PATCH   | `/api/users/<id>/role` | Cambiar rol                      | Admin                 |
|                   | DELETE  | `/api/users/<id>`      | Desactivar usuario               | Admin                 |
| **Posts**         | GET     | `/api/posts/<id>`       | Listar todos los posts                     | Público              |
|                   | GET     | `/api/posts/<id>`       | Ver un post específico                     | Publico                |
|                   | POST    | `/api/posts`       | Crear post                       | User+                 |
|                   | PUT     | `/api/posts/<id>`      | Editar propio post               | Autor/Admin           |
|                   | DELETE  | `/api/posts/<id>`      | Eliminar post                    | Autor/Admin           |
| **Comentarios**   | GET     | `/comments`    | Listar los comentarios           | Público              |
|                   | POST    | `/comments`    | Crear comentario                 | User+                 |
|                   | DELETE  | `/api/comments/<id>`   | Eliminar comentario              | Autor/Moderador/Admin |
| **Categorías**   | GET     | `/api/categories`  | Listar categorías               | Público              |
|                   | POST    | `/api/categories`  | Crear categoría                 | Moderator/Admin       |
|                   | PUT     | `//api/categories/<id>` | Editar categoría                | Moderator/Admin       |
|                   | DELETE  | `/api/categories/<id>` | Eliminar categoría              | Admin                 |
| **Estadísticas** | GET     | `/api/stats`       | Ver estadísticas                | Moderator/Admin       |


---

---

## Roles y permisos

| Acción                            | User | Moderator | Admin |
| ---------------------------------- | ---- | --------- | ----- |
| Ver posts/comentarios             | ✅   | ✅        | ✅    |
| Crear/editar propios posts         | ✅   | ✅        | ✅    |
| Eliminar cualquier comentario      | ❌   | ✅        | ✅    |
| Crear/editar categorías           | ❌   | ✅        | ✅    |
| Eliminar categorías               | ❌   | ❌        | ✅    |
| Cambiar roles / gestionar usuarios | ❌   | ❌        | ✅    |
| Ver estadísticas básicas         | ❌   | ✅        | ✅    |
| Ver estadísticas completas        | ❌   | ❌        | ✅    |

---
## Datos de prueba sugeridos

| Rol       | Email          | Contraseña |
| --------- | -------------- | ----------- |
| Admin     | admin@mail.com | admin1234    |
| Moderador | mod@mail.com   | mod1234      |
| Usuario   | user@mail.com  | user1234     |
Para crear estos usuarios:

1.  **Regístralos** usando `POST /api/register` (con Thunder Client).
    * `{"username": "admin_user", "email": "admin@mail.com", "password": "admin1234"}`
    * `{"username": "mod_user", "email": "mod@mail.com", "password": "mod1234"}`
    * `{"username": "user_user", "email": "user@mail.com", "password": "user1234"}`

2.  **Asigna los roles en MySQL:**
    Por defecto, todos se crearán como "user". Conéctate a tu base de datos y ejecuta los siguientes comandos SQL para actualizar sus roles:

    ```sql
    USE efipythonMyL;
    UPDATE user SET role = 'admin' WHERE email = 'admin@mail.com';
    UPDATE user SET role = 'moderator' WHERE email = 'mod@mail.com';
    ```

## Ejemplos de peticiones (Body)

### Registro de usuario

**POST**`/api/register`

```json
{
  "username": "admin1",
  "email": "admin@example.com",
  "password": "admin1234"
}
```
---

### Login de usuario

**POST**`/api/login`

```json
{
  "email": "admin@example.com",
  "password": "admin1234"
}
```

>  Respuesta:

```json
{
  "access_token": "<token_jwt>"
}
```

---

### Crear un post (Requiere Token)

**POST**`/api/posts`

```json
{
    "titulo": "Mi primer post sobre Flask",
    "contenido": "Este post fue creado usando la API."
}
```

---

### Modificar rol de usuario

**PATCH**`/api/users/2/role`

```json
{
  "role": "moderator"
}
```

---

### Actualizar post

**PUT**`/api/posts/1`

```json
{
    "titulo": "Post actualizado",
    "contenido": "Contenido actualizado."
}
```

---

#### Autores:

* Lucas Aruza- l.aruza@itecriocuarto.org.ar
* Mateo Gonzalez - mateo.gonzalez@itecriocuarto.org.ar
