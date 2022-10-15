#Import dependencies
from os import TMP_MAX
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #define the previous year from the last date
    year_prev = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #query the date and prcp from the last year of the dataset
    year_prcp = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= year_prev).all()
    #end the session
    session.close()
    #Create a dict where the date is the key for each prcp value
    year_prcp_result = {date: prcp for date, prcp in year_prcp}
    #return results
    return jsonify(year_prcp_result)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    stations_query= session.query(Station.station,Station.name,\
        Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = []
    for station, name, latitude, longitude, elevation in stations_query:
        stations_dict = {}
        stations_dict["elevation"] = elevation
        stations_dict["longitude"] = longitude
        stations_dict["latitude"] = latitude
        stations_dict["name"] = name
        stations_dict["station"] = station
        all_stations.append(stations_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    year_prev = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_query = session.query(measurement.date,measurement.tobs).\
        filter(measurement.date >= year_prev, measurement.station == 'USC00519281').\
         order_by(measurement.tobs).all()


    tobs_result = {date: tobs for date, tobs in tobs_query}

    session.close()
    return jsonify(tobs_result)


#Inform python how to run the program
if __name__ == '__main__':
    app.run(debug=True)