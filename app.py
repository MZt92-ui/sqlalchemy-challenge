#################################################
# Import dependencies
#################################################
import numpy as np
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from datetime import datetime, date
from flask import Flask, jsonify

#################################################
# Connect to Databases
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask set up
#################################################
app = Flask(__name__)

#################################################
# Flask routes
#################################################
@app.route("/")
def home():
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
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).all()
    session.close()
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict) 
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results_sta = session.query(station.station).all()
    session.close()
    all_stations = list(np.ravel(results_sta))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    ya_date = date(2016,8,24)
    session = Session(engine)
    results_tobs = session.query(measurement.tobs).\
                    filter(measurement.station == "USC00519397").filter(measurement.date > ya_date).all()
    session.close()
    all_tobs = list(np.ravel(results_tobs))
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def tobs_start(start):
    start_date = datetime.strptime(start,"%y-%m-%d")
    session = Session(engine)
    results_start = session.query(func.max(measurement.tobs),func.avg(measurement.tobs),func.min(measurement.tobs)).\
                filter(measurement.date > start_date).all()
    session.close()
    tobs_start = []
    for max, avg, min in results_start:
        range_dic = {}
        range_dic["max"] = max
        range_dic["avg"] = avg
        range_dic["min"] = min
        tobs_start.append(range_dic)
    return jsonify(tobs_start)

@app.route("/api/v1.0/<start>/<end>")
def tobs_range(start, end):
    start_date = datetime.strptime(start,"%y-%m-%d")
    end_date = datetime.strptime(end,"%y-%m-%d")
    session = Session(engine)
    results_range = session.query(func.max(measurement.tobs),func.avg(measurement.tobs),func.min(measurement.tobs)).\
                filter(measurement.date > start_date).\
                filter(measurement.date <= end_date).all()
    session.close()
    tobs_range = []
    for max, avg, min in results_range:
        range_dic2 = {}
        range_dic2["max"] = max
        range_dic2["avg"] = avg
        range_dic2["min"] = min
        tobs_range.append(range_dic2)
    return jsonify(tobs_range)

if __name__ == '__main__':
    app.run(debug=True)
