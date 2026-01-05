import os
import time
from xml.dom import minidom
from .shipment_logic import type_event , time_format
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
        sent_Sftp_file(event, fullpath)
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
def sent_Sftp_file(event, filepath):
    """Funcion para enviar el archivo via SFTP
    """
    import paramiko

    sftp_host = 'sftp.example.com'
    sftp_port = 22
    sftp_username = 'your_username'
    sftp_password = 'your_password'
    remote_path = '/remote/directory/'

    try:
        transport = paramiko.Transport((sftp_host, sftp_port))
        transport.connect(username=sftp_username, password=sftp_password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        filename = os.path.basename(filepath)
        remote_filepath = os.path.join(remote_path, filename)

        sftp.put(filepath, remote_filepath)

        sftp.close()
        transport.close()
    except Exception as e:
        raise e