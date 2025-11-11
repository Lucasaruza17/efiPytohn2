from .base_repository import BaseRepository
from models import Post
from datetime import datetime, timedelta
from extensions import db

class PostRepository(BaseRepository):
    model = Post

    def get_by_user_id(self, user_id):
        return Post.query.filter_by(usuario_id=user_id).all()
        
    def get_all_active(self):
        return Post.query.filter_by(is_published=True).order_by(Post.fecha_creacion.desc()).all()

    def count_posts_last_week(self):
        one_week_ago = datetime.utcnow() - timedelta(days=7)
        return Post.query.filter(Post.fecha_creacion >= one_week_ago).count()