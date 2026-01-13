from backend.model.models import UserNameDB
from backend.utility.utily import hashdata
from backend.utility.service.email_service import EmailService


class AuthService():
    def __init__(self):
        self.db = UserNameDB()
        self.email_svc = EmailService()


    def autenticar(self,username,password):
        pswd_hashed = hashdata(password)
        user_row = self.db.get_username(username,pswd_hashed)

        if user_row:
            from backend.model.entities import User
            user = User(user_row['id'], user_row['email'],user_row['nombre_empleado'], user_row['admit'])
            return user
        return None

    def verificar_primer_uso(self):
        if not self.db.get_username():
            return True
        return False

    def configurar_primer_admin(self,username,password,nombre_empleado,email):
        pswd_hashed = hashdata(password)
        self.db.insert_username(nombre_empleado=nombre_empleado,email=email,password=pswd_hashed,admit=True )
        self.email_svc.enviar_codigo_admin(email,self.email_svc.generar_codigo())

