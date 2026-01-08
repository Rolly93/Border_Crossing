from backend.db.confi import Config
from flask_login import LoginManager
from backend.routes.api import api_bp
from backend.routes.auth import auth_bp
from flask import Flask , render_template
from backend.model.models import users_db
from backend.routes.client import client_bp
from backend.routes.shipment import shipment_bp
from backend.routes.dashboard import dashboard_bp


# Configuración de Flask
def create_app (*args, **kwargs):
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'
    login_manager.login_message = "Por Favor inicia sesion paraa acceder a esta pagina"
    login_manager.login_message_category = "info"

    app.secret_key = "super_secret_key"


    @login_manager.user_loader
    def load_user(user_id):

        return users_db.get(user_id)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
        
    # Registro de Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(shipment_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(client_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config['DEBUG'],port=app.config.get('PORT', 5000))
else:
    myapp = create_app()
