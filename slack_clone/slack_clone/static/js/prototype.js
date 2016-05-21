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

    $('#submitmsg').on('click', );
};

Slackful.prototype = {

    pusherNewMessage: function(data){
        var username =  data.username;
        var time_stamp = data.time;
        time_stamp  = moment.utc(time_stamp).toDate();
        time_stamp = moment(time_stamp).format('h:mm A');
        var message_text = this.buildMessage(username, time_stamp, data.message);
        this.chatbox.append(message_text);
    };

    pusherNewChannel: function(data){
        console.log('realtime channel update');
        var channel_name =  data.channel_name;
        var channel_text = this.buildChannel(channel_name);
        this.channelList.append(channel_text);
    };

    pusherDeleteChannel: function(data){
        var channel_name =  data.channel_name;
        this.channelListItem.filter(function() {
          return $.text([this]) === channel_name; }).parent().remove();
    }:

    submitMessage: function () {
        var text = this.messageInputText.val();
        this.messageInputText.val('');
        var channel = this.currentChannel.val();
        $.post('/messages', {'message': text,'current-channel':channel }).success
        (function(){
          console.log('Message sent!');
          scrollToBottom();
      };
    }
};


$(document).ready(function(){
    window.app = new Slackful();
});