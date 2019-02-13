from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, request

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return(
        f"Routes:<br/><br/>"
        f"Precipitation<br/>"
        f"Dictionary using date as the key and precipitation as the value.<br/>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"Station<br/>"
        f"Database of Stations and locations.<br/>"
        f"/api/v1.0/stations<br/><br/>"
        f"Temperature <br/>"
        f"Dates and temperature observations from a year before the last data point.<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"Specific Date<br/>"
        f"Return a list of the min temperature, average temperature, and max temperature for an inputed start date in YYYY-MM-DD format.<br/>"
        f"/api/v1.0/[START DATE]<br/><br/>"
        f"Date Range<br/>"
        f"Return a list of the min temperature, average temperature, and max temperature for a given start-end range in YYYY-MM-DD format.<br/>"
        f"/api/v1.0/[START DATE]/[END DATE]"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2010-01-01").\
        all()
    precip = [data]
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    data = session.query(Station.name, Station.station, Station.elevation).all()
    stations_list = []
    for d in data:
        row = {}
        row['name'] = d[0]
        row['station'] = d[1]
        row['elevation'] = d[2]
        stationlist.append(row)
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def temps():
    data = session.query(Station.name, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-08-23").\
        all()
    temps_list= []
    for d in data:
        row = {}
        row["Date"] = d[1]
        row["Station"] = d[0]
        row["Temperature"] = int(d[2])
        temps_list.append(row)
        
    return jsonify(temp_list)

@app.route('/api/v1.0/<start>/')
def start_temp(start):
    data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    start_temps_list = []
    for d in data:
        row = {}
        row['TMIN'] = d[0]
        row['TAVG'] = d[1]
        row['TMAX'] = d[2]
        start_temps_list.append(row)
    return jsonify(temps)

@app.route('/api/v1.0/<start>/<end>')
def range_temp(start, end):
    data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()
    range_temp_list = []
    for d in data:
        row = {}
        row['TMIN'] = d[0]
        row['TAVG'] = d[1]
        row['TMAX'] = d[2]
        range_temp_list.append(row)
    return jsonify(range_temp_list)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(debug=True)