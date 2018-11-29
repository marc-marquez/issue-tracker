/* Enables all tooltips */
$(document).ready(function(){
    $('#ticketTable').DataTable({
        'autoWidth':true,
        'responsive':true,
        'columnDefs': [
            {responsivePriority: 3, targets: 0},
            {responsivePriority: 1, targets: 1},
            {'width': '30%', targets: 1},
            {responsivePriority: 6, targets: 2},
            {responsivePriority: 7, targets: 3},
            {responsivePriority: 5, targets: 4},
            {responsivePriority: 2, targets: 5},
            {responsivePriority: 4, targets: 6},
            {'width': '5%', targets: 6},
        ],
        drawCallback: function () {
            $('[data-toggle="tooltip"]').tooltip();
        }
    });
    $('[data-toggle="tooltip"]').tooltip();
});

/* Sets the duration for each slide of the carousel */
$(document).ready(function() {
  jQuery.fn.carousel.Constructor.TRANSITION_DURATION = 5000  // 5 seconds
});

/* Sets the referencing href when confirming a deletion in a modal */
$('#confirmationModal').on('show.bs.modal', function (e) {
  var my_href = $(e.relatedTarget).attr('data-href');
  $('#modalForm').attr('action',my_href);
});