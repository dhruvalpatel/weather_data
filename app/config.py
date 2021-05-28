"""
Sets necessary config environment variables in OS.env
"""
import os

user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
database = os.environ['POSTGRES_DB']
port = os.environ['POSTGRES_PORT']
table_name = 'Weather_Data'

DATABASE_CONNECTION_URI = 'postgresql://' + user + ':' + password + '@' + host + ':' + port + '/' + database
