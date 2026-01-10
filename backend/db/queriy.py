import re
import sqlite3
from tokenize import Exponent

from ..exception.exceptions      import exception
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
    def insert_employee(self, nombre_empleado, rol ,email,):
        """Funcion para crear un empleado en la base de datos"""
        query = "INSERT INTO empleado (nombre_empleado, rol) VALUES (?, ?)"
        employee_data = (nombre_empleado, rol,email)
        try:
            return self._ejecutar(query, employee_data)
        except Exception as e:
            raise e

    def update_employee(self, empleado_id, nombre_empleado, rol ,email):
        """Actualiza la información de un empleado."""
        query = "UPDATE empleado SET nombre_empleado = ?, rol = ? WHERE empleado_id = ?"
        employee_data = (nombre_empleado, rol, empleado_id ,email)
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
        
    def get_username(self,email,password):
        """funcion para extraer el usuario y contraseña de la base de datos"""
        query = "SELECT * FROM user WHERE email = ? AND password = ?"
        
        userdata = [email,password]
        
        try:
            result = self._ejecutar(query,userdata,es_select=True)
            return result[0] if result else None
        except Exception as e:
            raise e
    
    def delete_username(self,email):
        """funcion para eliminar un usuario de la base de datos"""
        query = "DELETE FROM user WHERE email = ?"
        try:
            self._ejecutar(query,(email,))
        except Exception as e:
            raise e
    
    def update_username(self,email,password):
        """funcion para actualizar un usuario de la base de datos"""
        query = "UPDATE user SET password = ? WHERE email = ?"
        userdata = (password,email)
        try:
            self._ejecutar(query,userdata)
        except Exception as e:
            raise e
      
class status_cruce(DatabaseOperacion):
    """Clase para manejar los estatus de cruce en una tabla unificada."""
    
    # Ahora validamos el TIPO de evento, no el nombre de la tabla
    _EVENTOS = ['fecha_llegada','fecha_salida', 'inspeccion_mex', 'verde_Mex', 'inspeccion_usa', 'verde_usa', 'fecha_finalizacion']

    def is_valid_event(self, event_type):
        if event_type not in self._EVENTOS:
            raise ValueError(f"El evento '{event_type}' no es válido.")

    def insertar_evento(self, id_traier, id_unidad, id_operador, id_CSR, status, fecha,  tipo_evento, cliente_ref, trans_ref):
        """Inserta un nuevo registro en la bitácora única."""
        self.is_valid_event(tipo_evento)
        
        # El query siempre apunta a la misma tabla: Bitacora_Eventos
        query = """
            INSERT INTO Bitacora_Eventos 
            (uk_ref, tipo_evento, id_traier, id_unidad, id_operador, id_CSR, status, fecha, cliente_ref) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        # trans_ref se usa como uk_ref para la unificación
        evento_data = (trans_ref, tipo_evento, id_traier, id_unidad, id_operador, id_CSR, status, fecha, cliente_ref)
        return self._ejecutar(query, evento_data)

    def actualizar_evento(self, trans_ref, tipo_evento, nuevos_datos_dict):
        """
        Actualiza un evento específico. 
        Al ser tabla única, identificas el registro por la referencia y el tipo de evento.
        """
        self.is_valid_event(tipo_evento)
        
        # Ejemplo: Actualizar la fecha y el status de la 'fecha_llegada' de un trans_ref específico
        query = """
            UPDATE Bitacora_Eventos 
            SET tipo_evento = ?, fecha = ?, id_operador = ?
            WHERE client_ref = ? AND tipo_evento = ?
        """
        params = (nuevos_datos_dict['status'], nuevos_datos_dict['fecha'], nuevos_datos_dict['id_operador'], trans_ref, tipo_evento)
        return self._ejecutar(query, params)

    def eliminar_evento(self, trans_ref, tipo_evento):
        """Elimina un paso específico de la cronología del cruce."""
        query = "DELETE FROM Bitacora_Eventos WHERE client_ref = ? AND tipo_evento = ?"
        return self._ejecutar(query, (trans_ref, tipo_evento))
    
def obtener_dashboard(self):
        """Consulta pivoteada para tu tabla de la imagen."""
        query = """
            SELECT 
                trans_ref, id_trailer, id_unidad , id_operador, id_CSR, client_ref
                MAX(CASE WHEN tipo_evento = 'LLEGADA' THEN fecha END) AS fecha_llegada,
                MAX(CASE WHEN tipo_evento = 'SALIDA' THEN fecha END) AS fecha_salida,
                MAX(CASE WHEN tipo_evento = 'INSP_MEX' THEN fecha END) AS insp_mex,
                MAX(CASE WHEN tipo_evento = 'INSP_MEX' THEN str_comentarios END) AS sello_mex,
                MAX(CASE WHEN tipo_evento = 'VERDE_MEX' THEN fecha END) AS verde_mex,
                MAX(CASE WHEN tipo_evento = 'FINALIZADO' THEN fecha END) AS fecha_finalizacion
            FROM Bitacora_Eventos
            GROUP BY trans_ref
            ORDER BY MAX(fecha_captura) DESC
        """
        # Usamos tu parámetro es_select=True para recibir la lista de diccionarios
        return self._ejecutar(query, es_select=True)