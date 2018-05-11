'''
	Filename : functions.py
	Serena Fan, Renee Huang, Mana Muchaku 
	findYourRoom
'''

import sys
import MySQLdb
import dbconn2

# Functions to connect to the database 
# ================================================================

def get_dsn(db='rhuang_db'):
    dsn = dbconn2.read_cnf()
    dsn['db'] = db
    return dsn

def getConn(dsn):
    return dbconn2.connect(dsn)

# Functions for login page 
# ================================================================

def emailcorrect(conn, email):
	'''Execute SQL statement to check if username exists in the table'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("select * from user where email=%s", [email]) 
	rows = curs.fetchall()
	return len(rows)==1
    
def getBID(conn, email): 
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("select BID from user where email=%s",[email])
	return curs.fetchone() 
	
# Functions for signup page 
# ================================================================

#return dict/row
def usernameexists(conn, email): 
	'''Execute SQL statement to check if the username chosen by user already exists'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT email FROM user WHERE email = %s', [email])
	row = curs.fetchone()
	return row

#returns nothing 
def insertinfo(conn, email, password, bid, classyear): 
	'''Execute SQL statement to insert user information into the table'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('INSERT into user(email, pwd, BID, classYear) VALUES(%s,%s,%s,%s)', [email, password, bid, classyear])

def inserthashed(conn, BID, hashed):
	'''Execute SQL statement to insert user hash password information into the table'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('INSERT into userpass(BID ,hashed) VALUES(%s,%s)',[BID, hashed])
	
def gethashed(conn, BID):
	'''Execute SQL statement to get hash password'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT hashed FROM userpass WHERE BID = %s',[BID])
	return curs.fetchone() 
	
	
# Functions for insert room page 
# ================================================================

def roomExists(conn, dormID, roomNumber, roomType):
    '''Execute SQL statement to check if the room exists'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * FROM room WHERE dormID=%s AND roomNumber=%s',[dormID, roomNumber])
    return curs.fetchone()

def addRoom(conn, dormID,roomNumber, roomType):#avg rating?
    '''Execute SQL statement to insert room into db'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('INSERT INTO room (dormID, roomNumber, roomType) VALUES (%s, %s, %s)', [dormID, roomNumber, roomType])
   
# Functions for inserting user review information 
# ================================================================

# update avgRating 
# Note : make sure to compute avgRating before putting in argument 
# def updateAvgRating(conn, dormID, RoomNum, avgRating):
#     '''Execute SQL statement to update avgRating'''
#     curs = conn.cursor(MySQLdb.cursors.DictCursor)
#     curs.execute('INSERT INTO movie VALUES avgRating=%s WHERE dormID=%s AND roomNumber = %s',[avgRating,RID,RoomNum])
#  
# check if the review table associated with the room exists already 
# def reviewExists(conn, dormID, roomNum, review, pros, cons):
#     '''Execute SQL statement to check if the review for that room exists'''
#     curs = conn.cursor(MySQLdb.cursors.DictCursor)
#     curs.execute('SELECT * FROM review WHERE dormID=%s AND roomNumber=%s',[dormID,roomNum])
#     return curs.fetchone()
# 
# update review 
# def updateReview(conn, dormID, roomNum, review):
#     '''Execute SQL statement to add Review'''
#     curs = conn.cursor(MySQLdb.cursors.DictCursor)
#     curs.execute('INSERT INTO review VAlUES review=%s,pros=%s,cons=%s WHERE dormID=%s AND roomNumber = %s',[review, pros, cons, RID, RoomNum])
# 
# add photos 
# def addPhotos(conn, dormID, roomNumber, size, path):
#     '''Execute SQL statement to update images associated with the room'''
#     curs = conn.cursor(MySQLdb.cursors.DictCursor)
#     curs.execute('INSERT INTO pic VALUES size = %s, path = %s, WHERE dormID=%s AND roomNumber = %s',[size, path, dormID, roomNumber]) 

# Functions for search room page 
# ================================================================

# To-do : add average rating to the filter
def getListOfRoomsbyDorm(conn, dormID):
    '''Execute SQL statement to get all the list of rooms based on dormID'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT room.dormID, dormName, roomNumber from room INNER JOIN dorm ON room.dormID = dorm.dormID WHERE room.dormID=%s',[dormID])
    return curs.fetchall()

# To-do : add special, gym, dinninghall and rating to the filter 
def getListOfRoomsbyFilter(conn, location, dormType, roomType):
    '''Execute SQL statement to get all the list of rooms based on user preference'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor) 
    curs.execute('SELECT dormName, roomNumber from room INNER JOIN dorm ON room.dormID = dorm.dormID WHERE location= %s AND dorm.dormType=%s AND room.roomType =%s', [location, dormType, roomType])
    return curs.fetchall()

def getListOfDorms(conn):
    '''Execute SQL statement to get list of all dorms'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("select dormName, dormID from dorm where dormName != 'NULL'")
    return curs.fetchall()

def getdormID(conn,dormName):
    '''Execute SQL statement to get dormID of all rooms'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("select dormID from dorm where dormName = %s", [dormName])
    dormDic = curs.fetchone()
    dormid = dormDic['dormID']
    return dormid
    

# ================================================================
# This starts the ball rolling, *if* the script is run as a script,
# rather than just being imported.    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: {name} nm".format(name=sys.argv[0])
    else:
        dsn = get_dsn()
        conn = dbconn2.connect(dsn)

