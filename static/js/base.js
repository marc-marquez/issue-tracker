/* Function to show loading screen */
function showLoader(isPageLoading,isJSLoading) {
    var currentURL = window.location.href;
    var isDashboard = currentURL.includes('/report/dashboard/');

    if (isDashboard) {
        if (isJSLoading) {
            document.getElementById('loader').style.display = 'block';
        }
        else {
            document.getElementById('loader').style.display = 'none';
        }
    }
    else {
        if(isPageLoading){
            document.getElementById('loader').style.display = 'block';
        }
        else {
            document.getElementById('loader').style.display = 'none';
        }
    }
}

/* Function to show the 'Add Credit Card' div in the profile page when hitting the button */
function showAddCard() {
    var x = document.getElementById('addCardDiv');
    if (x.style.display === 'none') {
        x.style.display = 'block';
    } else {
        x.style.display = 'none';
    }
}