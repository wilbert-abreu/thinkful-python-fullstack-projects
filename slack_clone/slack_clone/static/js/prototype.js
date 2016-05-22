var Slackful = function() {
    this.pusher = New Pusher('b568462b35424532aa89');
    this.messagesChannel = this.pusher.subscribe('messages');


    this.chatbox = $('div#chatbox')
    this.channelList = $('.channel-list')

    this.submitMsgButton = $('#submitmsg')

    this.messageInputText = $('input#usermsg')

    this.currentChannel = $('input#current-channel')

    this.channelListItem = $('.channel-list li span')

    this.channelName = $('#channel-name')

    this.messagesChannel.bind('new_message', this.pusherNewMessage.bind(this));

    this.channel = this.pusher.subscribe('channels');

    this.channel.bind('new_channel', this.pusherNewChannel.bind(this));

    this.channel.bind('delete_channel', this.pusherDeleteChannel.bind(this));

    this.submitMsgButton.on('click', this.submitMessage.bind(this));

    this.channelList.on('click','li', this.clickChannel.bind(this));

    this.channelList.on('click','li .glyphicon-remove-sign', this.deleteChannel.bind(this));

    this.channelList.on("mouseenter", "li", this.showDeleteIcon.bind(this)).on("mouseleave", "li", this.hideDeleteIcon.bind(this));

    this.getMessages();
	this.getChannels();
};

Slackful.prototype = {

    pusherNewMessage: function(data) {
        var username =  data.username;
        var time_stamp = data.time;
        time_stamp  = moment.utc(time_stamp).toDate();
        time_stamp = moment(time_stamp).format('h:mm A');
        var message_text = this.buildMessage(username, time_stamp, data.message);
        this.chatbox.append(message_text);
    },

    pusherNewChannel: function(data) {
        console.log('realtime channel update');
        var channel_name =  data.channel_name;
        var channel_text = this.buildChannel(channel_name);
        this.channelList.append(channel_text);
    },

    pusherDeleteChannel: function(data) {
        var channel_name =  data.channel_name;
        this.channelListItem.filter(function() {
          return $.text([this]) === channel_name; }).parent().remove();
    },

    submitMessage: function () {
        var text = this.messageInputText.val();
        this.messageInputText.val('');
        var channel = this.currentChannel.val();
        $.post('/messages', {'message': text,'current-channel':channel }).success
        (function(){
          console.log('Message sent!');
          this.scrollToBottom();
      };
    },

    scrollToBottom: function() {
        this.chatbox.scrollTop(this.chatbox[0].scrollHeight);
    },

    clickChannel: function(e) {
        if($(e.target).closest(".glyphicon-remove-sign").length > 0) {
            return false;}
        var channel_name = $(this).find('span').text();
        this.channelName.text(channel_name);
        this.currentChannel.val(channel_name);
        this.chatbox.html('');
        this.getMessages();
    },

    getMessages: function() {
        var channel_name = this.currentChannel.val();
        this.channelName.text(channel_name);
        $.get('/messages', {'channel_name': channel_name}).success(function(data){
            $.each(data, function(key, value) {
                var username =  data[key].display_name;
                var time_stamp = data[key].time_stamp;

                if (key === 0) {
                    var message_date = data[key].time_stamp;
                    message_date  = this.getMonthDayFromUTC(message_date);
                    console.log(message_date);
                    var first_date = "<div class='day_divider sticky-element'><hr" +
                    " role='separator'><div class='day_divider_label'>" + message_date + "</div>";
                    this.chatbox.append(first_date);
                }else if (this.getMonthDayFromUTC(data[key].time_stamp) != this.getMonthDayFromUTC(data[key-1].time_stamp)){
                    var message_date = data[key].time_stamp;
                    message_date  = this.getMonthDayFromUTC(message_date);
                    var first_date = "<div class='day_divider sticky-element'><hr" +
                    " role='separator'><div class='day_divider_label'>" + message_date + "</div>";
                    this.chatbox.append(first_date);
                };

                var time_stamp  = moment.utc(time_stamp).toDate();
                time_stamp = moment(time_stamp).format('h:mm A');
                var message_text = this.buildMessage(username, time_stamp,
                data[key].content)
                this.chatbox.append(message_text);
            });
            this.scrollToBottom();
        });
    },

    this.getMonthDayFromUTC = function(message_date) {
        var message_date  = moment.utc(message_date).toDate();
        message_date = moment(message_date).format('MMMM Do');
        return message_date;
    },

    this.buildMessage = function(username, time_stamp, message) {
        var message_text = "<div class='message'><a href='#' class='message_profile-pic'></a><a href='#' class='message_username'>" + username + "</a><span class='timestamp'>" + time_stamp + "</span><span class='message-text'>" + message + "</span></div>";
        return message_text;
    },

    this.buildChannel = function(channel_name) {
        var channel_text = "<li>#  <span>" + channel_name +
					"</span><a><i class='glyphicon glyphicon-remove-sign'></i></a></li>";
        return channel_text;
    },

    this.deleteChannel = function() {
        var channel_name = $(this).closest('li').find('span').text();
        console.log(channel_name);
        if (channel_name === this.currentChannel.val()){
            this.currentChannel.val('');
        };
        $.ajax({
            url: '/channel',
            type: 'DELETE',
            data: {'current-channel':channel_name }
        }).done
            (function(){
                this.channelListItem.filter(function() {
                    return $.text([this]) === channel_name; }).parent().remove();
            }).fail
            (function(){
                console.log('Channel Not Deleted!');
            });
    },

    showDeleteIcon: function() {
        $(this).find('i').css({'display':'block'});
    },

    hideDeleteIcon: function{
        $(this).find('i').css({'display':'none'});
    }
};

$(document).ready(function(){
    window.app = new Slackful();
});