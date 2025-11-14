from marshmallow import Schema, fields
from models import User, UserCredentials, Post, Comentario, Categoria


#User
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    is_active = fields.Bool()
    created_at = fields.DateTime()
    posts = fields.Nested("PostSchema", many=True, exclude=("usuario",))

#Credencial
class UserCredentialsSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    password_hash = fields.Str(load_only=True)


# Categoria
class CategoriaSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)


#Posteo
class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    category_id = fields.Int(required=True)
    subject = fields.Str(required=True)
    titulo = fields.Str(required=True)
    contenido = fields.Str(required=True)
    created_at = fields.DateTime()
    is_active = fields.Bool()
    usuario_id = fields.Int()
    usuario = fields.Nested(UserSchema, only=("id", "username", "email"))
    categorias = fields.Nested(CategoriaSchema, many=True)
    comentarios = fields.Nested("ComentarioSchema", many=True, exclude=("post",))


#Comentario
class ComentarioSchema(Schema):
    id = fields.Int(dump_only=True)
    texto = fields.Str(required=True)
    created_at = fields.DateTime()
    usuario_id = fields.Int()
    post_id = fields.Int()
    usuario = fields.Nested(UserSchema, only=("id", "username"))
    post = fields.Nested(PostSchema, only=("id", "titulo"))
