from flask import Flask, render_template
import config

app = Flask(__name__)
app.config.from_object(config)

@app.route("/")
def index():
    sport_center = [
        {'cn':'文山', 'en':'ws'}, 
        {'cn':'大安', 'en':'da'}, 
        # {'cn':'大同', 'en':'dt'}, 
        {'cn':'松山', 'en':'ss'}, 
        {'cn':'信義', 'en':'xy'}, 
        {'cn':'內湖', 'en':'nh'}, 
        {'cn':'士林', 'en':'sl'}, 
        {'cn':'萬華', 'en':'wh'}, 
        {'cn':'南港', 'en':'ng'}, 
        {'cn':'中正', 'en':'jj'}, 
        {'cn':'北投', 'en':'bt'}, 
        {'cn':'中山', 'en':'cs'}, 
    ]
    return render_template('index.html', sport_center=sport_center)

@app.route("/court/<sc>")
def court(sc):
    return "選擇的場地為{}".format(sc)

if __name__ == "__main__":
    app.run()