from backend.db.confi import Config
from backend.model.models import UserNameDB
from backend.utility.utily import hashdata
from backend.utility.service.email_service import EmailService


class AuthService():
    def __init__(self):
        self.db = UserNameDB()
        self.email_svc = EmailService(api_key=Config.RESNDER_API_KEY)

    def autenticar(self, username, password):
        pswd_hashed = hashdata(password)
        user_row = self.db.get_username(username, pswd_hashed)

        if user_row:
            from backend.model.entities import User
            user = User(user_row['id'], user_row['email'], user_row['nombre_empleado'], bool(user_row['admit']))
            
            if user.admit:
                codigo = self.email_svc.generar_codigo()
                self.db.update_codigo_seguridad(user.id, codigo)
                self.email_svc.enviar_codigo_admin(user.email, codigo)
            return user
        return None

    def es_token_valido(self, token_recibido):
        # Una sola función para validar el acceso a rutas especiales
        return token_recibido == Config.TOKEN_CONFIGURAR_ADMIN

    def crear_usuario(self, nombre, email, password, es_admin=False):
        """ESTA ES LA ÚNICA FUNCIÓN QUE NECESITAS PARA INSERTAR"""
        pswd_hashed = hashdata(password)
        return self.db.insert_username(
            nombre_empleado=nombre,
            email=email,
            password=pswd_hashed,
            admit=es_admin 
        )