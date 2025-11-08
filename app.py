# Mateo Gonzalez y Lucas Aruza
from flask import Flask, flash, render_template, request, redirect, url_for, abort, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from datetime import timedelta
from functools import wraps

# Importamos vistas REST
from views import PostAPI, ComentarioAPI, CategoriaAPI, UserAPI

# Importamos servicios y repositorios
from services import PostService, ComentarioService, CategoriaService, UserService
from repositories import UserRepository, PostRepository, ComentarioRepository, CategoriaRepository
from schemas import UserSchema, PostSchema, ComentarioSchema, CategoriaSchema

# Iniciamos Flask
app = Flask(__name__)
app.secret_key = "clavesecretaxd"

# Configuración DB
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/efipythonMyL"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configuración JWT
app.config["JWT_SECRET_KEY"] = "clavesecretaxd"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

# Inicializamos extensiones
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Importamos modelos
from models import User, UserCredentials, Post, Comentario, Categoria

# Login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_categorias():
    return dict(categorias=Categoria.query.all())

# Decorador de roles
def roles_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") not in roles:
                return jsonify({"msg": "Permiso denegado"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


# Registro
@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    user_repo = UserRepository()
    if user_repo.get_by_username_or_email(username, email):
        return jsonify({"msg":"Usuario o email ya existe"}), 400

    nuevo_usuario = UserService.crear_usuario(username, email, password)
    return jsonify({"message":"Usuario creado","user_id":nuevo_usuario.id}), 201

# Login
@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    usuario = UserRepository().get_by_email(email)
    if not usuario or not usuario.credentials.check_password(password):
        return jsonify({"msg":"Credenciales incorrectas"}), 401

    access_token = create_access_token(identity=usuario.id, additional_claims={
        "email": usuario.email,
        "role": usuario.role
    })
    return jsonify({"access_token": access_token}), 200


@app.route("/")
def index():
    posts = PostRepository().get_all_active()
    return render_template("index.html", posts=posts)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        if UserRepository().get_by_username_or_email(username, email):
            flash("Usuario o email ya existe","error")
            return redirect(url_for("register"))
        UserService.crear_usuario(username, email, password)
        flash("Registro exitoso. Ahora puedes iniciar sesión.","success")
        return redirect(url_for("login"))
    return render_template("auth/register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        usuario = UserRepository().get_by_username(username)
        if usuario and usuario.credentials.check_password(password):
            login_user(usuario)
            flash("Sesión iniciada","success")
            return redirect(url_for("index"))
        flash("Usuario o contraseña incorrectos","error")
    return render_template("auth/login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada","success")
    return redirect(url_for("index"))


@app.route("/post/new", methods=["GET","POST"])
@login_required
def new_post():
    if request.method=="POST":
        titulo = request.form["titulo"]
        contenido = request.form["contenido"]
        categorias_ids = request.form.getlist("categorias_seleccionadas")
        categorias = CategoriaRepository().get_by_ids(categorias_ids) if categorias_ids else None
        PostService.crear_post(titulo, contenido, current_user.id, categorias)
        flash("Post creado correctamente","success")
        return redirect(url_for("index"))
    return render_template("new_post.html")

@app.route("/post/<int:post_id>", methods=["GET","POST"])
def post_detail(post_id):
    post = PostRepository().get_by_id(post_id)
    if not post:
        abort(404)
    if request.method=="POST" and current_user.is_authenticated:
        texto = request.form["texto"]
        ComentarioService.crear_comentario(texto, current_user.id, post.id)
        flash("Comentario agregado","success")
        return redirect(url_for("post_detail", post_id=post.id))
    return render_template("post_detail.html", post=post)

@app.route("/post/edit/<int:post_id>", methods=["GET","POST"])
@login_required
def edit_post(post_id):
    post = PostRepository().get_by_id(post_id)
    if post.usuario_id != current_user.id and current_user.role != "admin":
        abort(403)
    if request.method=="POST":
        titulo = request.form["titulo"]
        contenido = request.form["contenido"]
        categorias_ids = request.form.getlist("categorias_seleccionadas")
        categorias = CategoriaRepository().get_by_ids(categorias_ids) if categorias_ids else None
        PostService.editar_post(post, titulo, contenido, categorias, user_role=current_user.role, user_id=current_user.id)
        flash("Post actualizado correctamente","success")
        return redirect(url_for("post_detail", post_id=post.id))
    return render_template("edit_post.html", post=post)

@app.route("/post/delete/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    post = PostRepository().get_by_id(post_id)
    if post.usuario_id != current_user.id and current_user.role != "admin":
        abort(403)
    PostService.eliminar_post(post, user_role=current_user.role, user_id=current_user.id)
    flash("Post eliminado correctamente","success")
    return redirect(url_for("index"))

@app.route("/comment/delete/<int:comment_id>", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = ComentarioRepository().get_by_id(comment_id)
    post_id = comment.post_id
    if current_user.id != comment.usuario_id and current_user.id != comment.post.usuario_id and current_user.role not in ["moderator","admin"]:
        abort(403)
    ComentarioService.eliminar_comentario(comment, user_role=current_user.role, user_id=current_user.id)
    flash("Comentario eliminado","success")
    return redirect(url_for("post_detail", post_id=post_id))

# Posts
post_view = PostAPI.as_view("posts_api")
app.add_url_rule("/api/posts", defaults={"post_id": None}, view_func=post_view, methods=["GET","POST"])
app.add_url_rule("/api/posts/<int:post_id>", view_func=post_view, methods=["GET","PUT","DELETE"])

# Comentario
comentario_view = ComentarioAPI.as_view("comentarios_api")
app.add_url_rule("/api/posts/<int:post_id>/comments", view_func=comentario_view, methods=["GET","POST"])
app.add_url_rule("/api/comments/<int:comment_id>", view_func=comentario_view, methods=["DELETE"])

# Categoria
categoria_view = CategoriaAPI.as_view("categorias_api")
app.add_url_rule("/api/categories", defaults={"categoria_id": None}, view_func=categoria_view, methods=["GET","POST"])
app.add_url_rule("/api/categories/<int:categoria_id>", view_func=categoria_view, methods=["GET","PUT","DELETE"])

# Usuarios/Admin
user_view = UserAPI.as_view("users_api")
app.add_url_rule("/api/users", defaults={"user_id": None}, view_func=user_view, methods=["GET"])
app.add_url_rule("/api/users/<int:user_id>", view_func=user_view, methods=["GET","DELETE"])
app.add_url_rule("/api/users/<int:user_id>/role", view_func=user_view, methods=["PATCH"])


if __name__ == "__main__":
    app.run(debug=True)
