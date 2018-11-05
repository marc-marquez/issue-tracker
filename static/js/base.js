//document.getElementsByClassName("dropdown-item").onclick = function(){showLoader()};

function showPage(isDashboardLoading){
    if (!isDashboardLoading) {
        document.getElementById("loader").style.display = "none";
    } else {
        document.getElementById("loader").style.display = "block";
    }
    //document.getElementById("outer").style.display = "block";
    //document.getElementById("outer").style.opacity = 1;
}

function showLoader(){
    document.getElementById("loader").style.display = "block";
    //document.getElementById("outer").style.display = "none";
    //document.getElementById("outer").style.opacity = 0;
}

function showAddCard() {
    var x = document.getElementById("addCardDiv");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}



//window.onload = function(){ document.getElementById("loader").style.display = "none" }