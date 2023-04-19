import sqlite3


def read_furniture(field,search):
    conn = sqlite3.connect('furniture.db')
    c = conn.cursor()
    c.execute('''SELECT DISTINCT * FROM FURNITURE WHERE Furn_id=?''', (search,))
    data = c.fetchone()
    print(data[field])


read_furniture(1,13)
    
