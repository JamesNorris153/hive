function new_transaction(sender, recipient, amount) {

	sender = $(sender).val();
	recipient = $(recipient).val();
	amount = $(amount).val();

	if (sender == "") {
		$(sender).addClass("is-danger");
	} else {
		$(sender).removeClass("is-danger");
	}

	if (recipient == "") {
		$(recipient).addClass("is-danger");
	} else {
		$(recipient).removeClass("is-danger");
	}

	if ($(sender).parent().find('.is-danger').length != 0) {
		return false;
	}

	$.post("/new_transaction", {sender:sender, recipient:recipient, amount:amount},
	function(data) {
		if (data == "Success") {
			window.location.href = "/new_transaction";
		} else {
			$("#register_error").html(data);
		}
	});

	return false;

}

function get_chain() {
	$.get("/get_chain", function(data) {
		if (data == "Success") {
			window.location.href = "/new_transaction";
		} else {
			$("#register_error").html(data);
		}
	});

	return false;

}
