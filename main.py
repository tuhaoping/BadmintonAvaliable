from flask import Flask
import config

app = Flask(__name__)
app.config.from_object(config)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/court/<sc>")
def court(sc):
    return "選擇的場地為{}".format(sc)

if __name__ == "__main__":
    app.run()