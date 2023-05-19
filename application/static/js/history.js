$(document).ready(function() {
    // Get 2 recent messages
    appendChatCard();
});

function appendChatCard() {
    console.log("appending chat card");
    $.get({
        method: "GET",
        url: "/get_history",
        contentType: "application/json",
        dataType: "json",
    }).done(function(data) {
        console.log("finished getting messages");
        console.log(data);

        data.forEach((chat) => {
            $("#body").append(
                "<p class='times'>" + chat.created_at + "</p>"
            );
            $("#body").append(
                '<img src="{{ url_for( "static",filename="img/line.png" )}} ">'
            );
            $("#body").append(
                '<div class="preview "> <p class="preview-content ">' + chat.body + '</p> </div>'
            );
        });
    });
    // const cardBody = $('<div>').addClass('card-body');
    // const timeElement = $('<p>').addClass('time').text(chat.created_at);
    // const lineImage = $('<img>').attr('src', "{{ url_for( 'static', filename='img/line.png' )}}").attr('alt', '');
    // const previewDiv = $('<div>').addClass('preview');
    // const previewContent = $('<p>').addClass('preview-content').text(chat.body);

    // console.log(cardBody, timeElement, lineImage, previewDiv, previewContent)

    // // Append elements to the card body
    // cardBody.append(timeElement, lineImage, previewDiv.append(previewContent));

    // // Create card div and append the card body
    // const card = $('<div>').attr('id', 'card-border').append(cardBody);

    // // Append the card to the container element
    // $('#hello').append(card); // Replace 'container' with your actual container element selector

}

// chats.forEach((chat) => {
//     appendChatCard(chat);
// });