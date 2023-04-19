import sqlite3 #Using sqlite and pandas
import pandas as pd
from pandas import DataFrame #imported for test display of values
import os 

path = os.path.dirname(__file__)


def populate_tbl():
    conn = sqlite3.connect('Furniture.db') #Establish connection with DB  
    c = conn.cursor()
    read_furniture = pd.read_csv (path + os.path.sep + "Data to import.csv" )
    read_furniture.to_sql('FURNITURE', conn, if_exists='append', index = False) # read csv file into the database

def query_test():
    conn = sqlite3.connect('Furniture.db') #Establish connection with DB  
    c = conn.cursor()
    c.execute(''' SELECT DISTINCT * FROM Furniture WHERE Blocktype=2''') #test query to find entries in table with blocktype 2
    df = DataFrame(c.fetchall(), columns=['Furn_id','Name','Height','Blocktype'])
    print(df) #print query results

populate_tbl()
query_test()
