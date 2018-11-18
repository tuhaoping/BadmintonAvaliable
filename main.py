from flask import Flask, render_template
import config

app = Flask(__name__)
app.config.from_object(config)

@app.route("/")
def index():
    sport_center = [
        {'id':'ws', 'name':'文山'}, 
        {'id':'da', 'name':'大安'}, 
        # {'id':'dt', 'name':'大同'}, 
        {'id':'ss', 'name':'松山'}, 
        {'id':'xy', 'name':'信義'}, 
        {'id':'nh', 'name':'內湖'}, 
        {'id':'sl', 'name':'士林'}, 
        {'id':'wh', 'name':'萬華'}, 
        {'id':'ng', 'name':'南港'}, 
        {'id':'jj', 'name':'中正'}, 
        {'id':'bt', 'name':'北投'}, 
        {'id':'cs', 'name':'中山'}, 
    ]
    return render_template('index.html', sport_center=sport_center)

@app.route("/court/<sc>")
def court(sc):
    return "選擇的場地為{}".format(sc)

if __name__ == "__main__":
    app.run()