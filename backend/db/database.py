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