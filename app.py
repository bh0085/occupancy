#!/usr/bin/env python

from flask import Flask
from flask import render_template, redirect, request, url_for, session as flask_session

from flask_assets import Environment, Bundle
import dateparser
import datetime
import babel.dates


from db import Session
from flask_sqlalchemy_session import flask_scoped_session
from sqlalchemy import func
import babel

from models import LineData
import json


app = Flask(__name__,static_url_path='/static')
session = flask_scoped_session(Session, app)


assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle( 'base.scss', filters='pyscss', output='all.css')
assets.register('scss_all', scss)


def format_datetime(value, format='short'):
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format="EE dd.MM.y HH:mm"
    elif format == 'short':
        format="MMM d"
    return babel.dates.format_datetime(value, format)

def format_unixtime(seconds):
    dt = datetime.datetime.fromtimestamp(seconds)
    

    hour24 = dt.hour
    minute = dt.minute
    ampm = "AM" if hour24 < 12 else "PM"
    return "{0}{1}{2}".format((int(hour24 )-1)%12 + 1,":{0}".format(int(minute)) if int(minute) !=0 else "", ampm)

def unixtime_hour(seconds):
    dt = datetime.datetime.fromtimestamp(seconds)
    return dt.hour

def weekday(value):
    #date = dateparser.parse(value)
    return babel.dates.format_datetime(value, "EE").lower()
    


app.jinja_env.filters['datetime'] = format_datetime
app.jinja_env.filters['time'] = format_unixtime
app.jinja_env.filters['weekday'] = weekday

@app.route('/date/<date>')
def dateview(date):
    dt = dateparser.parse(date)
    d = datetime.date(dt.year,dt.month,dt.day)
    
    
    logs = session.query(LineData).filter(LineData.date==(d)).all()

    print d
    print logs[0].date
    return render_template("loglist.html",  
                           page={"id":"date"},
                           logs = logs)
                                          
    
@app.route('/')
def index():
    logs = session.query(LineData).order_by(LineData.unixtime).all()

    #cols = [["hour","wait"]]
    #vals = [["{0}:00".format(unixtime_hour(r.unixtime)),r.linewait] for r in logs]
    #chart_data = cols + vals

    import itertools as it


    data = []
    for k1, g1 in it.groupby(sorted(logs, key=lambda x:x.weekday),  key = lambda x: x.weekday ):
        items1 = list(g1)
        for k2, g2 in it.groupby(sorted(items1, key=lambda x:x.hour), key = lambda x: x.hour):
            if k1 != 5: continue

            day_string = "SAT"
            hour_string = "{0}pm".format(k2-12) if k2 >12 else "{0}am".format(k2)

            items2 = list(g2)
            data.append(["{0} {1}".format(day_string,hour_string), sum(e.linewait for e in items2)/len(items2)])

    chart_data = [["Hour interval","Average wait time"]] + data
    
    return render_template("home.html",
                           page={"id":"home"},
                           logs = logs,
                           chart_data=json.dumps(chart_data))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5051)
