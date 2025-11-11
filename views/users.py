from flask.views import MethodView
from flask import jsonify, request
from services.user_service import UserService
from schemas import UserSchema
from flask_jwt_extended import jwt_required, get_jwt
from decorators import roles_required

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserAPI(MethodView):

    @jwt_required()
    def get(self, user_id):
        
        # Logica para GET /api/users para ver todos
        if user_id is None:
            claims = get_jwt()
            if claims.get("role") != "admin":
                return jsonify({"msg": "Permiso denegado"}), 403
                
            users = UserService.repo.get_all()
            return jsonify(users_schema.dump(users))
        
        # Logica para get/api/users/<id> para ver uno
        claims = get_jwt()
        current_user_id = claims.get("sub") 
        
        if claims.get("role") != "admin" and current_user_id != user_id:
             return jsonify({"msg": "Permiso denegado"}), 403
             
        user = UserService.repo.get_by_id(user_id)
        if not user:
            return jsonify({"msg": "Usuario no encontrado"}), 404
        return jsonify(user_schema.dump(user))

    #rol admin puede borrar
    @roles_required("admin") 
    def delete(self, user_id):
        user = UserService.repo.get_by_id(user_id)
        if not user:
            return jsonify({"msg": "Usuario no encontrado"}), 404
        
    
        user.is_active = False
        UserService.repo.save(user)
        
        return jsonify({"msg": "Usuario desactivado"})

    #le damos poder solo al admin para cambiar roles
    @roles_required("admin") 
    def patch(self, user_id):
        data = request.get_json()
        role = data.get("role")
        
        if not role or role not in ["user", "moderator", "admin"]:
            return jsonify({"msg": "Rol inválido"}), 400
            
        user = UserService.repo.get_by_id(user_id)
        if not user:
            return jsonify({"msg": "Usuario no encontrado"}), 404
            
        user.role = role
        UserService.repo.save(user)
        return jsonify({"msg": "Rol actualizado", "role": user.role})