# Import the dependencies.
import numpy as np
import re
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.sql import exists  

from flask import Flask, jsonify



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


#################################################
# Flask Setup
#################################################
app = Flask(__name__)




#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return(f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end (enter as YYYY-MM-DD/YYYY-MM-DD)"
)

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date)
    precip_date_tobs = []
    for row in results:
        dt_dict = {}
        dt_dict["date"] = row.date
        dt_dict["tobs"] = row.tobs
        precip_date_tobs.append(dt_dict)

    return jsonify(precip_date_tobs)

@app.route("/api/v1.0/stations")
def stations():
    session = Sessions(engine)
    results = session.query(Station.name).all()
    station_list = list(np.ravel(results))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    latest_date = (session.query(Measurement.date).order_by(Measurement.date.desc()).first())
    latest_date_str = str(latest_date)
    latest_date_str = re.sub("'|,", "",latest_date_str)
    latest_date_obj = dt.datetime.strptime(latest_date_str, '(%Y-%m-%d)')
    query_start_date = dt.date(latest_date_obj.year, latest_date_obj.month, latest_date_obj.day) - dt.timedelta(days=365)
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    station_temp = active_stations[0][0]
    print(station_temp)
    results = (session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.date >= query_start_date).filter(Measurement.station == station_hno).all())
    tobs_list = []
    for result in results:
        line = {}
        line["Date"] = result[1]
        line["Station"] = result[0]
        line["Temperature"] = int(result[2])
        tobs_list.append(line)

    return jsonify(tobs_list)

@app.route("/api/v1.0/start (enter as YYYY-MM-DD)")
def start():
    session = Session(engine)
    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    max_date_string = str(max_date)
    max_date_string = re.sub("'|,", "",max_date_string)
    print (max_date_string)

    min_date = session.query(Measurement.date).first()
    min_date_string = str(min_date)
    min_date_string = re.sub("'|,", "",min_date_string)
    print (min_date_string)

    valid = session.query(exists().where(Measurement.date == start)).scalar()
 
    if valid:

    	results = (session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).all())
tmin = results[0][0]
tavg ='{0:.4}'.format(results[0][1])
tmax = results[0][2]
    
print_result =( ['Enter The Start Date: ' + start,
    						'The lowest Temperature was: '  + str(tmin) + ' F',
    						'The average Temperature was: ' + str(tavg) + ' F',
    						'The highest Temperature was: ' + str(tmax) + ' F'])
return jsonify(print_result)
return jsonify({"error": f"The date inputed {start} is not valid. The date range is {min_date_string} to {max_date_string}"}), 404

@app.route("/api/v1.0/start/<end> (enter as YYYY-MM-DD)")
def start():
    session = Session(engine)
    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    max_date_string = str(max_date)
    max_date_string = re.sub("'|,", "",max_date_string)
    print (max_date_string)

    min_date = session.query(Measurement.date).first()
    min_date_string = str(min_date)
    min_date_string = re.sub("'|,", "",min_date_string)
    print (min_date_string)

    valid = session.query(exists().where(Measurement.date == start)).scalar()
    valid_end = session.query(exists().where(Measurement.date == end)).scalar()

 
    if valid and valid_end:

    	results = (session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date<= end).all())
tmin =results[0][0]
tavg ='{0:.4}'.format(results[0][1])
tmax =results[0][2]
    
print_result =( ['Enter The Start Date: ' + start,
    						'The lowest Temperature was: '  + str(tmin) + ' F',
    						'The average Temperature was: ' + str(tavg) + ' F',
    						'The highest Temperature was: ' + str(tmax) + ' F'])
    return jsonify(print_result)
    
        if not valid and not valid_end:
return jsonify({"error": f"Input Start {start} and End Date {end} not valid. Date Range is {min_date_string} to {max_date_string}"}), 404

if not valid:
return jsonify({"error": f"Input Start Date {start} not valid. Date Range is {min_date_string} to {max_date_string}"}), 404

if not valid_end:
return jsonify({"error": f"Input End Date {end} not valid. Date Range is {min_date_string} to {max_date_string}"}), 404


if __name__ == '__main__':
    app.run(debug=True)