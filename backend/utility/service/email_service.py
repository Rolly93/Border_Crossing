import resend
import random
import string

class EmailService:
    def __init__(self):
        resend.api_key = "key_"

    def enviar_codigo_admin(self,email,codigo):
        try:
            params ={
                "from" : "onboarding@resend.dev",
                "to": email ,
                "subject": "Codigo de Accesp Administrador",
               "html": f"""
                    <h1>Verificación de Seguridad</h1>
                    <p>Tu código de acceso es: <strong>{codigo}</strong></p>
                    <p>Este código expirará en 10 minutos.</p>
                """ }
            resend.Emails.send(params)
            return True
        except Exception as e:
            print(f"Error enviado correo: {e}")
            return False
    def generar_codigo(self):
        return ''.join(random.choices(string.digits, k=6))