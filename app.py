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
Station = Base.classes.station
Measurement = Base.classes.measurement

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
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert the query results to a dictionary using date as the key and prcp as the value."""
    # Query all dates
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list
    prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp.append(prcp_dict)

    return jsonify(prcp)


@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)

    results = session.query(tation.station,Station.name).all()

    session.close()

    stations = []
    for station,name in results:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        stations.append(station_dict)

    return jsonify(stations)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    
    most_active = session.query(Measurement.station).group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]
    
    recent_date_most_active = session.query(Measurement.date).filter(Measurement.station==most_active).\
        order_by(Measurement.date.desc()).first()[0]

    recent_date_most_active = dt.datetime.strptime(recent_date_most_active, "%Y-%m-%d")

    # Calculate the date one year from the last date in data set.
    one_year_ago_most_active = recent_date_most_active - dt.timedelta(days=365)

    # Perform a query to retrieve the data and temperatures
    temps_most_active = (
        session.query(Measurement.date, Measurement.tobs)
        .filter(Measurement.date > one_year_ago)
        .filter(Measurement.station==most_active)
        .order_by(Measurement.date)
        .all()
        )
    session.close()

    temps = []
    for date, tobs in temps_most_active:
        temps_dict = {}
        temps_dict["Date"] = date
        temps_dict["Tobs"] = tobs
        temps.append(temps_dict)

    return jsonify(temps)


@app.route('/api/v1.0/<start>')
def get_start(start):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    temps = []
    for min,avg,max in results:
        temps_dict = {}
        temps_dict["Min"] = min
        temps_dict["Average"] = avg
        temps_dict["Max"] = max
        temps.append(temps_dict)

    return jsonify(temps)

@app.route('/api/v1.0/<start>/<stop>')
def get_start_stop(start,stop):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= stop).all()
    session.close()

    temps = []
    for min,avg,max in results:
        temps_dict = {}
        temps_dict["Min"] = min
        temps_dict["Average"] = avg
        temps_dict["Max"] = max
        temps.append(temps_dict)

    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)
