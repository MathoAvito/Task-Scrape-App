import os

user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_ROOT_PASSWORD')
host = os.environ.get('MYSQL_HOST')
database = os.environ.get('MYSQL_DATABASE')
port = os.environ.get('MYSQL_PORT')

DATABASE_CONNECTION_URI = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'