from flask import Flask, render_template, request
import config
import json
import requests
import time
import threading
from queue import Queue


app = Flask(__name__)
app.config.from_object(config)

class SportCenter(object):
    '''a Sport Center object'''
    crawler_url = "http://booking.tpsc.sporetrofit.com/Location/findAllowBookingList?LID={}SC&categoryId=Badminton&useDate={}"
    with open('./static/data/sc_info.json', 'r', encoding='utf8') as f:
        sc_info = json.load(f)

    def __init__(self, sc_id):
        self.sc_id     = sc_id
        self.name      = self.sc_info[sc_id]['name']
        self.address   = self.sc_info[sc_id]['address']
        self.phone     = self.sc_info[sc_id]['phone']
        self.website   = self.sc_info[sc_id]['website']
        self.avaliable = self.sc_info[sc_id]['avaliable']
        self.court_avaliable = []

    @property
    def info(self):
        return [
            self.sc_id,
            self.name,
            self.address,
            self.phone,
            self.website,
            self.avaliable,
            self.court_avaliable,
        ]

    @classmethod
    def all_sport_center(self):
        return self.sc_info

    def avaliable_time_crawler(self, date):
        url = self.crawler_url.format(self.sc_id.upper(), date)
        payload = {
            "nd": time.time(),
            "rows": "100",
            "page": "1",
        }
        data = requests.post(url=url, data=payload).json()
        if 'errorMsg' in data:
            self.court_avaliable.append([1, self.sc_id])
        else:
            avaliable = list(filter(lambda x:x['allowBooking'] == 'Y', data['rows']))
            if avaliable:
                for row in avaliable:
                    self.court_avaliable.append([row['LIDName'], row['LSIDName'], row['StartTime']['Hours'], row['EndTime']['Hours']])
            else:
                self.court_avaliable.append([2, self.sc_id])

        return self

def crawler_threading_task(obj, date):
    obj.avaliable_time_crawler(date)

@app.route("/")
def index():
    
    sport_center = filter(lambda obj: obj['avaliable'] == True, 
        [sc_data for sc_id, sc_data in SportCenter.all_sport_center().items()]
    )
    
    return render_template('index.html', sport_center=sport_center)

@app.route("/court", methods=['post'])
def court():
    sc_query = request.form.getlist('sclist')
    if sc_query[0] == "all":
        sc_query = SportCenter.all_sport_center().keys()
    date = request.form.get('date').replace(' / ', '-')
    
    sport_center = [SportCenter(sc_id) for sc_id in sc_query]
    threads = []
    for sc in sport_center:
        t = threading.Thread(target=crawler_threading_task, args=(sc, date))        
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    return render_template('court.html', sportcenter=sport_center, date=date)

if __name__ == "__main__":
    app.run()