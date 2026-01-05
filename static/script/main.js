import { filterTable , setCurrentTime , enableInput} from './utils.js';
import { getShipmentiD ,setupEditModal , getShipmentData} from './shipment.js';



    const shipmentRows = document.querySelectorAll("tr.dashboard");
    shipmentRows.forEach((row) => {

        row.addEventListener('dblclick', () => {
            

            const refId = row.cells[0].textContent;
            getShipmentiD(refId);
        });
    });


const editinput = document.querySelectorAll("#editShipmentForm input").forEach((input)=>{
    input.addEventListener("dblclick",(e)=>{
        const transRef = document.querySelector("#edit_trans_ref").value
        const input = e.target;
        enableInput(input)

        getShipmentData(transRef);
    })
})

// esta funcion extrae los botones de 'now' para ingresar el timepo actual
const btnNowTime = document.querySelectorAll(".btn-now")
btnNowTime.forEach((btn)=>{
    btn.addEventListener('click',(e)=>{
        const inputDateTime = e.target.previousElementSibling
        
        setCurrentTime(inputDateTime)
    })
})

const layout = document.getElementById("layout");
const newShipmentModal = document.getElementById("newshipmet");
const btncancel = document.querySelectorAll(".btn-cancel")


document.getElementById("NewShipment").onclick=NewShipment
document.getElementById("search").onkeyup = filterTable



document.querySelectorAll('.btn-edit').forEach(button => {
    button.addEventListener('click', function() {

        const transRef = document.querySelector("#edit_trans_ref").value
        
        console.log(transRef)
        getShipmentData(transRef)
            const enableinput = document.querySelectorAll("#editShipmentForm input").forEach((input)=>{
              enableInput(input)
            })
    });
});





//funcion aplicada para cerrar al momento que seleccionan el boton de cerrar
btncancel.forEach((btn)=>{
    btn.addEventListener('click',(e)=>{

        const divform = e.target.closest('div.form')
        hideShipmentModal(divform)
        divform.style.display = "none";
    })
})



window.addEventListener("click", (e) => {
    if (layout.style.display === "flex" && e.target === layout) {hideShipmentModal(layout);}
    
    if (newShipmentModal.style.display === "flex" && e.target === newShipmentModal) {hideShipmentModal(newShipmentModal);}
});



function  hideShipmentModal(divform) {divform.style.display = "none";}


function NewShipment() {    newShipmentModal.style.display = "flex";}



