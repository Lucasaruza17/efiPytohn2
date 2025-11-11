from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt
from repositories import UserRepository, PostRepository, ComentarioRepository
from services import UserService
from . import PostAPI, ComentarioAPI, CategoriaAPI, UserAPI
from decorators import roles_required


#uso una funcion/def que haga q reciba app como argumento
def register_api_routes(app):

    #mueve todas las rutas API
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

    @app.route("/api/stats", methods=["GET"])
    @roles_required("moderator", "admin")
    def get_stats():
        claims = get_jwt()
        current_user_role = claims.get("role")

        # repositorios
        post_repo = PostRepository()
        user_repo = UserRepository()
        comment_repo = ComentarioRepository()

        #stats basicas
        stats = {
            "total_posts": len(post_repo.get_all()),
            "total_comments": len(comment_repo.get_all()),
            "total_users": len(user_repo.get_all())
        }
        
        # stats solo para Admin
        if current_user_role == 'admin':
            stats["posts_last_week"] = post_repo.count_posts_last_week()
            
        return jsonify(stats), 200


    #esto aca trae todo lo .add_url_rule aquí, usando app
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
    # (Tu 'DELETE' ya estaba aquí, lo cual es perfecto)
    app.add_url_rule("/api/categories/<int:categoria_id>", view_func=categoria_view, methods=["GET","PUT","DELETE"])

    # Usuarios/Admin
    user_view = UserAPI.as_view("users_api")
    app.add_url_rule("/api/users", defaults={"user_id": None}, view_func=user_view, methods=["GET"])
    app.add_url_rule("/api/users/<int:user_id>", view_func=user_view, methods=["GET","DELETE"])
    app.add_url_rule("/api/users/<int:user_id>/role", view_func=user_view, methods=["PATCH"])