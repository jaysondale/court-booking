$('.cancel-booking').click(function(){
    let bid = $(this).attr('bid');
    $.ajax({url: $(this).attr('action'),
		type: 'post',
		data: {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
			'bid': bid},
		success: function(response) {
				if (response['code'] == 400){
					alert('Error: Bad Request');
				}
				window.location.reload(true);
			}
		});
})