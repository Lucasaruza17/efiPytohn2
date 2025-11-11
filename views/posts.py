from flask.views import MethodView
from flask import jsonify, request
from services.post_service import PostService
from schemas import PostSchema
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

post_schema = PostSchema()
posts_schema = PostSchema(many=True)


class PostAPI(MethodView):
    
    @jwt_required(optional=True)
    def get(self, post_id):
        if post_id:
            post = PostService.repo.get_by_id(post_id)
            if not post or not post.is_published:
                return jsonify({"msg": "Post no encontrado"}), 404
            return jsonify(post_schema.dump(post))
        
        posts = PostService.repo.get_all_active() 
        return jsonify(posts_schema.dump(posts))

    @jwt_required()
    def post(self, post_id=None):
        data = request.get_json()
        current_user_id = get_jwt_identity() #obtenemo el id del token
        
        titulo = data.get("titulo")
        contenido = data.get("contenido")
        categorias = data.get("categorias", [])
        
        #se usa el id del token
        nuevo_post = PostService.crear_post(titulo, contenido, current_user_id, categorias)
        return jsonify(post_schema.dump(nuevo_post)), 201

    @jwt_required()
    def put(self, post_id):
        data = request.get_json()
        post = PostService.repo.get_by_id(post_id)
        if not post:
            return jsonify({"msg": "Post no encontrado"}), 404
            
        claims = get_jwt()
        current_user_id = claims.get("sub")
        current_user_role = claims.get("role")

        if current_user_role != 'admin' and post.usuario_id != current_user_id:
            return jsonify({"msg": "Permiso denegado"}), 403
            
        titulo = data.get("titulo")
        contenido = data.get("contenido")
        categorias = data.get("categorias", [])
        
    
        actualizado = PostService.editar_post(post, titulo, contenido, categorias)
        return jsonify(post_schema.dump(actualizado))

    @jwt_required()
    def delete(self, post_id):
        post = PostService.repo.get_by_id(post_id)
        if not post:
            return jsonify({"msg": "Post no encontrado"}), 404

        
        claims = get_jwt()
        current_user_id = claims.get("sub")
        current_user_role = claims.get("role")

        if current_user_role != 'admin' and post.usuario_id != current_user_id:
            return jsonify({"msg": "Permiso denegado"}), 403
    
        PostService.eliminar_post(post)
        return jsonify({"msg": "Post eliminado"})