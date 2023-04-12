$(document).ready(function () {
    // Toggle menu
    $('#menu-icon').click(function () {
        $('.menu button').toggle();
    });

    // Send message
    // $('#submit-button').click(function (event) {
    //     event.preventDefault();
    //     console.log("button clicked");
    //     let userMessage = $('#chat-input').val();
    //     console.log(userMessage);
    //     if (userMessage != '') {
    //         $("section").append(
	// 						"<div class=messages>" + userMessage + "</div>");
    //         $('.messages').css('visibility', 'visible');
    //     }
    // });

    // Send message and receive response from gpt
    $("#submit-button").click(function (event) {
        event.preventDefault();
        let input = $("#chat-input").val();
        if (input != '') {
            $("section").append("<div class=messages>" + input + "</div>");
            $('.messages').css('visibility', 'visible');
        }
        console.log(input);

        // Post request to gpt
        $.post({
            url: "http://127.0.0.1:8080/generate",
            data: JSON.stringify({ prompt: input }),
            contentType: "application/json",
            dataType: "json",
        }).done(function (data) {
            console.log("finished query");
            console.log(data);
            $("section").append("<div class=messages>" + data.response + "</div>");
            $(".messages").css("visibility", "visible");
        });
    });
});

