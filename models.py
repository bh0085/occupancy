#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv

import sqlite3
from decimal import Decimal
from datetime import date, datetime, timedelta
import dateparser


from sqlalchemy.orm import relationship, backref, configure_mappers, synonym
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, Numeric, String, Unicode, Text, Date, DateTime, Time, Boolean, ForeignKey, UniqueConstraint, func
from sqlalchemy.engine import Engine
from sqlalchemy import event

Base = declarative_base()

# enforce foreign keys in sqlite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if type(dbapi_connection) is sqlite3.Connection:
       cursor = dbapi_connection.cursor()
       cursor.execute("PRAGMA foreign_keys=ON")
       cursor.close()


class LineData(Base):
    __tablename__="linedata"
    id = Column(Unicode(255),primary_key=True)
    linewait= Column(Integer)
    linelength = Column(Integer)
    howfull=Column(Unicode(255)) 
    linewait_description= Column(Unicode(255))
    email=Column(Unicode(255))
    date= Column(Date)
    unixtime = Column(Integer)

    

       
def main():  
    print "CURRENTLY ALL DATA INGESTION IS DONE WITH PACKAGE GSHEETS-IO"
    

    

if __name__ == "__main__":
    main()

