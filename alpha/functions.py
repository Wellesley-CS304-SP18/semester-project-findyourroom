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

def get_dsn(db='yourroom_db'):
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
    
# get bid from email and password, we have already checked that email & password exists/is correct
def getBID(conn, email):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("select BID from user where email=%s", [email])
    row = curs.fetchone()    
    return row['BID']


# Functions for signup page 
# ================================================================

#return dict/row
def usernameexists(conn, email): 
	'''check if the username chosen by user already exists, returns'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT email FROM user WHERE email = %s', [email])
	row = curs.fetchone()
	return row

#returns nothing 
def insertinfo(conn, email, password, bid, classyear): 
	'''insert user information into the table, '''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('INSERT into user(email, pwd, BID, classYear) VALUES(%s,%s,%s,%s)', [email, password, bid, classyear])

# Functions for account  page 
# ================================================================
def pullReviews(conn, BID):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT dormID, roomNumber FROM review where BID=%s', [BID])
	return curs.fetchall()

def deleteReview(conn, BID, dormID, roomNumber):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('DELETE FROM review WHERE dormID=%s AND roomNumber=%s AND BID=%s', [dormID, roomNumber, BID])

def loadReview(conn, BID, dormID, roomNumber):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT dormID, roomNumber, rating, comment FROM review WHERE dormID=%s AND roomNumber=%s AND BID=%s', [dormID, roomNumber, BID])
	return curs.fetchone()

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

def updateRating(conn, rating, dormID, roomNumber):
    '''Execute SQL statement to recalculate a movie's rating'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('UPDATE room SET avgRating = (SELECT AVG(rating) FROM review WHERE review.dormID=%s AND review.roomNumber=%s) WHERE room.dormID=%s AND room.roomNumber =%s',[dormID, roomNumber, dormID, roomNumber])
 
# check if the review table associated with the room exists already 
def reviewExists(conn, dormID, roomNum, BID):
    '''Execute SQL statement to check if the review for that room exists'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * FROM review WHERE dormID=%s AND roomNumber=%s AND BID = %s',[dormID,roomNum, BID])
    return curs.fetchone()
 
# insert review 
def insertReview(conn, dormID, roomNumber, comment, rating, BID):
     '''Execute SQL statement to add Review'''
     curs = conn.cursor(MySQLdb.cursors.DictCursor)
     # add pros and cons later
     curs.execute('INSERT INTO review (dormID, roomNumber, BID, rating, comment) VALUES (%s, %s, %s, %s, %s)', [dormID, roomNumber, comment, rating, BID]);

# update review, add photos functionality
def updateReview(conn, dormID, roomNumber, comment, rating, BID):
    '''Execute SQL statement to update review'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('UPDATE review SET dormID=%s, roomNumber=%s, BID=%s, comment=%s, rating=%s WHERE dormID=%s AND roomNumber=%s AND BID=%s', [dormID, roomNumber, BID, comment, rating, dormID, roomNumber, BID])

# add photos 
#do i need size here?
def addPhotos(conn, dormID, roomNumber, BID, path):
	'''Execute SQL statement to update images associated with the room'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('INSERT INTO photo (dormID, roomNumber, BID, path) VALUES (%s, %s, %s, %s)',[dormID, roomNumber, BID, path]) 
   
   
# Functions for displaying roominfo
# ================================================================
def getroomInfo(conn, dormID, roomNumber):
    '''Execute SQL statement to get the current average rating of a movie'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT roomType, avgRating, comment, reviewType FROM review INNER JOIN room on review.dormID = room.dormID AND review.roomNumber = room.roomNumber WHERE review.dormID=%s AND review.roomNumber=%s', [dormID, roomNumber])
    return curs.fetchall()

def getroomPhoto(conn, dormID, roomNumber):
    '''Execute SQL statement to get the current average rating of a movie'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT path FROM photo INNER JOIN room on photo.dormID = room.dormID AND photo.roomNumber = room.roomNumber WHERE photo.dormID=%s AND photo.roomNumber=%s', [dormID, roomNumber])
    return curs.fetchall()


# Functions for search room page 
# ================================================================

def getListOfRoomsbyDorm(conn, dormID):
    '''Execute SQL statement to get all the list of rooms based on dormID'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT room.dormID, dormName, roomNumber from room INNER JOIN dorm ON room.dormID = dorm.dormID WHERE room.dormID=%s',[dormID])
    return curs.fetchall()
    
def getListOfRoomsbyFilter(conn, location, dormType, roomType, gym, dinningHall,rating): 
    '''Execute SQL statement to get all the list of rooms based on user preference'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor) 
    curs.execute('SELECT room.dormID, dormName, roomNumber from room INNER JOIN dorm ON room.dormID = dorm.dormID WHERE location= %s AND dorm.dormType=%s AND room.roomType =%s', [location, dormType, roomType])
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

