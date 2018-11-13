/*Enables all tooltips*/
$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});

/*Sets the duration for each slide of the carousel*/
$(document).ready(function() {
  jQuery.fn.carousel.Constructor.TRANSITION_DURATION = 5000  // 5 seconds
});

/*Sets the referencing href when confirming a deletion in a modal*/
$('#confirmationModal').on('show.bs.modal', function (e) {
  var my_href = $(e.relatedTarget).attr('data-href');
  $('#modalForm').attr('action',my_href);
});

/*$(window).on('load',function(){
    console.log("Finished loading page.");
    $('#loader').hide();
});*/