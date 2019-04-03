# Import numpy and datetime
import numpy as np
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy import create_engine, func

# Import Flask and Jsonify
from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

# Create app/ Flask Setup
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


# Define Flask Routes
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (f"List of available routes:<br/>"
    		f"/api/v1.0/precipitation<br/>"
    		f"/api/v1.0/stations<br/>"
    		f"/api/v1.0/tobs<br/>"
    		f"/api/v1.0/start<br/>"
    		f"/api/v1.0/start/end"
    )

# Calculate the date 1 year ago from the last data point in the database
last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
print(last_date)

# to get the last 12 months of data, last date - 365
last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
print(last_year)

# Perform a query to retrieve the data and precipitation scores
precip_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= last_year).all()


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Perform a query to retrieve the date and precipitation scores
    scores = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_year).\
        order_by(Measurement.date.asc()).all()
    
    # Create a dictionary from the row data and append to a list of prcp_data
    precip_data = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        precip_data.append(precip_dict)
    
    return jsonify(precip_data)    

    