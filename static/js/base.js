function showLoader(isLoading) {
    console.log(window.location.href);
    var currentURL = window.location.href;
    var isDashboard = currentURL.includes("/report/dashboard/");
    console.log("isDashboard = " + isDashboard);

    if (!isDashboard) {
        document.getElementById("loader").style.display = "none";
    } else {
        if (isLoading) {
            document.getElementById("loader").style.display = "block";
        }
        else {
            var now = new Date().getTime();
            console.log(now);
            var waitTime = 5000;
            /* 5 secs */
            while (new Date().getTime() < now + waitTime) {
            }
            console.log(new Date().getTime());
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