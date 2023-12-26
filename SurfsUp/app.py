# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station



# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """"List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # create session
    session = Session(engine)
    # query the last 12 months
    One_yr_from_most_recent  = '2016-08-23'


    """""Return a list of the precipitation data alongside the date"""
    # Query all the precipitation and date
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > One_yr_from_most_recent).all()
    session.close()

    #  turn list of tuples into a dictionary

    precip_data=[]
    for date,prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precip_data.append(precipitation_dict)
    
    return jsonify(precip_data)


# app routing for station list
@app.route("/api/v1.0/stations")
def stations():
    # create session
    session = Session(engine)

    """"Return a list of stations"""
    # query stations
    results = session.query(Measurement.station).distinct().all()
    session.close()

    # dictionary for active stations
    station_list=[]
    for station in results:
        station_dict = {}
        station_dict["station name"] = station[0]
        station_list.append(station_dict)

    return jsonify(station_list)

# app routing for observed temperatures
@app.route("/api/v1.0/tobs")
def temperature_obs():
    # create session
    session = Session(engine)

    # query the last 12 months of temp data from the most active station
    One_yr_from_most_recent = '2016-08-23'
    
    results = session.query(Measurement.date, Measurment.tobs).filter((Measurement.station == 'USC00519281') 
                & (Measurement.date > One_yr_from_most_recent)).all()
    session.close()

    # create dictionary of the temperature_obs for the most active station
    temperature_obs_data = []
    for date, temperature_obs in results:
        temp_obs_dict = {}
        temp_obs_dict["Date"] = date
        temp_obs_dict["Temperature Observed"] = temperature_obs
        temperature_obs_data.append(temp_obs_dict)
    
    return jsonify(temperature_obs_data)

# app routing for min, max, avg temp for a given start date
@app.route("/api/v1.0/start")
def temps_start(start):
    session = Session(engine)

    results = session.query(func.avg(Measurement.tobs),func.min(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    temp_data = []
    for temperature_obs in results:
        temp_dict = {}
        temp_dict["Average"] = results[0][0]
        temp_dict["Minimum"] = results[0][1]
        temp_dict["Maximum"] = results[0][2]
        temp_data.append(temp_dict)

    return jsonify(temp_data)

# app routing for min, max, avg temp through the end date
@app.route("/api/v1.0/start/end")
def temp_start_end(start=None, end=None):
    session = Session(engine)                  

    results = session.query(func.avg(Measurement.tobs),func.min(Measurement.tobs),func.max(Measurement.tobs)).\
        filter((Measurement.date >= start) & (Measurement.date <= end)).\
        all()  

    temp_data = []
    for temperature_obs in results:
        temp_dict = {}
        temp_dict["Average"] = results[0][0]
        temp_dict["Minimum"] = results[0][1]
        temp_dict["Maximum"] = results[0][2]
        temp_data.append(temp_dict)

    return jsonify(temp_data)
if __name__== '_main_':
    app.run(debug=True)

