from flask.views import MethodView
from flask import jsonify, request
from services.categoria_service import CategoriaService
from schemas import CategoriaSchema
from flask_jwt_extended import jwt_required
from decorators import roles_required

categoria_schema = CategoriaSchema()
categorias_schema = CategoriaSchema(many=True)


class CategoriaAPI(MethodView):
    

    def get(self, categoria_id):
        if categoria_id:
            categoria = CategoriaService.repo.get_by_id(categoria_id)
            if not categoria:
                return jsonify({"msg": "Categoría no encontrada"}), 404
            return jsonify(categoria_schema.dump(categoria))
        categorias = CategoriaService.repo.get_all()
        return jsonify(categorias_schema.dump(categorias))

    #admin y moderador
    @roles_required("moderator", "admin") 
    def post(self, categoria_id=None):
        data = request.get_json()
        nombre = data.get("nombre")
        nueva_categoria = CategoriaService.crear_categoria(nombre)
        return jsonify(categoria_schema.dump(nueva_categoria)), 201

    #admins y moderador
    @roles_required("moderator", "admin")
    def put(self, categoria_id):
        data = request.get_json()
        categoria = CategoriaService.repo.get_by_id(categoria_id)
        if not categoria:
            return jsonify({"msg": "Categoría no encontrada"}), 404
        nombre = data.get("nombre")
        
        categoria.nombre = nombre
        actualizada = CategoriaService.repo.save(categoria)
        
        return jsonify(categoria_schema.dump(actualizada))

    #admin solos
    @roles_required("admin")
    def delete(self, categoria_id):
        categoria = CategoriaService.repo.get_by_id(categoria_id)
        if not categoria:
            return jsonify({"msg": "Categoría no encontrada"}), 404
        
        CategoriaService.repo.delete(categoria)
        
        return jsonify({"msg": "Categoría eliminada"})