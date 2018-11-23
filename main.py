from flask import Flask, render_template, request
import config
import requests
import time

app = Flask(__name__)
app.config.from_object(config)

@app.route("/")
def index():
    sport_center = {
        'ws':{'name':'文山'}, 
        'da':{'name':'大安'}, 
        # 'dt':{'name':'大同'}, 
        'ss':{'name':'松山'}, 
        'xy':{'name':'信義'}, 
        'nh':{'name':'內湖'}, 
        'sl':{'name':'士林'}, 
        'wh':{'name':'萬華'}, 
        'ng':{'name':'南港'}, 
        'jj':{'name':'中正'}, 
        'bt':{'name':'北投'}, 
        'cs':{'name':'中山'}, 
    }
    return render_template('index.html', sport_center=sport_center)

@app.route("/court", methods=['post'])
def court():
    sc = request.form.getlist('sclist')
    date = request.form.get('date').replace(' / ', '-')
    msg = []
    for sportcenter in sc:
        url = "http://booking.tpsc.sporetrofit.com/Location/findAllowBookingList?LID={}SC&categoryId=Badminton&useDate={}"
        url = url.format(sportcenter.upper(), date)
        payload = {
            "nd": time.time(),
            "rows": "100",
            "page": "1",
        }

        res = requests.post(url=url, data=payload)
        # print(res)
        data = res.json()
        # print(data)
        if 'errorMsg' in data:
            msg.append([1, sportcenter])
        else:
            avaliable = list(filter(lambda x:x['allowBooking'] == 'Y', data['rows']))
            if avaliable:
                for row in avaliable:
                    msg.append([row['LIDName'], row['LSIDName'], row['StartTime']['Hours'], row['EndTime']['Hours']])
            else:
                msg.append([2, sportcenter])
        
    return render_template('court.html', messages=msg, date=date)

if __name__ == "__main__":
    app.run()