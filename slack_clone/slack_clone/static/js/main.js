$(function(){
            var pusher = new Pusher('b568462b35424532aa89');
            var messagesChannel = pusher.subscribe('messages');

            messagesChannel.bind('new_message', function(data){
                var username =  data.username
                var time_stamp = data.time
                console.log(username)
                console.log(time_stamp)
                var message_text = username + " " + data.message + " " +
                time_stamp + "<br>";
                $('div#chatbox').append(message_text);
            });

       $('#submitmsg').on('click', function () {
                  var text = $('input#usermsg').val();
                  $('input#usermsg').val("");
                  $.post('/chat', {'message': text}).success(function(){
                    console.log('Message sent!');

                });

                });

});