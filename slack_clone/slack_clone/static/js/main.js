$(function(){
            var pusher = new Pusher('b568462b35424532aa89');
            var messagesChannel = pusher.subscribe('messages');

            messagesChannel.bind('new_message', function(data){
                var username =  data.username;
                var time_stamp = data.time;
                var message_text = username + " " + data.message + " " +
                time_stamp + "<br>";
                $('div#chatbox').append(message_text);
            });

       $('#submitmsg').on('click', function () {
                  var text = $('input#usermsg').val();
                  $('input#usermsg').val("");
                  var channel = $('input#current-channel').val();
                  $.post('/messages', {'message': text,'current-channel':channel }).success
                  (function(){
                    console.log('Message sent!');
                });

                });

       $('.glyphicon-plus').on('click', function () {
                  var text = $('input#usermsg').val();
                  $('input#usermsg').val("");
                  var channel = $('input#current-channel').val();
                  $.post('/messages', {'message': text,'current-channel':channel }).success
                  (function(){
                    console.log('Message sent!');
                });

                });

        $('.channel-list li').on("click", function(){
            var channel_name = $(this).text();
            $('#channel-name').text(channel_name);
            $("input#current-channel").val(channel_name);
             $('div#chatbox').html("")
            getMessages();
        });

    function getMessages(){
            var channel_name = $('input#current-channel').val()
            $('#channel-name').text(channel_name);
            $.get('/messages', {'channel_name': channel_name}).success(function(data){
                $.each(data, function(key, value) {
                    var username =  data[key].display_name;
                    var time_stamp = data[key].time_stamp;
                    var message_text = username + " " + data[key].content + " " +
                    time_stamp + "<br>";
                    $('div#chatbox').append(message_text);
                });
            });
    };

    getMessages();

});