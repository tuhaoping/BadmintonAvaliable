from flask import Flask, render_template
import config

app = Flask(__name__)
app.config.from_object(config)

@app.route("/")
def index():
    sport_center = ['文山', '大安', '大同', '松山', '信義', '內湖', '士林', '萬華', '南港', '中正', '北投', '中山']
    return render_template('index.html', sport_center=sport_center)

@app.route("/court/<sc>")
def court(sc):
    return "選擇的場地為{}".format(sc)

if __name__ == "__main__":
    app.run()