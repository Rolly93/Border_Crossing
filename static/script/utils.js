
export function setCurrentTime(inputID){
    const input = inputID
    
    if(!input) return;
    
    const now = new Date()
    const offset= now.getTimezoneOffset()*60000;
    const localISOTime = new Date(now - offset).toISOString().slice(0,16)
    input.value = localISOTime;
    
    enableInput(input)
}

export function enableInput(input){
input.readOnly= false
input.style.backgroundColor = "white";

}

export function filterTable() {
    const input = document.getElementById("search");
    const filter = input.value.toLowerCase();
    
    const tableBody = document.querySelector("table tbody");
    const rows = tableBody.getElementsByTagName("tr");

    for (let i = 0; i < rows.length; i++) {
        const row = rows[i];
        const text = row.textContent || row.innerText;

        if (text.toLowerCase().indexOf(filter) > -1) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    }
}