import re
import sqlite3
from tokenize import Exponent

from frontend.backend import exception
from .database import get_db_connection


class DatabaseOperacion:
    """Clase para manejar operaciones de base de datos."""
    def _ejecutar(self,query , params=None , es_select=False):
        """Ejecuta una consulta SQL."""
        try:
            with get_db_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                if es_select:
                    return [dict(row) for row in cursor.fetchall()]
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            raise Exception("Datos duplicados o inválidos.")
        except sqlite3.Error as e:
            raise Exception(f"Database error: {e}")
        
class ClienteDB(DatabaseOperacion):
    """ Clase para manejar operaciones relacionadas con clientes."""
    def insert_cliente(self, nombre_cliente, conneccion_sftp=False):
        """Funcion para crear un cliente en la base de datos"""
        query = "INSERT INTO cliente (nombre_cliente, conneccion_sftp) VALUES (?, ?)"
        cliente_data = (nombre_cliente, conneccion_sftp)
        try:
            return self._ejecutar(query, cliente_data)
        except Exception as e:
            raise e
    def get_clientes(self):
        """Obtiene todos los clientes de la base de datos."""
        query = "SELECT * FROM cliente"
        try:
            return self._ejecutar(query, es_select=True)
        except Exception as e:
            raise e

    def delete_cliente(self, cliente_id):
        """Elimina un cliente por su ID."""
        query = "DELETE FROM cliente WHERE cliente_id = ?"
        try:
            self._ejecutar(query, (cliente_id,))
        except Exception as e:
            raise e

    def update_cliente(self, cliente_id, nombre_cliente, conneccion_sftp):
        """Actualiza la información de un cliente."""
        query = "UPDATE cliente SET nombre_cliente = ?, conneccion_sftp = ? WHERE cliente_id = ?"
        cliente_data = (nombre_cliente, conneccion_sftp, cliente_id)
        try:
            self._ejecutar(query, cliente_data)
        except Exception as e:
            raise e
class SFTPDB(DatabaseOperacion):
    """ Clase para manejar operaciones relacionadas con SFTP."""
    def insert_sftp(self, cliente, usuario, puerto, password, host, ruta_remota):
        """Funcion para crear una configuración SFTP en la base de datos"""
        query = """
        INSERT INTO sftp (cliente, usuario, puerto, password, host, ruta_remota) 
        VALUES (?, ?, ?, ?, ?, ?)
        """
        sftp_data = (cliente, usuario, puerto, password, host, ruta_remota)
        try:
            return self._ejecutar(query, sftp_data)
        except Exception as e:
            raise e

    def update_sftp(self, cliente, usuario, puerto, password, host, ruta_remota):
        """Actualiza la configuración SFTP de un cliente."""
        query = """
        UPDATE sftp 
        SET usuario = ?, puerto = ?, password = ?, host = ?, ruta_remota = ? 
        WHERE cliente = ?
        """
        sftp_data = (usuario, puerto, password, host, ruta_remota, cliente)
        try:
            self._ejecutar(query, sftp_data)
        except Exception as e:
            raise e

    def get_sftp_by_cliente(self, cliente):
        """Obtiene la configuración SFTP de un cliente."""
        query = "SELECT * FROM sftp WHERE cliente = ?"
        try:
            results = self._ejecutar(query, (cliente,), es_select=True)
            return results[0] if results else None
        except Exception as e:
            raise e
    def delete_sftp(self, cliente):
        """Elimina la configuración SFTP de un cliente."""
        query = "DELETE FROM sftp WHERE cliente = ?"
        try:
            self._ejecutar(query, (cliente,))
        except Exception as e:
            raise e 

class EmployeeDB(DatabaseOperacion):
    """ Clase para manejar operaciones relacionadas con empleados."""
    def insert_employee(self, nombre_empleado, rol):
        """Funcion para crear un empleado en la base de datos"""
        query = "INSERT INTO empleado (nombre_empleado, rol) VALUES (?, ?)"
        employee_data = (nombre_empleado, rol)
        try:
            return self._ejecutar(query, employee_data)
        except Exception as e:
            raise e

    def update_employee(self, empleado_id, nombre_empleado, rol):
        """Actualiza la información de un empleado."""
        query = "UPDATE empleado SET nombre_empleado = ?, rol = ? WHERE empleado_id = ?"
        employee_data = (nombre_empleado, rol, empleado_id)
        try:
            self._ejecutar(query, employee_data)
        except Exception as e:
            raise e    
    
    def delete_employee(self, empleado_id):
        """Elimina un empleado por su ID."""
        query = "DELETE FROM empleado WHERE empleado_id = ?"
        try:
            self._ejecutar(query, (empleado_id,))
        except Exception as e:
            raise e
    
class TrailerDB(DatabaseOperacion):
    """ Clase para manejar operaciones relacionadas con trailers."""
    def insert_trailer(self, numero_trailer, placas, hazmat, register_date):
        """Funcion para crear un trailer en la base de datos"""
        query = "INSERT INTO trailer (numero_trailer, placas, hazmat, register_date) VALUES (?, ?, ?, ?)"
        trailer_data = (numero_trailer, placas, hazmat, register_date)
        try:
            return self._ejecutar(query, trailer_data)
        except Exception as e:
            raise e
    def update_trailer(self, trailer_id, numero_trailer, placas, hazmat, register_date):
        """Actualiza la información de un trailer."""
        query = "UPDATE trailer SET numero_trailer = ?, placas = ?, hazmat = ?, register_date = ? WHERE trailer_id = ?"
        trailer_data = (numero_trailer, placas, hazmat, register_date, trailer_id)
        try:
            self._ejecutar(query, trailer_data)
        except Exception as e:
            raise e

    def delete_trailer(self, trailer_id, register_date):
        """Elimina un trailer por su ID."""
        query = "DELETE FROM trailer WHERE trailer_id = ? AND register_date = ?"
        try:
            self._ejecutar(query, (trailer_id, register_date))
        except Exception as e:
            raise e

    def get_trailer_by_numero(self, numero_trailer, register_date):
        """Obtiene la información de un trailer por su número."""
        query = "SELECT * FROM trailer WHERE numero_trailer = ? AND register_date = ?"
        try:
            results = self._ejecutar(query, (numero_trailer, register_date), es_select=True)
            return results[0] if results else None
        except Exception as e:
            raise e
        
class UserNameDB(DatabaseOperacion):
    """Clase para manejar operacion realizaciondos a los usuarios"""
    def insert_username(self,nombre_empleado , email,password , admit=False):

        """ Funcion para crear un usuario sea Admit o no"""
        query = "INSTER INTO user (nombre_empleado , email , password , admit)"
        usuario_data = (nombre_empleado,email,password,admit)
        try:
            result =  self._ejecutar(query,usuario_data , es_select=True)
            return result[0] if result else None
        except Exception as e :
            raise e