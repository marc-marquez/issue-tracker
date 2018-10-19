/*$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});*/

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
});

$(document).ready(function() {
  jQuery.fn.carousel.Constructor.TRANSITION_DURATION = 5000  // 5 seconds
});

$('#confirmationModal').on('show.bs.modal', function (e) {
  var my_href = $(e.relatedTarget).attr('data-href');
  console.log(my_href);
});

/*$(document).on("click","#confirmationModal",function(){
  var myURL = $(this).data('data-href');
  console.log(myURL);
});*/