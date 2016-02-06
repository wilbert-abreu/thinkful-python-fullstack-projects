var Chat = React.createClass({

  getInitialState: function() {
    return {
      username: null
    };
  },

  _onName: function(e){
    if (e.nativeEvent.keyCode != 13) return;
    var username = e.target.value;
    this.setState({username: username});
  },

  render: function() {
    return (
      <div>
        <WelcomeView username={this.state.username} _onName={this._onName} />
        <MainView username={this.state.username} />
      </div>
    );
  }

});



var WelcomeView = React.createClass({

  render: function() {

    var view;
    var username = this.props.username;

    if (username) {
      view = <h1>Welcome {username}</h1>
    } else {
      view = <input onKeyPress={this.props._onName} placeholder="Please enter your Twitter username" />
    }

    return view;
  }

});

var MainView = React.createClass({

  getInitialState: function() {
    return {
      messages: []
    };
  },

  componentWillMount: function() {

  this.pusher = new Pusher('b568462b35424532aa89');
  this.chatRoom = this.pusher.subscribe('messages');

   },

  componentDidMount: function() {

  this.chatRoom.bind('new_message', function(message){
    this.setState({messages: this.state.messages.concat(message)})
  }, this);

   },

  _onMessage: function(e){
  if (e.nativeEvent.keyCode != 13) return;

  var input = e.target;
  var text = input.value;

  // if the text is blank, do nothing
  if (text === "") return;

  var message = {
    username: this.props.username,
    text: text,
    time: new Date()
  }

  $.post('/messages', message).success(function(){
    // reset the input
    input.value = ""
  });

  },


  render: function() {

    if (!this.props.username) var style = {display:'none'}

    return (
      <div style={style}>

      <MessageList messages={this.state.messages}  />

      <input placeholder="Type your message" onKeyPress={this._onMessage} />
    </div>
    );
  }

});


var MessageList = React.createClass({

  render: function() {

    var list = this.props.messages.map(function(message){

      return  (
        <li>
          <img src={"https://twitter.com/"+message
          .username+"/profile_image?size=mini"}/>
          <b>{message.username} - {message.time}</b>
          <p>{message.text}</p>
        </li>
      )

    });

    return (
      <ul>
        {list}
      </ul>
    );
  }

});


React.render(<Chat />, document.getElementById('app'));