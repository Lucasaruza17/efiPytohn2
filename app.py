# Mateo Gonzalez y Lucas Aruza
from flask import Flask
from extensions import db, migrate, jwt
from datetime import timedelta
#Importama solo las rutas API
from views.api_routes import register_api_routes


#nnicia Flask
app = Flask(__name__)
app.secret_key = "clavesecretaxd"

# Configuración db
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/efipythonMyL"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configuración JWT
app.config["JWT_SECRET_KEY"] = "clavesecretaxd"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

# Conecta las extensiones
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)


#Importaciones de models, servicie y etc 
from models import User, UserCredentials, Post, Comentario, Categoria
from services import PostService, ComentarioService, CategoriaService, UserService
from repositories import UserRepository, PostRepository, ComentarioRepository, CategoriaRepository
from schemas import UserSchema, PostSchema, ComentarioSchema, CategoriaSchema
from views import PostAPI, ComentarioAPI, CategoriaAPI, UserAPI
from decorators import roles_required





#registra solo las rutas de la API
register_api_routes(app)

if __name__ == "__main__":
    app.run(debug=True)