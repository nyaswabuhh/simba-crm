import psycopg2

conn =psycopg2.connect(host='localhost',port='5432', database='test3', user='postgres', password='simbapos@2019')

cur = conn.cursor()

print('Database connected')