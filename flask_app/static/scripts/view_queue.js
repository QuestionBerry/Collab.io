//If user clicks on Custom status text input, deselect other statuses
function setCustomStatus(){
    var statusElements = document.getElementsByName('status')
    for(var i =0; i<statusElements.length; i++){
        if (statusElements[i].id != 'custom'){
            console.log
            statusElements[i].checked = false;
        }
    }
}
