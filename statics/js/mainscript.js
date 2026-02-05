$(document).ready(function (e) {
	$('.nomineeimagediv').mouseenter(function (e) {
		$('.nomineeimageoverlay').show();
	});
	$('.nomineeimagediv').mouseleave(function (e) {
		$('.nomineeimageoverlay').hide();
	});
	$('.nomineeimageoverlay').on('click', function (e) {
		$('.nomineeimage').click();
	});

	$('#reducevotebtn').on('click', function (e) {
		if (parseInt($('#votecount').val()) > 1) {
			$('#votecount').val(parseInt($('#votecount').val()) - 1);
			$('#voteamount').text((parseFloat($('#votecount').val()) * 1.00).toFixed(2));
		}
	});
	$('#increasevotebtn').on('click', function (e) {
		$('#votecount').val(parseInt($('#votecount').val()) + 1);
		$('#voteamount').text((parseFloat($('#votecount').val()) * 1.00).toFixed(2));
	});
});

function upload_nominee_image(input) {
	if (input.files && input.files[0]) {
		var reader = new FileReader();
		reader.onload = function (e) {
			$('.nomineeimagediv img')
				.attr('src', e.target.result)
				.width('100%')
				.height('100%');
		};
		reader.readAsDataURL(input.files[0]);
	}
}

function clear_mem_photograph() {
	$('#nominationform #photograph').val('');
	$('.nomineeimagediv img').prop("src", "/static/images/user.png");

}