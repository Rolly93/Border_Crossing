import uuid
import random
from ..utility.shipment_logic import validate_shipment
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