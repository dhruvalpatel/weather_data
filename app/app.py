"""
This module consist of API endpoints
"""
import traceback

import pandas as pd
from flask import Flask, request, jsonify
from meteostat import Daily
from sqlalchemy import create_engine, inspect
from datetime import date, timedelta, datetime

from .config import *


class InvalidUsage(Exception):
    """
    This class is implemented for exception handling demonstration
    """
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def create_app():
    """
    Flask object creation
    :return: flask app object
    """
    flask_app = Flask(__name__)
    return flask_app


app = create_app()


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """
    Registering error handler
    :param error: Error message
    :return: response in JSON format
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


# Query string for berlin/tagle station for average temp across the years
query_string = """SELECT AVG(t.tavg), t.Year_i FROM ( SELECT tavg, 
                            EXTRACT(YEAR from time) as Year_i,
                            EXTRACT(MONTH from time) as Month_i
                            FROM public."Weather_Data" ) as t
                            WHERE t.Month_i=2
                            GROUP BY t.Year_i
                            ORDER BY t.Year_i"""


@app.route("/load_historical_data/<station_id>", methods=["GET"])
def load_historical_data(station_id):
    f"""
    This method loads historical available data into {table_name}
    :param station_id: Give station id which one wants to extract data for
    :return: success when historic data is successfully stored in {table_name}
    """
    data = Daily(str(station_id)).fetch()
    data['station_id'] = station_id
    engine = create_engine(DATABASE_CONNECTION_URI)

    inspect_obj = inspect(engine)
    table_exists_flag = inspect_obj.dialect.has_table(engine.connect(), table_name)
    message_flag = False

    if not table_exists_flag:
        try:
            with engine.connect() as con:
                data.to_sql(table_name, engine, if_exists='append')
                con.execute(f"""ALTER TABLE public."{table_name}" ADD PRIMARY KEY (time, station_id);""")
                message_flag = True
        except:
            print(traceback.print_exc())

    try:
        with engine.connect() as con:
            con.execute(f"""DELETE FROM public."{table_name}" WHERE station_id = '{station_id}' """)
            print(f'Data for {station_id} is deleted from the table {table_name}')
    except:
        print(traceback.print_exc())

    try:
        data.to_sql(table_name, engine, if_exists='append')
        print(f'Data is inserted into {table_name} for station id {station_id}')
    except:
        print(traceback.print_exc())

    if message_flag:
        return 'Historical data endpoint ran for the first time'
    else:
        return f'Historical data endpoint ran for the first time for {station_id}'


@app.route("/load_daily_data/<station_id>", methods=["GET"])
def load_daily_data(station_id):
    f"""
    This method inserts daily report into database for a given station id
    :param station_id: Give station id which one wants to extract data for
    :return: Success when data is inserted into {table_name}
    """
    today = datetime.combine(date.today(), datetime.min.time())
    yesterday = today - timedelta(days=1)

    data = Daily(str(station_id), yesterday, today).fetch()
    data['station_id'] = station_id
    engine = create_engine(DATABASE_CONNECTION_URI)

    for i in range(len(data)):
        try:
            data.iloc[i:i + 1].to_sql(name=table_name, if_exists='append', con=engine)
            print(f'-------------------- Daily data is loaded for {station_id}')
        except:
            print(traceback.print_exc())
            raise InvalidUsage(f'Daily record is already inserted for {station_id}', status_code=208)
            # return f'Daily record is already inserted for {station_id}'
    return 'success'


@app.route("/berlin_tegel_station_data/", methods=["GET"])
def berlin_tegel_station_data():
    """
    SQL query result for berlin/tegel station
    :return: API response which gives SQL result
    """
    engine = create_engine(DATABASE_CONNECTION_URI)
    # dataframe = pd.DataFrame()
    try:
        with engine.connect() as con:
            dataframe = pd.read_sql(query_string, con, columns=['avg', 'year_i'], index_col=['year_i'])
        dataframe.index = dataframe.index.astype('int64')
        return str(dataframe.to_dict())
    except:
        print(traceback.print_exc())
    return 'success'
