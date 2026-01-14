
import os
import re
import sqlite3
from tokenize import Exponent

#from ..exception.exceptions      import exception

from backend.utility.utily import hashdata ,cryptoPswd

#configuracion para obtencion de datos 
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logistica.db')  

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
    
    def get_db_connection(self):
        """Obtiene una conexión a la base de datos."""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    #funcion para crear la base de datos
    @staticmethod
    def create_database():
        database_name = DB_PATH
        print(f"Database path: {DB_PATH}")
        conn = None
        # SQL Schema provided
        sql_script = """
-- 1. Tablas Maestras
 CREATE TABLE IF NOT EXISTS empleado (
     empleado_id INTEGER PRIMARY KEY AUTOINCREMENT,
     nombre_empleado VARCHAR,
     rol VARCHAR,
     email VARCHAR,
     date_ingreso DATE DEFAULT (CURRENT_DATE ) 
 );


 CREATE TABLE IF NOT EXISTS transporte (
     transporte_id INTEGER PRIMARY KEY AUTOINCREMENT,
     empleado_id INTEGER, -- aquien se lo asignan
     tipo VARCHAR, --trailer , placa , 3.5 etc
     placa VARCHAR UNIQUE, 
     num_unidad VARCHAR UNIQUE,
     ishazmat BOOLEAN ,
     puede_cruzar BOOLEAN DEFAULT TRUE,
     register_date DATETIME DEFAULT CURRENT_TIMESTAMP,
     FOREIGN KEY (empleado_id) REFERENCES empleado (empleado_id)
 );

 CREATE TABLE IF NOT EXISTS trailer (
     trailer_id INTEGER PRIMARY KEY AUTOINCREMENT,
     numero_trailer VARCHAR UNIQUE,
     placas VARCHAR,
     hazmat BOOLEAN,
     register_date DATETIME DEFAULT CURRENT_TIMESTAMP
 );
 

CREATE TABLE IF NOT EXISTS bitacora_eventos (
    id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
    client_ref VARCHAR(50) NOT NULL,
    trans_ref VARCHAR(50) NOT NULL,
    tipo_evento VARCHAR(30) NOT NULL,         
    trailer_id VARCHAR(50),              
    id_unidad VARCHAR(50),              
    id_operador VARCHAR(100),
    comentarios VARCHAR(250),       
    sello VARCHAR(250),       
    id_CSR VARCHAR(50),                 
    status VARCHAR(50),                 
    fecha DATETIME NOT NULL,            
    fecha_captura DATETIME DEFAULT CURRENT_TIMESTAMP,

    
    -- Llaves foráneas (Asegúrate que estas tablas existan primero)
    FOREIGN KEY (trailer_id) REFERENCES trailer (numero_trailer),
    FOREIGN KEY (id_unidad) REFERENCES transporte (num_unidad),
    FOREIGN KEY (id_operador) REFERENCES empleado (nombre_empleado),
    FOREIGN KEY (id_CSR) REFERENCES empleado (nombre_empleado)
);

-- 2. Índices de Rendimiento (Cruciales para que el Dashboard sea rápido)
-- Este índice permite que el GROUP BY trnasf_ref sea instantáneo
CREATE INDEX IF NOT EXISTS idx_bitacora_ref ON bitacora_eventos (trans_ref);

-- Este índice ayuda a ordenar los embarques más recientes primero
CREATE INDEX IF NOT EXISTS idx_bitacora_fecha ON bitacora_eventos (fecha);


 -- 3. Tablas de Clientes y Configuración (Actualizadas con Host y Ruta)
 CREATE TABLE IF NOT EXISTS cliente (
     cliente_id INTEGER PRIMARY KEY AUTOINCREMENT,
     nombre_cliente VARCHAR,
     conneccion_sftp BOOLEAN,
     caputrado DATETIME DEFAULT CURRENT_TIMESTAMP
 );

 CREATE TABLE IF NOT EXISTS sftp (
     cliente INTEGER, --tiene que se el id
     usuario VARCHAR,
     puerto VARCHAR,
     password VARCHAR NOT NULL,
     host VARCHAR,
     ruta_remota VARCHAR,
     FOREIGN KEY (cliente) REFERENCES cliente (cliente_id)
 );

CREATE TABLE IF NOT EXISTS user (
    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_empleado VARCHAR,
    email VARCHAR UNIQUE,
    password VARCHAR,
    admit BOOLEAN,
    FOREIGN KEY (nombre_empleado) REFERENCES empleado (nombre_empleado)
);
 
 -- 4. Cruce Completo
 CREATE TABLE IF NOT EXISTS crucecompleto (
     tractor VARCHAR,
     operador VARCHAR,
     trailer VARCHAR,
     Llegada_Fecha_Patio_Origen DATETIME,
     Salida_Fecha_Patio_Origen DATETIME,
     VerdeMX_Fecha DATETIME,
     RojoMx_Fecha DATETIME,
     RojoMX_NuevoSello VARCHAR,
     VerdeUS_Fecha DATETIME,
     RojoUSA_Fecha DATETIME,
     RojoUSA_NuevoSello VARCHAR,
     Entrega_Fecha DATETIME,
     Entrega_Recibe VARCHAR,
     FOREIGN KEY (tractor) REFERENCES transporte (num_unidad),
     FOREIGN KEY (trailer) REFERENCES trailer (numero_trailer),
     FOREIGN KEY (operador) REFERENCES empleado (nombre_empleado ) 
     ); """

        try:
            conn = sqlite3.connect(database_name)
            # Connect to SQLite (creates the file if it doesn't exist)
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")

            # Execute the script
            print("Creating tables and relationships...")
            cursor.executescript(sql_script)

            conn.commit()
            print(f"Database '{database_name}' created successfully.")

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            if conn:
                conn.close()
class ClienteDB(DatabaseOperacion):
    """ Clase para manejar operaciones relacionadas con clientes."""
    def insert_cliente(self, nombre_cliente, conneccion_sftp=False):
        """Funcion para crear un cliente en la base de datos"""
        query = "INSERT INTO cliente (nombre_cliente, conneccion_sftp) VALUES (?, ?)"
        cliente_data = (nombre_cliente, conneccion_sftp)
        return self._ejecutar(query, cliente_data)
        
        
    def get_clientes(self):
        """Obtiene todos los clientes de la base de datos."""
        query = "SELECT * FROM cliente"
        return self._ejecutar(query, es_select=True)
        
    def delete_cliente(self, cliente_id):
        """Elimina un cliente por su ID."""
        query = "DELETE FROM cliente WHERE cliente_id = ?"
        self._ejecutar(query, (cliente_id,))
        
    def update_cliente(self, cliente_id, nombre_cliente, conneccion_sftp):
        """Actualiza la información de un cliente."""
        query = "UPDATE cliente SET nombre_cliente = ?, conneccion_sftp = ? WHERE cliente_id = ?"
        cliente_data = (nombre_cliente, conneccion_sftp, cliente_id)
        self._ejecutar(query, cliente_data)
        
class SFTPDB(DatabaseOperacion):
    """ Clase para manejar operaciones relacionadas con SFTP."""
    def insert_sftp(self, id_cliente, usuario, puerto, password, host, ruta_remota):
        """Funcion para crear una configuración SFTP en la base de datos"""
        query = """
        INSERT INTO sftp (cliente, usuario, puerto, password, host, ruta_remota) 
        VALUES (?, ?, ?, ?, ?, ?)
        """
        pswdhashed = cryptoPswd(password)

        sftp_data = (id_cliente, usuario, puerto, pswdhashed, host, ruta_remota)
        return self._ejecutar(query, sftp_data)
        
    def update_sftp(self, id_cliente, usuario, puerto, password, host, ruta_remota):
        """Actualiza la configuración SFTP de un cliente."""
        query = """
        UPDATE sftp 
        SET usuario = ?, puerto = ?, password = ?, host = ?, ruta_remota = ? 
        WHERE cliente = ?
        """
        pswdhashed = cryptoPswd(password)

        sftp_data = (usuario, puerto, pswdhashed, host, ruta_remota, id_cliente)
        self._ejecutar(query, sftp_data)
        
    def get_sftp_by_cliente(self, id_cliente):
        """Obtiene la configuración SFTP de un cliente."""
        query = "SELECT * FROM sftp WHERE cliente = ?"
        results = self._ejecutar(query, (id_cliente,), es_select=True)
        return results[0] if results else None
    
    def delete_sftp(self, cliente):
        """Elimina la configuración SFTP de un cliente."""
        query = "DELETE FROM sftp WHERE cliente = ?"
        self._ejecutar(query, (cliente,))
        
class EmployeeDB(DatabaseOperacion):
    """ Clase para manejar operaciones relacionadas con empleados."""
    def insert_employee(self, nombre_empleado, rol ,email,):
        """Funcion para crear un empleado en la base de datos"""
        query = "INSERT INTO empleado (nombre_empleado, rol , email) VALUES (?, ?,?)"
        employee_data = (nombre_empleado, rol,email)
        
        return self._ejecutar(query, employee_data)
        
    def update_employee(self, empleado_id, nombre_empleado, rol ,email):
        """Actualiza la información de un empleado."""
        query = "UPDATE empleado SET nombre_empleado = ?, rol = ? ,email = ? WHERE empleado_id = ?"
        employee_data = (nombre_empleado, rol ,email , empleado_id)
        
        self._ejecutar(query, employee_data)

    def delete_employee(self, empleado_id):
        """Elimina un empleado por su ID."""
        query = "DELETE FROM empleado WHERE empleado_id = ?"
        
        self._ejecutar(query, (empleado_id,))
        
    
class TrailerDB(DatabaseOperacion):
    """ Clase para manejar operaciones relacionadas con trailers."""
    def insert_trailer(self, numero_trailer, placas, hazmat):
        """Funcion para crear un trailer en la base de datos"""
        query = "INSERT INTO trailer (numero_trailer, placas, hazmat) VALUES (?, ?, ?)"
        trailer_data = (numero_trailer, placas, hazmat)
        
        return self._ejecutar(query, trailer_data)
        
    def update_trailer(self, trailer_id, numero_trailer, placas, hazmat):
        """Actualiza la información de un trailer."""
        query = "UPDATE trailer SET numero_trailer = ?, placas = ?, hazmat = ?  WHERE trailer_id = ?"
        trailer_data = (numero_trailer, placas, hazmat, trailer_id)
        
        self._ejecutar(query, trailer_data)
        

    def delete_trailer(self, trailer_id):
        """Elimina un trailer por su ID."""
        query = "DELETE FROM trailer WHERE trailer_id = ? "

        self._ejecutar(query, (trailer_id,))

    def get_trailer_by_numero(self, numero_trailer):
        """Obtiene la información de un trailer por su número."""
        query = "SELECT * FROM trailer WHERE numero_trailer = ?  "
        results = self._ejecutar(query, (numero_trailer   ), es_select=True)
        return results[0] if results else None
        
class UserNameDB(DatabaseOperacion):
    """Clase para manejar operacion realizaciondos a los usuarios"""
    def insert_username(self,nombre_empleado , email,password , admit=False):
        

        pswhashed = hashdata(password)

        """ Funcion para crear un usuario sea Admit o no"""
        query = """
        INSERT INTO user (nombre_empleado , email , password , admit)
          VALUES (?,?,?,?)
          """
        
        usuario_data = (nombre_empleado,email,pswhashed,admit)

        result =  self._ejecutar(query,usuario_data )
        return result is not None 
        
        
    def get_username(self,email,password):
        """funcion para extraer el usuario y contraseña de la base de datos"""
        query = "SELECT * FROM user WHERE email = ? AND password = ?"
        
        userdata = [email,password]
        
        result = self._ejecutar(query,userdata,es_select=True)
        return result[0] if result else None
        

    def delete_username(self,email):
        """funcion para eliminar un usuario de la base de datos"""
        query = "DELETE FROM user WHERE email = ?"
        self._ejecutar(query,(email,))
        
    
    def update_username(self,email,password):
        """funcion para actualizar un usuario de la base de datos"""
        query = "UPDATE user SET password = ? WHERE email = ?"

        pswhashed = hashdata(password)

        userdata = (pswhashed,email)
        self._ejecutar(query,userdata)
        
class status_cruce(DatabaseOperacion):

    """Clase para manejar los estatus de cruce en una tabla unificada."""
    
    # Ahora validamos el TIPO de evento, no el nombre de la tabla
    _EVENTOS = ['fecha_llegada','fecha_salida', 'inspeccion_mex', 'verde_mex', 'inspeccion_usa', 'verde_usa', 'fecha_finalizacion']

    def is_valid_event(self, event_type):
        if event_type not in self._EVENTOS:
            raise ValueError(f"El evento '{event_type}' no es válido.")

    def insertar_evento(self, trans_ref, client_ref, tipo_evento, fecha, 
                    id_trailer=None, id_unidad=None, id_operador=None, 
                    id_CSR=None, status=None, sello=None, comentarios=None):
        """Inserta un nuevo registro en la bitácora única."""
        self.is_valid_event(tipo_evento)
        
        # El query siempre apunta a la misma tabla: Bitacora_Eventos
        query = """
            INSERT INTO bitacora_eventos 
            (trans_ref, client_ref, tipo_evento, fecha, trailer_id, id_unidad, 
         id_operador, id_CSR, status, sello, comentarios) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ? , ?)
        """
        # trans_ref se usa como uk_ref para la unificación
        evento_data = (trans_ref, client_ref, tipo_evento, fecha, id_trailer, id_unidad, 
              id_operador, id_CSR, status, sello, comentarios)
        return self._ejecutar(query, evento_data)

    def actualizar_evento(self, trans_ref, tipo_evento, nuevos_datos_dict):
        """
        Actualiza un evento específico. 
        Al ser tabla única, identificas el registro por la referencia y el tipo de evento.
        """
        self.is_valid_event(tipo_evento)
        
        # Ejemplo: Actualizar la fecha y el status de la 'fecha_llegada' de un trans_ref específico
        query = """
            UPDATE bitacora_eventos 
            SET status = ?, fecha = ?, id_operador = ?
            WHERE trans_ref = ? AND tipo_evento = ?
        """
        params = ( nuevos_datos_dict.get('status'),
                   nuevos_datos_dict.get('fecha'),
                   nuevos_datos_dict.get('id_operador'),
                   trans_ref, tipo_evento)
        
        return self._ejecutar(query, params)

    def eliminar_evento(self, trans_ref, tipo_evento):
        """Elimina un paso específico de la cronología del cruce."""
        self.is_valid_event(tipo_evento)
        

        query = "DELETE FROM bitacora_eventos WHERE trans_ref = ? AND tipo_evento = ?"
        return self._ejecutar(query, (trans_ref, tipo_evento))
    
    def obtener_dashboard(self):
        """Consulta pivoteada para tu tabla de la imagen."""
        query = """
            SELECT 
                trans_ref, id_trailer, id_unidad, id_operador, id_CSR, client_ref,
                MAX(CASE WHEN tipo_evento = 'fecha_llegada' THEN fecha END) AS fecha_llegada,
                MAX(CASE WHEN tipo_evento = 'fecha_salida' THEN fecha END) AS fecha_salida,
                MAX(CASE WHEN tipo_evento = 'inspeccion_mex' THEN fecha END) AS insp_mex,
                MAX(CASE WHEN tipo_evento = 'inspeccion_mex' THEN sello END) AS sello_mex,
                MAX(CASE WHEN tipo_evento = 'verde_mex' THEN fecha END) AS verde_mex,
                MAX(CASE WHEN tipo_evento = 'inspeccion_usa' THEN fecha END) AS inspeccion_usa,
                MAX(CASE WHEN tipo_evento = 'inspeccion_usa' THEN sello END) AS sello,
                MAX(CASE WHEN tipo_evento = 'verde_usa' THEN fecha END) AS verde_usa,
                MAX(CASE WHEN tipo_evento = 'fecha_finalizacion' THEN fecha END) AS fecha_finalizacion
            FROM bitacora_eventos
            GROUP BY trans_ref
            ORDER BY MAX(fecha_captura) DESC
        """
        # Usamos tu parámetro es_select=True para recibir la lista de diccionarios
        return self._ejecutar(query, es_select=True)

class trasporte_unidad (DatabaseOperacion):
    """
    Docstring for trasporte_unidad, para la asignacion de unidades a 'x' operador
    """
    def insert_transporte(self,empleado_id , tipo , placa, num_unidad , ishazmat ):
        query = """INSERT INTO transporte (empleado_id, tipo, placa, num_unidad, ishazmat) 
            VALUES (?, ?, ?, ?, ?)"""
        transporte_data = (empleado_id , tipo , placa, num_unidad , ishazmat )
        try:
            return self._ejecutar(query,transporte_data)
        except Exception as e:
            raise e
    
    def update_transporte(self, transporte_id, empleado_id , puede_cruzar , placa ):
        query ="""UPDATE transporte 
            SET puede_cruzar = ?, empleado_id = ?, placa = ? 
            WHERE transporte_id = ?"""
        data_unit = (puede_cruzar , empleado_id  , placa ,transporte_id)
        try:
            self._ejecutar(query,data_unit)
        except Exception as e:
            raise e
    def delete_transporte(self,transporte_id):
        query = "DELETE FROM transporte WHERE transporte_id = ?"
        try:
            self._ejecutar(query,(transporte_id,))
        except Exception as e:
            raise e
        
    def get_all_transporte(self):
        query = "SELECT * FROM transporte"
        return self._ejecutar(query,es_select=True)
        
