from flask import Flask

app = Flask(__name__)

@app.route("/")
def greetings():
  return "<h2>greetings...</h2>"
