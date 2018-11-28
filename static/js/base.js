/* Function for showing loading screen */
function showLoader(isLoading) {
    var currentURL = window.location.href;
    var isDashboard = currentURL.includes("/report/dashboard/");

    if (!isDashboard) {
        document.getElementById("loader").style.display = "none";
    } else {
        if (isLoading) {
            document.getElementById("loader").style.display = "block";
        }
        else {
            var now = new Date().getTime();
            var waitTime = 5000; /* 5 secs */
            while (new Date().getTime() < now + waitTime) {
            }
            document.getElementById("loader").style.display = "none";
        }
    }
}

/* Function to show the "Add Credit Card" div the profile section when hitting the button */
function showAddCard() {
    var x = document.getElementById("addCardDiv");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}