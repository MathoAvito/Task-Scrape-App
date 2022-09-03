import os

# user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_ROOT_PASSWORD')
host = os.environ.get('MYSQL_HOST')
database = os.environ.get('MYSQL_DATABASE')
port = 3306

DATABASE_CONNECTION_URI = f'mysql+pymysql://root:{password}@{host}:{port}/{database}'
