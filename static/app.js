$(document).ready(function () {
    const $questionInput = $('#question');
    const $messages = $('#messages');
    const $sendBtn = $('#send-btn');

    $sendBtn.click(function () {
        sendMessage();
    });

    $questionInput.keypress(function (e) {
        if (e.which == 13) {
            sendMessage();
        }
    });

    function sendMessage() {
        const question = $questionInput.val().trim();
        if (question === '') return;

        addMessage('user', question);
        $questionInput.val('');
        scrollToBottom();

        $.ajax({
            type: 'POST',
            url: '/chat',
            contentType: 'application/json',
            data: JSON.stringify({ question: question }),
            success: function (response) {
                if (response && response.answer) {
                    addMessage('bot', response.answer);
                } else {
                    addMessage('bot', 'Sorry, I did not understand the response.');
                }
                scrollToBottom();
            },
            error: function (xhr, status, error) {
                const errorMessage = xhr.responseJSON ? xhr.responseJSON.detail : error;
                addMessage('bot', `Sorry, I encountered an error: ${errorMessage}`);
                scrollToBottom();
            }
        });
    }

    function addMessage(role, text) {
        $messages.append(`<div class="message ${role}">${text}</div>`);
    }

    function scrollToBottom() {
        $messages.scrollTop($messages[0].scrollHeight);
    }
});
