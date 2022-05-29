import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

# 1. import Flask
from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model use autoamp
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

# 2. Create an app, being sure to pass __name__

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def Welcome():
    print("List all available api routes")
    return(
        "Welcome: <br/>"
        f"Here are the Availeble Routs: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/start <br/>"
        f"/api/v1.0/start/end <br/>"
    )


#Convert the query results to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year = '2016-08-23'
    prcp_result = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > last_year).all()
    pre_list = []

    for date, prcp in prcp_result:
        row = {}
        row["date"] = date
        row["prcp"] = prcp
        pre_list.append(row)
    return jsonify(pre_list)

#Return a JSON list of stations from the dataset. 
    
@app.route("/api/v1.0/stations")
def stations():
   
    stations_result = session.query(Station.station, Station.name).all()
    stations_list = []

    for station, name in stations_result:
        strow = {}
        strow["station"] = station
        strow["name"] = name
        stations_list.append(strow)
    return jsonify(stations_list)

#Query the dates and temperature observations of the most active station for the previous year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year

@app.route("/api/v1.0/tobs")
def tobs():
    last_year = '2016-08-23'
    observations = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date > last_year)
    active_station=[]

    for date,tobs in observations:
        observationsrow={}
        observationsrow["date"]= date
        observationsrow["tobs"] = tobs
        active_station.append(observationsrow)
    return jsonify(active_station)
    
    


#Query the dates and temperature observations of the most active station for the previous year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/<start>")
def startOnly(start):
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    min = func.min(Measurement.tobs).filter(Measurement.station == "USC00519523")
    avg = func.avg(Measurement.tobs).filter(Measurement.station == "USC00519523")
    max = func.max(Measurement.tobs).filter(Measurement.station == "USC00519523")
    temp_results = session.query(min, avg, max).filter(Measurement.date >= start_date).all()
    tempst=[]
    for min, avg, max in temp_results:
        tempstrow={}
        tempstrow["min"]= min
        tempstrow["avg"]= avg
        tempstrow["max"]= max 
        tempst.append(tempstrow)
    return jsonify(tempst)

#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates from the start date through the end date (inclusive).

@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    end_date = dt.date(2017, 8, 23)
    min = func.min(Measurement.tobs)
    avg = func.avg(Measurement.tobs)
    max = func.max(Measurement.tobs)
    start_end_temp_results = session.query(min, avg, max).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    stend=[]

    for min, avg, max in start_end_temp_results:
        stendrow={}
        stendrow["min"]= min
        stendrow["avg"]=avg
        stendrow["max"]=max 
        stend.append(stendrow)
    return jsonify(stend)

if __name__ == "__main__":
    app.run(debug=True)