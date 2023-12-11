import mysql.connector
import inspect
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Establish a connection to the MySQL database
conn = mysql.connector.connect(
    host='localhost',  # Only the server address should be specified here
    user='root',
    password='Hagith963!',
    database='python'
)

# Create a cursor to execute SQL queries
cursor = conn.cursor()
query = "SELECT * FROM python.products"
engine = create_engine("mysql://root:Hagith963!@localhost:3306/products")
# Execute the query
cursor.execute(query)
result = cursor.fetchall()
print('Executing')