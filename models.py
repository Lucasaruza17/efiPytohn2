#Mateo Gonzalez y Lucas Aruza 
from extensions import db
from flask_login import UserMixin  # Clase auxiliar para integrar el modelo de usuario con Flask-Login
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Tabla intermedia para la relación muchos-a-muchos entre Posteos y Categorias
post_categorias = db.Table(
    "post_categorias",
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True),
    db.Column("categoria_id", db.Integer, db.ForeignKey("categoria.id"), primary_key=True),
)


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)

    # NUEVOS CAMPOS
    role = db.Column(db.String(20), default="user")  # roles: user, moderator, admin
    is_active = db.Column(db.Boolean, default=True)  # Estado de activación
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con UserCredentials (1 a 1)
    credentials = db.relationship("UserCredentials", backref="user", uselist=False)

    # Relaciones existentes con posts y comentarios
    posts = db.relationship("Post", backref="usuario", lazy=True)
    comentarios = db.relationship("Comentario", backref="usuario", lazy=True)

    def __str__(self):
        return self.username


class UserCredentials(db.Model):
    __tablename__ = "user_credentials"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=True)
    titulo = db.Column(db.String(150), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())
    usuario_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    
    is_published = db.Column(db.Boolean, default=True)  # Publicación visible
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    
    categorias = db.relationship(
        "Categoria",
        secondary=post_categorias,
        lazy="subquery",
        backref=db.backref("posts", lazy=True),
    )

    
    comentarios = db.relationship("Comentario", backref="post", lazy=True)


class Comentario(db.Model):
    __tablename__ = "comentario"

    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())
    usuario_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    
    is_visible = db.Column(db.Boolean, default=True)  # Para moderación

class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    
