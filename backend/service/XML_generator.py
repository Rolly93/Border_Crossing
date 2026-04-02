import xml.etree.ElementTree as ET
from datetime import datetime
import os

class XMLService():
    """docstring for XMLService."""
    def __init__(self, referencia, tipo_operacion,codigo_transport,ref_transport,codigo_evento,date_time,comments, output_dir="temp/xmltemp/"):

        self.now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        if not os.path.exists(self._output_dir):
            os.makedirs(self._output_dir)
    
    def create_event_file (self, referencia: str,
                           tipo_operacion: str,
                           codigo_transport : str,
                           ref_transport : str,
                           codigo_evento : str ,
                           date_time : str,
                           comments : str)->object:
        """XML Events File Creator
        
        Keyword arguments:
        referencia-- Client refences (92B , 82B) lenght 10 chars.
        tipo_operacion -- 1 Importacion / 2 Exportacion -> str.
        codigo_transport -- SCAC -> len 4 char.
        ref_transport -- supplier reference /track num.
        codigo_evento -- AFS: Arrival  / DPU: departure / ECC: MEX Clearece /   CLR : USA Clearece /  TSC : Delivery.
        date_time -- date and time when it happens.
        comments -- general comments..
        
        Return: File XML with events created.
        """
        
        root = ET.Element("AvisoEventos",{
            "ReferenciaExpd":referencia,
            "TipoOperacion":tipo_operacion,
            "CodigoTransportista":codigo_transport,
            "ReferenciaTransportista":ref_transport,
            "CodigoEvento":codigo_evento,
            "FechaHoraEvento":date_time,
            "Comentarios":comments 
        })
        tree = ET.ElementTree(root)
        file_name = f"{codigo_transport}_{referencia}_{codigo_evento}_{self.now}.xml"
        

    