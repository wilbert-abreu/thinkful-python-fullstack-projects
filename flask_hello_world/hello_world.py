from flask import Flask
import os

# __name__ tells the app where it's being from run from
app = Flask(__name__)


#used to decorate every flask view
#says when you visit '/' or 'hello' say_hi should run
@app.route("/")
@app.route("/hello")
def say_hi():
    # function that returns hello world
    return "Hello World!"

@app.route("/hello/<name>")
# def hi_person(name):
#     return "Hello {}!".format(name.title())
def hello_person(name):
    html= """
        <h1>
            Hello {}!
        </h1>
        <p>
            Here's a picture of a kitten. Awww....
        </p>
        <img src="http://placekitten.com/g/200/400">
    """
    return html.format(name.title())

# Try making a new view called /jedi. In this view, you should work out what a person's Jedi name is, and return it to them as HTML. Your Jedi name is the first three letters of your last name, followed by the first two letters of your first name. So visiting /jedi/beyonce/knowles should tell you that your Jedi name is "knobe".
@app.route("/jedi/<firstname>/<lastname>")
# def hi_person(name):
#     return "Hello {}!".format(name.title())
def jedi_name(firstname,lastname):
    jedi_name = lastname[0:3] + firstname[0:2]
    html= """
        <h1>
            Here's your Jedi name: {}
        </h1>

        <img src="http://vignette2.wikia.nocookie.net/swfans/images/e/e2/Star_Wars_Title_Placeholder_001.jpg/revision/latest?cb=20150312204827" width="500" height="500">
    """
    return html.format(jedi_name.title())


if __name__ == "__main__":
    # app.run(host=environ['IP'],port=int(environ['PORT']))
    app.run(host="0.0.0.0",port=int("8080"))
