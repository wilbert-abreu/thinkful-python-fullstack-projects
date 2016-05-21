$(function(){
        var pusher = new Pusher('b568462b35424532aa89');
        var messagesChannel = pusher.subscribe('messages');

        messagesChannel.bind('new_message', function(data){
            var username =  data.username;
            var time_stamp = data.time;
            time_stamp  = moment.utc(time_stamp).toDate();
            time_stamp = moment(time_stamp).format('h:mm A');
            var message_text = buildMessage(username, time_stamp, data.message);
            $('div#chatbox').append(message_text);
        });

        var Channel = pusher.subscribe('channels');

        Channel.bind('new_channel', function(data){
            console.log('realtime channel update');
            var channel_name =  data.channel_name;
            var channel_text = buildChannel(channel_name);
           $('.channel-list').append(channel_text);
        });

        Channel.bind('delete_channel', function(data){
            var channel_name =  data.channel_name;
           $('.channel-list li span').filter(function() {
               return $.text([this]) === channel_name; }).parent().remove();
        });





       $('#submitmsg').on('click', function () {
                  var text = $('input#usermsg').val();
                  $('input#usermsg').val('');
                  var channel = $('input#current-channel').val();
                  $.post('/messages', {'message': text,'current-channel':channel }).success
                  (function(){
                    console.log('Message sent!');
                      scrollToBottom();
                });
       });

        $('.channel-list').on("click",'li', function(e) {
            if($(e.target).closest(".glyphicon-remove-sign").length > 0) {
                return false;}
            var channel_name = $(this).find('span').text();
            $('#channel-name').text(channel_name);
            $('input#current-channel').val(channel_name);
             $('div#chatbox').html('');
            getMessages();
        });

    function getChannels(){
        $.get('/channel').success(function(data){
                $.each(data, function(key, value) {
                    var channel_name = data[key].channel_name;
					var channel_text = buildChannel(channel_name);
                    $('.channel-list').append(channel_text);
                });
            });
    }


    function getMessages(){
            var channel_name = $('input#current-channel').val();
            $('#channel-name').text(channel_name);
            $.get('/messages', {'channel_name': channel_name}).success(function(data){
                $.each(data, function(key, value) {
                    var username =  data[key].display_name;
                    var time_stamp = data[key].time_stamp;

                    if (key === 0) {
                        var message_date = data[key].time_stamp;
                        message_date  = getMonthDayFromUTC(message_date);
                        console.log(message_date);
                        var first_date = "<div class='day_divider sticky-element'><hr" +
                        " role='separator'><div class='day_divider_label'>" + message_date + "</div>";
                        $('div#chatbox').append(first_date);
                    }else if (getMonthDayFromUTC(data[key].time_stamp) != getMonthDayFromUTC(data[key-1].time_stamp)){
                        var message_date = data[key].time_stamp;
                        message_date  = getMonthDayFromUTC(message_date);
                        var first_date = "<div class='day_divider sticky-element'><hr" +
                        " role='separator'><div class='day_divider_label'>" + message_date + "</div>";
                        $('div#chatbox').append(first_date);
                    };

                    var time_stamp  = moment.utc(time_stamp).toDate();
                    time_stamp = moment(time_stamp).format('h:mm A');
					var message_text = buildMessage(username, time_stamp, data[key].content)
                        //"<div class='message'><a href='#' class='message_profile-pic'></a><a href='#' class='message_username'>" + username + "</a><span class='timestamp'>" + time_stamp + "</span><span class='message-text'>" + data[key].content + "</span></div>";
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

    function getMonthDayFromUTC(message_date) {
        var message_date  = moment.utc(message_date).toDate();
        message_date = moment(message_date).format('MMMM Do');
        return message_date;
    };


    function buildMessage(username, time_stamp, message){
        var message_text = "<div class='message'><a href='#' class='message_profile-pic'></a><a href='#' class='message_username'>" + username + "</a><span class='timestamp'>" + time_stamp + "</span><span class='message-text'>" + message + "</span></div>";
        return message_text;
    };

    function buildChannel(channel_name) {
        var channel_text = "<li>#  <span>" + channel_name +
					"</span><a><i class='glyphicon glyphicon-remove-sign'></i></a></li>";
        return channel_text;
    }



    $('.channel-list').on("click",'li .glyphicon-remove-sign', function(){
        var channel_name = $(this).closest('li').find('span').text();
        console.log(channel_name);
        if (channel_name === $('input#current-channel').val()){
            $('input#current-channel').val('');
        };

        $.ajax({
            url: '/channel',
            type: 'DELETE',
            data: {'current-channel':channel_name }
        }).done
            (function(){
                $('.channel-list li span').filter(function() {
               return $.text([this]) === channel_name; }).parent().remove();
            }).fail
            (function(){
            console.log('Channel Not Deleted!');
            });
       });

    $(".channel-list").on("mouseenter", "li", function(){
        $(this).find('i').css({'display':'block'});
    }).on("mouseleave", "li", function(){
        $(this).find('i').css({'display':'none'});
    });





});