import os

import paramiko
import io
from xml.dom import minidom
from .shipment_logic import type_event , time_format
import time
import backend.exception.exceptions as DuplicatedEventError

def eventcreador(event):
    """funccion para reorganizar los eventos y enviar eventos de exportacion via sftp
    """
    event = type_event(event)
    
    for shipment_event in event:

        export_to_xml(shipment_event)
    
    

def export_to_xml(event):
    
    savapath = os.path.join(os.getcwd(), 'exported_events')
    if not os.path.exists(savapath):
        os.makedirs(savapath)
    
    try:
        
        avisoEventos =minidom.Document()

        root = avisoEventos.createElement('AvisoEventos')
        avisoEventos.appendChild(root)
        root.setAttribute('ReferenciaExpd', event.get('cliente_ref', ''))
        root.setAttribute('TipoOperacion','2')
        root.setAttribute('CodigoTransportista',event.get('scac', ''))
        root.setAttribute('ReferenciaTransportista', event.get('trans_ref', ''))
        root.setAttribute('CodigoEvento', event.get('Codigo_evento', ''))
        root.setAttribute('FechaHoraEvento', event.get('event_date', ''))
        root.setAttribute('Comentarios', event.get('description', ''))
        
        xml_str = avisoEventos.toprettyxml(indent="\t", encoding="UTF-8")
        
        scac = str(event.get('scac', '')).upper()
        evento = event.get('Codigo_evento', '').upper()
        cliente_ref = event.get('cliente_ref', '').upper()
        format_time = time_format()
        filename = f"{scac}_{cliente_ref}_{evento}_{format_time}.xml"
        
        event_prefix = f"{scac}_{cliente_ref}_{evento}_"
        if isduplicate(event_prefix):
            raise Exception(f"Evento duplicado: {filename} ya fue exportado.")     
        
        
        format_time = time_format()
        
        fullpath = os.path.join(savapath, filename) 

        with open(fullpath, 'wb') as f:
            f.write(xml_str)
            f.close()
        sent_Sftp_file( fullpath,filename)

    except Exception as e:
        raise e
    
def isduplicate(event_prefix):
    savapath = os.path.join(os.getcwd(), 'exported_events')
    if not os.path.exists(savapath):
        return False
        
    # Listamos los archivos y vemos si alguno EMPIEZA con nuestro prefijo
    existing_files = os.listdir(savapath)
    for f in existing_files:
        if f.startswith(event_prefix):
            print(f"Duplicado encontrado: {f}")
            return True
            
    return False


def sent_Sftp_file( fullpath,filename):

    host = 'localhost'
    port = 2222
    username = 'tester'
    password = 'password'


    file_path = fullpath

    try:

        transport = paramiko.Transport((host, port ))
        transport.connect(username=username, password=password)    

        remote_path = f"./events/{filename}"

        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(file_path,remote_path)
        sftp.close()
        print("File uploaded successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
            transport.close()