from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, nombre, rol):
        self.id = id
        self.nombre = nombre
        self.rol = rol

# La base de datos vive aquí, accesible para todos
"""users_db = {
    "1": User("1", "Administrador", "admin"),
    "2": User("2", "Invitado", "cliente")
}"""