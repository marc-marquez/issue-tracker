function showPage(){
    document.getElementById("loader").style.display = "none";
    document.getElementById("outer").style.display = "block";
    document.getElementById("outer").style.opacity = 1;
}

function showAddCard() {
    var x = document.getElementById("addCardDiv");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}