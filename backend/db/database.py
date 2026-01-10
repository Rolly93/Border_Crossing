import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logistica.db')  
def  get_db_connection():
    """Establece y devuelve una conexion a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


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
     email VARCHAR
     date_ingreso DATE NOT NULL
 );


 CREATE TABLE IF NOT EXISTS transporte (
     transporte_id INTEGER PRIMARY KEY AUTOINCREMENT,
     uk_fk_asignado VARCHAR,
     str_tipo VARCHAR, -Importacion / Exportacion
     uk_placa VARCHAR, 
     uk_num_unidad VARCHAR UNIQUE,
     str_hazmat BOOLEAN ,
     char_puede_cruzar BOOLEAN,
     FOREIGN KEY (uk_fk_asignado) REFERENCES Cargo (str_nombre_cargo)
 );

 CREATE TABLE IF NOT EXISTS Caja (
     id_caja INTEGER PRIMARY KEY AUTOINCREMENT,
     num_caja VARCHAR UNIQUE,
     placas VARCHAR,
     estado VARCHAR,
     ishazmat BOOLEAN,
     str_condiciones VARCHAR
 );
CREATE TABLE IF NOT EXISTS Bitacora_Eventos (
    id_evento INTEGER PRIMARY KEY AUTOINCREMENT,
    uk_ref VARCHAR(50) NOT NULL,
    str_tipo_evento VARCHAR(30) NOT NULL,
    str_capturado VARCHAR(100),         
    str_caja VARCHAR(50),               
    str_tractor VARCHAR(50),            
    str_chofer VARCHAR(100),            
    str_tipo_cargo INTEGER,             
    fecha DATETIME NOT NULL,            
    fecha_captura DATETIME DEFAULT CURRENT_TIMESTAMP,
    str_comentarios VARCHAR(255),
    
    -- Llaves foráneas (Asegúrate que estas tablas existan primero)
    FOREIGN KEY (str_caja) REFERENCES Caja (num_caja),
    FOREIGN KEY (str_tractor) REFERENCES Transporte (uk_num_unidad)
);

-- 2. Índices de Rendimiento (Cruciales para que el Dashboard sea rápido)
-- Este índice permite que el GROUP BY uk_ref sea instantáneo
CREATE INDEX IF NOT EXISTS idx_bitacora_ref ON Bitacora_Eventos (uk_ref);

-- Este índice ayuda a ordenar los embarques más recientes primero
CREATE INDEX IF NOT EXISTS idx_bitacora_fecha ON Bitacora_Eventos (fecha);


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
     FOREIGN KEY (str_caja) REFERENCES Caja (num_caja)
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