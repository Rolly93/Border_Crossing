from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, nombre, rol):
        self.id = id
        self.nombre = nombre
        self.rol = rol

# La base de datos vive aquí, accesible para todos
