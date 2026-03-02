from flask import Flask
import threading
import bot

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h2>MT5 Cloud Bot</h2>
    <a href='/start'>Start Bot</a><br>
    <a href='/stop'>Stop Bot</a>
    """

@app.route("/start")
def start():
    t = threading.Thread(target=bot.run_bot)
    t.start()
    return "Bot Started"

@app.route("/stop")
def stop():
    bot.stop_bot()
    return "Bot Stopped"

app.run(host="0.0.0.0", port=8000)
