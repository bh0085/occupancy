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
    return render_template("home.html",  
                           page={"id":"date"},
                           logs = logs)
                                          
    
@app.route('/')
def index():
    logs = session.query(LineData).all()
    return render_template("home.html",
                           page={"id":"home"},
                           logs = logs)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5051)
