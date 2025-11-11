from flask.views import MethodView
from flask import jsonify, request
from services.comentario_service import ComentarioService
from schemas import ComentarioSchema
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

comentario_schema = ComentarioSchema()
comentarios_schema = ComentarioSchema(many=True)


class ComentarioAPI(MethodView):
    @jwt_required(optional=True)
    def get(self, post_id):
        comentarios = ComentarioService.repo.get_by_post_id(post_id)
        return jsonify(comentarios_schema.dump(comentarios))

    @jwt_required()
    def post(self, post_id):
        data = request.get_json()
        current_user_id = get_jwt_identity() # Obtenemo el id del token
        
        texto = data.get("texto")
        
        #usa el id del token
        nuevo_comentario = ComentarioService.crear_comentario(texto, current_user_id, post_id)
        return jsonify(comentario_schema.dump(nuevo_comentario)), 201

    @jwt_required()
    def delete(self, comment_id):
        comentario = ComentarioService.repo.get_by_id(comment_id)
        if not comentario:
            return jsonify({"msg": "Comentario no encontrado"}), 404
            
        claims = get_jwt()
        current_user_id = claims.get("sub")
        current_user_role = claims.get("role")
        
        # Permite al admin, al moderador, o al autor del comentario
        allowed = ["admin", "moderator"]
        if current_user_role not in allowed and comentario.usuario_id != current_user_id:
            return jsonify({"msg": "Permiso denegado"}), 403
            
        ComentarioService.eliminar_comentario(comentario)
        return jsonify({"msg": "Comentario eliminado"})