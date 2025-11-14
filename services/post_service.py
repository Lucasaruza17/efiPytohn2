from extensions import db
from models import Post, Categoria

class PostService:
   @staticmethod
   def crear_post(subject, titulo, contenido, user_id, categorias=None):
    # Importa Categoria aquí si no está importado al inicio del archivo
    from models import Categoria, Post
    from extensions import db

    # --- LÍNEA MODIFICADA (Añadimos 'subject=subject') ---
    nuevo_post = Post(subject=subject, titulo=titulo, contenido=contenido, usuario_id=user_id)

    if categorias:
        # Asegurarnos de que las categorías son objetos Categoria, no solo strings
        categorias_obj = Categoria.query.filter(Categoria.nombre.in_(categorias)).all()
        nuevo_post.categorias.extend(categorias_obj)

    db.session.add(nuevo_post)
    db.session.commit()
    return nuevo_post


