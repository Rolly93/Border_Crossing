import { enableInput, filterTable } from "./utils.js";

export function EditShipment() {
    const form = document.querySelector(".shipment-content");
    const inputs = form.querySelectorAll("input");
    inputs.forEach(input => {
        input.readOnly = false;
        input.style.backgroundColor = "white";
    });
}

export async function  getShipmentData(transRef) {
    try {
        const response =  await fetch(`/api/updateShipment/${transRef}`)
        if (!response.ok) throw new Error("Something Went Wrong")
        
        const data = await response.json();
        
        setupEditModal(data)
        
    } catch (error) {
        console.error(error)
    }
    
}

 export async function getShipmentiD(refId) {
    const layout = document.getElementById("layout");
    const form = layout.querySelector(".shipment-content");
    
    layout.style.display = "flex";

    const allInputs = form.querySelectorAll("input");
    allInputs.forEach(input => {
        input.value = "";

         enableInput(input)

    });

    try {
        const response = await fetch(`/api/updateShipment/${refId}`);
        if (!response.ok) throw new Error("Could not fetch shipment");
        
        const data = await response.json();

        // 2. Map the JSON data to the form inputs
        Object.keys(data).forEach(key => {
            const input = form.querySelector(`[name="${key}"]`);
            if (input) {
                let rawValue = data[key] ? data[key].toString().trim() : "";

                if (input.type === "datetime-local" && rawValue) {
                    const parts = rawValue.split(" "); 
                    
                    if (parts.length === 2) {
                        const dateParts = parts[0].split("/"); 
                        if (dateParts.length === 3) {
                            // Convert MM/DD/YYYY to YYYY-MM-DD for the browser picker
                            const formattedDate = `${dateParts[2]}-${dateParts[0].padStart(2, "0")}-${dateParts[1].padStart(2, "0")}T${parts[1]}`;
                            input.value = formattedDate;
                        }
                    }
                } else {
                    input.value = rawValue;
                }
                
                if (input.value !== "") {
                    input.readOnly = true;
                    input.style.backgroundColor = "#f0f0f0";
                }
            }
        });
    } catch (error) {
        console.error("Error fetching shipment:", error);
    }
}




const editForm = document.getElementById("editShipmentForm");
let originalData = {};



export function setupEditModal(data){originalData= data}
const timelineOrder = [
    "fecha_llegada",     
    "fecha_salida", 
    "inspeccion_mex", 
    "verde_Mex", 
    "inspecccion_usa", 
    "verde_usa", 
    "fecha_finalizacion"
]


editForm.addEventListener('submit',function(e){
    e.preventDefault();

    let lastDateValue = null;
    let lastName = "";

    for (const fieldName of timelineOrder){
        const input = editForm.querySelector(`[name="${fieldName}"]`);

        if(!input|| !input.value ) continue

        const currentDateValue = new Date(input.value);

        
        if (lastDateValue && currentDateValue <= lastDateValue  ){
             alert(`Error: La fecha en ${fieldName} no puede ser  menor o igual a ${lastName}.`)
             return;
            }
            
            lastDateValue = currentDateValue;
            lastName = fieldName;
        }
        const formData = new FormData(editForm);
        const updatedData = {}
        
        
        updatedData['trans_ref'] = document.getElementById('edit_trans_ref').value
        
        formData.forEach((value,key) =>{
            
            if (value !== originalData[key] && key !== 'trans_ref'){
                updatedData[key]=value;
            }
        })
    fetch(editForm.action,{
        method:'POST',
        headers:{
            'Content-Type' : 'application/json'
        },
        body:JSON.stringify(updatedData)
    
    
    }).then(response =>{
        if (response.ok){
            return response.json();
        }else{
            throw new Error("Error al actuaizar el embarque")
        }
    }).then(data =>
        {
        console.log(data)
        if (data.action === 'redirect'){
            window.location.href = data.url
        }
    }).catch(error=>{
        console.error("Error en el fetch:",error)
    })})
