from flask import Flask
from flask_login import UserMixin
from flask_login import LoginManager
from backend.routes.api import api_bp
from backend.routes.auth import auth_bp
from backend.routes.client import client_bp
from backend.routes.shipment import shipment_bp
from backend.routes.dashboard import dashboard_bp

class User(UserMixin):
    def __init__(self, id, nombre, rol):
        self.id = id
        self.nombre = nombre
        self.rol = rol

# Tu "base de datos" manual
users_db = {
    "1": User("1", "Administrador", "admin"),
    "2": User("2", "Invitado", "cliente")
}


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login'
login_manager.login_message = "Por Favor inicia sesion paraa acceder a esta pagina"
login_manager.login_message_category = "info"

app.secret_key = "super_secret_key"


@login_manager.user_loader
def load_user(user_id):

    return users_db.get(user_id)


# Registro de Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(shipment_bp)
app.register_blueprint(api_bp)
app.register_blueprint(client_bp)

if __name__ == '__main__':
    app.run(debug=True)