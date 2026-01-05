from datetime import datetime
from ..exception.exceptions import ShipmentValidationError
import time

def validate_shipment(newData):
    """The 'Bridge' - Validation Logic"""

    
    actual_content = [v.strip() for k, v in newData.items() if k != 'tipo_operacion']
    
    if not any(actual_content):
        raise ShipmentValidationError("No puedes guardar un registro vacío.")
    
    # You can add more bridge rules here (e.g., checking field lengths)
    if len(newData.get('trailer', '')) > 20:
        raise ShipmentValidationError("El número de Trailer es demasiado largo.")



def format_shipment_dates(details):
    """
    conversion de HTML datetime-local a formato de display del Dashboard.
    """
    date_fields = ["fecha_llegada", "fecha_salida", "inspeccion_mex", 
                   "verde_Mex", "inspecccion_usa", "verde_usa", "fecha_finalizacion"]
    
    for key in date_fields:
        if details.get(key):
            try:
                dt = datetime.fromisoformat(details[key])
                details[key] = dt.strftime("%m/%d/%Y %H:%M")
            except ValueError:
                raise ValueError(f"Invalid format for {key}")
    return details


def validate_client_shipment(entry_Shipment):
    """Validates client shipment data."""

    standard_data = {
                    k: (v.replace(" ","").upper() if k =='cliente_ref' else v.strip().upper()) 
                    for k, v in entry_Shipment.items()
                    if v is not None}

    if standard_data['cliente'].upper() == 'EXPEDITORS NLD': 
        if not standard_data['cliente_ref'].upper().startswith('82B') and not standard_data['cliente_ref'].upper().startswith('92B'):
            raise ShipmentValidationError("El cliente Expeditors requiere que la referencia del cliente comience con '92B'.")
        if not len(standard_data['cliente_ref']) == 10:           
            
            raise ShipmentValidationError("La referencia del cliente de Expeditors debe tener exactamente 10 caracteres.")
    
    return standard_data



def format_for_display(date_val):
    """in case that the dates comes with T format from input"""
    k_dates = ["fecha_llegada", "fecha_salida", "inspeccion_mex", 
               "verde_Mex", "inspecccion_usa", "verde_usa", "fecha_finalizacion"]

    
    for key in k_dates:
        if date_val.get(key):
            date_val[key] = format_display_helper(date_val[key])
    return date_val

def format_display_helper(date_val):
    if not date_val:
        return ""
    # Si viene como objeto datetime de Python
    if hasattr(date_val, 'strftime'):
        print("Formatting datetime object for display")  # Debugging line
        return date_val.strftime('%m/%d/%Y %H:%M')
    # Si viene como string, asegúrar de cambiar la 'T' por un espacio
    format_date = str(str(date_val).replace("T", " ")[:16]).replace("-", "/")
    
    splitdate = format_date.split(" ")
    if len(splitdate) == 2:
        date_part = splitdate[0]
        time_part = splitdate[1]
        date_components = date_part.split("/")
        if len(date_components) == 3:
            year, month, day = date_components
            formatted_date = f"{month}/{day}/{year} {time_part}"
            return formatted_date
    return format_date

def type_event(shipment):
    """restructuracion de datos para eventos
    
    ROLANDO QUE NO SE TE OLVIDE EXTRAER EL SCAC DE SISTEMA!!!
    
    Keyword diccionario shipment --:
    argument -- description
    Return: arreglo de eventos
    """

    event_mapping = {
        "fecha_llegada": ("AFS","Llegando a Origen"),
        "fecha_salida": ("DPU","Saliendo de Origen"),
        "inspeccion_mex": ("EXR","Inspección en México"),
        "verde_Mex": ("ECC","Liberado en México"),
        "inspecccion_usa": ("ILR","Inspección en USA"),
        "verde_usa": ("CLR","Liberado en USA"),
        "fecha_finalizacion": ("TSC","Entregado en Destino")
    }
    arr_events = []
    for key , (code , description) in event_mapping.items():
        event_date = shipment.get(key)
        if event_date:
            arr_events.append({
                "cliente_ref": shipment.get('cliente_ref', ''),
                "tipo_operacion":"2",
                "SCAC_CODE": shipment.get('scac', ''),  # Reemplaza con el código SCAC real si está disponible
                "trans_ref": shipment.get('trans_ref', ''),
                "Codigo_evento": code,
                "event_date": event_date,
                "description": description
            })
    return arr_events

def time_format():
    """para generar timestamps"""
    actual_time = time.localtime()
    timepo = time.strftime("%Y-%m-%d %H:%M:%S", actual_time)
    
    splitdaytime = timepo.split(" ")
    fecha = splitdaytime[0]    
    fecha = fecha.replace("-","")   
    actual_hour = splitdaytime[1]
    actual_hour = actual_hour.replace(":","")
    timeformat = fecha+actual_hour
    return timeformat