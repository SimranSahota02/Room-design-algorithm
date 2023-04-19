import sqlite3 # Using sqlite to create database

def create_db():
    conn = sqlite3.connect('furniture.db')  # Establish database connection and name it 
    c = conn.cursor() # Create a cursor
    c.execute('''CREATE TABLE FURNITURE 
                 ([Furn_id] integer PRIMARY KEY,[Name] text, [Height] integer, [Blocktype] integer)''') 
    #Create table with necessary fields                 
    conn.commit() # end connection and save


create_db()
