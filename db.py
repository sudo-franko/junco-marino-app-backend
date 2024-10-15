import pymysql

def get_db():
    return pymysql.connect(
        host='localhost', 
        user='root', 
        passwd='', 
        db='JUNCOMARINO',
        cursorclass=pymysql.cursors.DictCursor
    )
