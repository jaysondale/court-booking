$('.available').click(function(){
	let court_name = $(this).attr('courtname');
	let court_id = $(this).attr('court');
	let meta_time = $(this).attr('meta');
	$('#court-name').html(court_name);
	$('#booking-time').html($(this).attr('time'));
	$('.modal-action').click(function() {
		$.ajax({url: $(this).attr('action'),
		type: 'post',
		data: {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
			'court': court_id,
			'time': meta_time},
		success: function(response) {
				if (response['code'] == 400){
					alert('Error: Bad Request');
				}
				window.location = response['url']
			}
		});
	});
	$("#confirm-booking-modal").modal('show');
});

if(booking_error === "True") {
	alert("Booking not permitted. Members are entitled to 1 KLM pickleball court " +
	"per day OR 2 HF courts per day at the same time.")
}