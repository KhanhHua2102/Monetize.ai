/*
  This is the index.js file, which contains the JavaScript code for a chat bot interface.
  It uses jQuery to interact with the DOM and handle events.
  The code includes functions for sending queries, retrieving recent messages, and displaying them in the chat box.
*/

$(document).ready(function() {
    // Function to get 2 recent messages
    $(getRecentMessages).ready(function() {
        startMessage();
    });

    // Event handler for button click
    $(".chat-action button").click(function(event) {
        event.preventDefault();
        console.log("submit button clicked");
        sendQuery();
    });

    // Event handler for Enter key press
    $(".chat-action input").on("keypress", function(event) {
        if (event.which === 13) {
            event.preventDefault();
            console.log("enter pressed");
            sendQuery();
        }
    });
});

// Displays a loading animation and initial bot message
function startMessage() {
    // Loading animation
    var animation = `
    <div class="loading-messages">
    <div class="loading-dot"></div>
    <div class="loading-dot"></div>
    <div class="loading-dot"></div>
    </div>
  `;
    $('hr').append(animation);

    // Wait for 1 second and then display initial bot message
    function delay(time) {
        return new Promise((resolve) => setTimeout(resolve, time));
    }

    delay(1000).then(() => {
        $(".loading-messages").remove();
        $("#messages-box").append(
            "<div class='messages bot-messages'>" +
            "Hi there, I am Monetize.ai - your personal financial chat bot advisor. I have access to the most recent, accurate and reliable financial data from Yahoo Finance to give you relevant financial information at a glance." +
            "</div>"
        );
        $(".bot-messages").css("visibility", "visible");
    });
}

// Sends user query and displays loading animation
function sendQuery() {
    console.log("sending query");

    let input = $(".chat-action input").val().trim();
    $(".chat-action input").val("");

    if (input != "") {
        $("#messages-box").append(
            "<div class='messages user-messages'>" + input + "</div>"
        );
        $(".user-messages").css("visibility", "visible");
    }
    console.log(input);

    // Loading animation
    var animation = `
    <div class="loading-messages">
    <div class="loading-dot"></div>
    <div class="loading-dot"></div>
    <div class="loading-dot"></div>
    </div>
  `;
    $("#messages-box").append(animation);

    // Post request to gpt
    postRequest(input);
}

// Sends POST request to generate a response
function postRequest(input) {
    console.log("posting request");
    $.post({
        url: "/generate",
        data: JSON.stringify({ prompt: input }),
        contentType: "application/json",
        dataType: "json",
    }).done(function(data) {
        console.log("finished query");
        console.log(data);
        $(".loading-messages").remove();
        $("#messages-box").append(
            "<div class='messages bot-messages'>" + data.response + "</div>"
        );
        $(".bot-messages").css("visibility", "visible");
    });
}

// Retrieves recent messages and displays them in the chat box
function getRecentMessages() {
    console.log("getting recent messages");
    $.get({
        method: "GET",
        url: "/get_messages",
        contentType: "application/json",
        dataType: "json",
    }).done(function(data) {
        console.log("finished getting recent messages");
        console.log(data);
        if (data == null || data == undefined || data.messages == "") {
            console.log("No recent messages");
            return;
        } else {
            console.log("Recent messages");
            messagesLen = Object.keys(data.messages).length;

            if (messagesLen < 2) {
                console.log("No recent messages");
                return;
            }

            userMessage = data.messages['0']['body'];
            if (userMessage != "") {
                $("#messages-box").append(
                    "<div class='messages user-messages'>" + userMessage + "</div>"
                );
                $(".user-messages").css("visibility", "visible");
            }
            botMessage = data.messages['1']['body'];
            if (botMessage != "") {
                $("#messages-box").append(
                    "<div class='messages bot-messages'>" + botMessage + "</div>"
                );
                $(".bot-messages").css("visibility", "visible");
            }

            $("#messages-box").append(
                "<hr id='hr' style='border: 2px solid green; width: 40%; margin: 15px auto;'>"
            );
        }
    });
}

// Sends a request to fetch the portfolio
function portfolio() {
    $.get("/portfolio", function(response) {
        // Handle the response
    });
}