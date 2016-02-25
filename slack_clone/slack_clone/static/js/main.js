$(function(){
            var pusher = new Pusher('b568462b35424532aa89');
            var messagesChannel = pusher.subscribe('messages');

            messagesChannel.bind('new_message', function(data){
                var username =  data.username;
                var time_stamp = data.time;
                var message_text = "<div class='message'><a href='#' class='message_profile-pic'></a><a href='#' class='message_username'>" + username + "</a><span class='timestamp'>" + time_stamp + "</span><span class='message-text'>" + data.message + "</span></div>";
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

        $('.channel-list').on("click",'li span', function(){
            var channel_name = $(this).text();
            $('#channel-name').text(channel_name);
            $("input#current-channel").val(channel_name);
             $('div#chatbox').html("");
            getMessages();
						
        });

    function getChannels(){
        $.get('/channel-list').success(function(data){
                $.each(data, function(key, value) {
                    var channel_name = data[key].channel_name;
					var channel = "<li>#  <span>" + channel_name +
					"</span></li>";
                    $('.channel-list').append(channel);
                });
            });
    }


    function getMessages(){
            var channel_name = $('input#current-channel').val()
            $('#channel-name').text(channel_name);
            $.get('/messages', {'channel_name': channel_name}).success(function(data){
                $.each(data, function(key, value) {
                    var username =  data[key].display_name;
                    var time_stamp = data[key].time_stamp;
                    time_stamp = Date.parse(time_stamp);
                    time_stamp = time_stamp.toString('h:mm tt MM/yy');
					var message_text = "<div class='message'><a href='#' class='message_profile-pic'></a><a href='#' class='message_username'>" + username + "</a><span class='timestamp'>" + time_stamp + "</span><span class='message-text'>" + data[key].content + "</span></div>";
									
									
                    $('div#chatbox').append(message_text);
									
                });
							
							scrollToBottom();
            });
			
				 
    };

    getMessages();
	getChannels();

		function scrollToBottom() {
				$('div#chatbox').scrollTop($('div#chatbox')[0].scrollHeight);
		};
	
		$('.chat-wrapper').on('contentchanged', 'div #chatbox', function() {
  		scrollToBottom();
		});
	
	
});