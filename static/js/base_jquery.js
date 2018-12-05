/* Initialization: Enables all tooltips. Set datatable option. Set carousel interval. */
$(document).ready(function(){
    $('#ticketTable').DataTable({
        'autoWidth':true,
        'responsive':true,
        'responsive': {
            details: false
        },
        drawCallback: function () {
            $('[data-toggle="tooltip"]').tooltip();
        }
    });
    $('[data-toggle="tooltip"]').tooltip();
    $('.carousel').carousel({
        interval: 7000
    });
});

/* Sets the referencing href when confirming a deletion in a modal */
$('#confirmationModal').on('show.bs.modal', function (e) {
  var my_href = $(e.relatedTarget).attr('data-href');
  $('#modalForm').attr('action',my_href);
});