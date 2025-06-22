from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send


# setup Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "tp2"
socketio = SocketIO(app)


# rotas da aplicação

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app, "0.0.0.0", 5000)
