import sqlite3 as sql

#connect to SQLite
con = sql.connect("db_web.db")

#Create a connection
cur = con.cursor()

#Drop users table if already exist
cur.execute("DROP TABLE IF EXISTS badges")

#Create users table in db_web database
sql = '''CREATE TABLE "badges" (
        "BID" INTEGER PRIMARY KEY AUTOINCREMENT,
        "BADGE_NAME" TEXT,
        "BADGE_DESCRIPTION" TEXT,
        "UPLOAD_BADGE" TEXT,
        "ELIGIBLE_STUDENTS" TEXT
)'''

cur.execute(sql)

#commit changes
con.commit()

#close connection
con.close()
