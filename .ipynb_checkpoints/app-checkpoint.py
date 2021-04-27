import numpy as np

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
Measurement = Base.classes.measurement
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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start><end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a dictionary of dates and their precipitations"""
    session = Session(engine)
    
    result = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23').order_by(Measurement.date).all()
    
    session.close()
    
    prcp_list = []
    
    for r in result:
        prcp_dict = {}
        prcp_dict['Date'] = r.date
        prcp_dict['Precipitation'] = r.prcp
        prcp_list.append(prcp_dict)


    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def station():
    """Return a list of stations from the dataset"""
    
    session = Session(engine)
    
    result = session.query(Station.station).all()
    
    session.close()


    all_stations = list(np.ravel(result))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of TOBS for the most active station over the previous year"""
    
    session = Session(engine)
    
    result = session.query(Measurement.tobs, Measurement.date).filter(Measurement.station == 'USC00519281', Measurement.date > '2016-08-23').order_by(Measurement.date).all()
    
    session.close()
    
    temp_list = []
    
    for r in result:
        temp_dict = {}
        temp_dict['Date'] = r.date
        temp_dict['TOBS'] = r.tobs
        temp_list.append(temp_dict)
    
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def start(start):
    """Return the minimum, maximum, and average TOBS for all dates greater than or equal to the start date"""
    
    session = Session(engine)
    result = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    
    temp_list = list(np.ravel(result))
    
    start_dict = {
        "Start Date":start,
        "Minimum Temp":temp_list[0]
        "Maximum Temp":temp_list[1]
        "Average Temp":temp_list[2]
    }
    
    return jsonify(start_dict)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Return the minium, maximum, and average TOBS  for all dates between the start and end dates"""
    
    session = Session(engine)
    result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()
    session.close()

    se_list = list(np.ravel(result))
    
    se_dict = {
        "Start Date":start,
        "End Date":end,
        "Minimum Temp":se_list[0]
        "Maximum Temp":se_list[1]
        "Average Temp":se_list[2]
    }
    
    return jsonify(se_dict)
    
if __name__ == '__main__':
    app.run(debug=True)
