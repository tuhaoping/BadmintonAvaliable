from flask import Flask, render_template, request
import config
import requests
import time
import json

app = Flask(__name__)
app.config.from_object(config)

class SportCenter(object):
    '''a Sport Center object'''
    def __init__(self, sc_id, sc_data):
        self.sc_id     = sc_id
        self.name      = sc_data['name']
        self.address   = sc_data['address']
        self.phone     = sc_data['phone']
        self.website   = sc_data['website']
        self.avaliable = sc_data['avaliable']



@app.route("/")
def index():
    with open('./static/data/sc_info.json', 'r', encoding='utf8') as f:
        sc_info = json.load(f)
    sport_center = filter(lambda obj: obj.avaliable == True, [SportCenter(sc_id, sc_data) for sc_id, sc_data in sc_info.items()])
    
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