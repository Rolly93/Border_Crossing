import os
import uuid
#import random
#from ..utility.shipment_logic import validate_shipment


folder_path = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(folder_path, 'logistica.db')
database_name = database_path
print(f"Database path: {database_name}")

data =[ {"trans_ref":"Rar3215", 
         "cliente_ref" :"92B1337515",  
         "cliente":"Expeditors",
         "tipo_unidad":"Trialer",
         "operador":"Abraham",
         "asignacion_unidad":"12/26/2025 11:10",
         "unidad":"unit_t253 ",
         "trailer":"HGIU5207456",
         "sello_Ori":"Seal_3215",
         "placas":"333460W",
         "tipo_operacion":"Exportacion",
         "origen":"MOGA",
         "destino":"Expeditors LRD",
         "fecha_llegada":"12/26/2025 13:00",
         "fecha_salida":"12/26/2025 13:40",
         "inspeccion_mex":"12/26/2025 13:50",
         "n_sello_mex":"new_Mex_1548",
         "verde_Mex":"12/26/2025 14:10",
         "inspecccion_usa":"12/26/2025 14:20",
         "n_sello_usa":"New_Usa_2865",
         "tipo_inspeccion":"X-Ray",
         "verde_usa":"12/26/2025 15:40",
         "fecha_finalizacion":"12/26/2025 15:50",
         "recive":"Juan" }]

def getData():
    
    return data

def insertData(newData):
    rand_part = random.randint(1000, 9999)
    validate_shipment(newData)
    newData['trans_ref'] = 'RAC' + str(rand_part)
    data.append(newData)
    
    return data


def updateData(changes):
    
    """filtracion de los datos que se van a actualizar"""
    
    trans_ref = changes.get('trans_ref')
    if not trans_ref:
        return
    
    # Buscamos el registro
    shipment = next((item for item in data if item['trans_ref'] == trans_ref), None)
    
    if shipment:
        # Aplicamos SOLO las llaves que vienen en 'changes'
        for key, value in changes.items():
            if key != 'trans_ref':
                shipment[key] = value.strip().upper() if isinstance(value, str) else value
    changes["cliente_ref"] = shipment["cliente_ref"]
    return changes  
import sqlite3

def create_database():
    folder_path = os.path.dirname(os.path.abspath(__file__))
    database_path = os.path.join(folder_path, 'logistica.db')
    database_name = database_path
    print(f"Database path: {database_name}")
    # SQL Schema provided
    sql_script = """
-- 1. Tablas Maestras
 CREATE TABLE IF NOT EXISTS Empleados (
     pk_empleado_id INTEGER PRIMARY KEY AUTOINCREMENT,
     str_nombre VARCHAR,
     int_edad INTEGER,
     date_fecha_nacimiento DATE,
     str_seguro_social VARCHAR NOT NULL,
     str_rfc VARCHAR NOT NULL,
     str_curp VARCHAR NOT NULL,
     str_licencia VARCHAR,
     date_ingreso DATE NOT NULL
 );

 CREATE TABLE IF NOT EXISTS Cargo (
     uk_empleado_id INTEGER, -- Eliminado AUTOINCREMENT (es una FK)
     str_nombre_cargo VARCHAR UNIQUE,
     str_area_cargo VARCHAR,
     uk_str_correo VARCHAR UNIQUE,
     FOREIGN KEY (uk_empleado_id) REFERENCES Empleados (pk_empleado_id)
 );

 CREATE TABLE IF NOT EXISTS Areas (
     str_cargo VARCHAR,
     str_puesto VARCHAR,
     FOREIGN KEY (str_cargo) REFERENCES Cargo (str_nombre_cargo),
     FOREIGN KEY (str_puesto) REFERENCES Cargo (str_area_cargo)
 );

 CREATE TABLE IF NOT EXISTS Transporte (
     pk_uk_transporte_id INTEGER PRIMARY KEY AUTOINCREMENT,
     str_uk_fk_asignado VARCHAR,
     str_tipo VARCHAR,
     uk_placa VARCHAR,
     uk_num_unidad VARCHAR UNIQUE,
     int_ejes INTEGER,
     str_hazmat BOOLEAN,
     dbl_capacidad_peso REAL,
     char_puede_cruzar BOOLEAN,
     str_tipo_dano VARCHAR,
     FOREIGN KEY (str_uk_fk_asignado) REFERENCES Cargo (str_nombre_cargo)
 );

 CREATE TABLE IF NOT EXISTS Caja (
     pk_caja_clave INTEGER PRIMARY KEY AUTOINCREMENT,
     str_num_caja VARCHAR UNIQUE,
     uk_str_placas VARCHAR,
     str_estado VARCHAR,
     char_hazmat BOOLEAN,
     str_condiciones TEXT
 );

 -- 2. Tablas de Eventos (Cronología)
 -- Se mantiene la estructura DATETIME para facilitar la comparación de tiempos
 CREATE TABLE IF NOT EXISTS fecha_llegada (
     uk_ref VARCHAR,
     str_capturado VARCHAR,
     str_caja VARCHAR,
     str_tractor VARCHAR,
     str_chofer VARCHAR,
     str_tipo INTEGER,
     fecha DATETIME,
     str_evento VARCHAR,
     FOREIGN KEY (str_capturado) REFERENCES Cargo (str_nombre_cargo),
     FOREIGN KEY (str_caja) REFERENCES Caja (str_num_caja),
     FOREIGN KEY (str_tractor) REFERENCES Transporte (uk_num_unidad),
     FOREIGN KEY (str_chofer) REFERENCES Cargo (str_nombre_cargo)
 );

 -- ... (Las tablas fecha_salida, inspeccion_mex, verde_Mex, inspecccion_usa, verde_usa, fecha_finalizacion siguen el mismo patrón)

 -- 3. Tablas de Clientes y Configuración (Actualizadas con Host y Ruta)
 CREATE TABLE IF NOT EXISTS cliente (
     cliente_id INTEGER PRIMARY KEY AUTOINCREMENT,
     nombre_cliente VARCHAR,
     conneccion_sftp BOOLEAN
 );

 CREATE TABLE IF NOT EXISTS sftp (
     cliente INTEGER,
     usuario VARCHAR,
     puerto VARCHAR,
     password VARCHAR NOT NULL,
     host VARCHAR,
     ruta_remota VARCHAR,
     FOREIGN KEY (cliente) REFERENCES cliente (cliente_id)
 );

 -- 4. Cruce Completo
 CREATE TABLE IF NOT EXISTS CruceCompleto (
     str_Tractor VARCHAR,
     str_Operador VARCHAR,
     str_caja VARCHAR,
     str_Llegada_Fecha_Patio_Origen DATETIME,
     str_Salida_Fecha_Patio_Origen DATETIME,
     str_VerdeMX_Fecha DATETIME,
     str_RojoMx_Fecha DATETIME,
     str_RojoMX_NuevoSello VARCHAR,
     str_VerdeUS_Fecha DATETIME,
     str_RojoUSA_Fecha DATETIME,
     str_RojoUSA_NuevoSello VARCHAR,
     str_Entrega_Fecha DATETIME,
     str_Entrega_Recibe VARCHAR,
     FOREIGN KEY (str_Tractor) REFERENCES Transporte (uk_num_unidad),
     FOREIGN KEY (str_caja) REFERENCES Caja (str_num_caja)
 );"""

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
def create_user():
    """Funcion para crear un usuario admin / Usuario en la base de datos"""
    pass

def create_driver():
    """Funcion para crear un chofer en la base de datos"""
    pass

def create_sftp_config():
    """Funcion para crear la configuracion SFTP en la base de datos"""
    pass

if __name__ == "__main__":
    create_database()