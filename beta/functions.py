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

def getConn(db='mmuchaku_db'):
    dsn = dbconn2.read_cnf()
    dsn['db'] = db
    return dbconn2.connect(dsn)

# Functions for login page 
# ================================================================

def emailcorrect(conn, email):
	'''check if email exists in the table'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("select * from user where email=%s", [email]) 
	rows = curs.fetchall()
	return len(rows)==1
    

def getBID(conn, email):
	'''get bid from user's email and password, we have already checked that email & password exists/is correct'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("select BID from user where email=%s", [email])
	row = curs.fetchone()
	return row['BID']

# Functions for signup page 
# ================================================================

def emailexists(conn, email): 
	'''check if the email chosen by user already exists, returns dict/row'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT email FROM user WHERE email = %s', [email])
	row = curs.fetchone()
	return row


def insertinfo(conn, email, password, bid, classyear): 
	'''insert user information into the table, returns nothing'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('INSERT into user(email, pwd, BID, classYear) VALUES(%s,%s,%s,%s)', [email, password, bid, classyear])

# Functions for account  page 
# ================================================================

def pullReviews(conn, BID):
	'''get reviews that the user has written '''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT dormID, roomNumber FROM review where BID=%s', [BID])
	return curs.fetchall()

def deleteReview(conn, BID, dormID, roomNumber):
	'''delete specific review'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('DELETE FROM review WHERE dormID=%s AND roomNumber=%s AND BID=%s', [dormID, roomNumber, BID])

def loadReview(conn, BID, dormID, roomNumber):
	'''get information on an existing review'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("""SELECT dormID, roomNumber, rating, comment 
					FROM review WHERE dormID=%s AND roomNumber=%s 
					AND BID=%s""", [dormID, roomNumber, BID])
	return curs.fetchone()
	
def loadPhoto(conn, BID, dormID, roomNumber):
	'''get photo from existing review '''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("""SELECT path, alt FROM photo WHERE dormID=%s 
					AND roomNumber=%s AND BID=%s""", [dormID, roomNumber, BID])
	return curs.fetchone()

def updatePhoto(conn, BID, dormID, roomNumber, alt, path):
	'''update path and alt of photo'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("""UPDATE  photo SET path=%s, alt=%s WHERE 
					dormID=%s AND roomNumber=%s AND BID=%s""", [path, alt, dormID, roomNumber, BID])

def inserthashed(conn, BID, hashed):
	'''insert user hash password information into the table'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('INSERT into userpass(BID ,hashed) VALUES(%s,%s)',[BID, hashed])

def gethashed(conn, email):
	'''get hash password'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT hashed FROM userpass inner join (user) on user.BID = userpass.BID WHERE email = %s',[email])
	return curs.fetchone() 
		
# Functions for insert room page 
# ================================================================

def roomExists(conn, dormID, roomNumber, roomType):
    '''check if the room exists'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * FROM room WHERE dormID=%s AND roomNumber=%s',[dormID, roomNumber])
    return curs.fetchone()

def addRoom(conn, dormID,roomNumber, roomType):
    '''insert room into db'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('INSERT INTO room (dormID, roomNumber, roomType) VALUES (%s, %s, %s)', [dormID, roomNumber, roomType])
   
# Functions for inserting user review information 
# ================================================================

def updateRating(conn, rating, dormID, roomNumber):
    '''recalculate a room's average rating'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("""UPDATE room SET avgRating = (SELECT AVG(rating) 
    				FROM review WHERE review.dormID=%s AND 
    				review.roomNumber=%s) WHERE room.dormID=%s AND 
    				room.roomNumber =%s""",[dormID, roomNumber, dormID, roomNumber])
 
# check if the review table associated with the room exists already 
def reviewExists(conn, dormID, roomNum, BID):
    '''check if the review for that room exists'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * FROM review WHERE dormID=%s AND roomNumber=%s AND BID = %s',[dormID,roomNum, BID])
    return curs.fetchone()
 
# insert review 
def insertReview(conn, dormID, roomNumber, comment, rating, BID):
     '''add Review'''
     curs = conn.cursor(MySQLdb.cursors.DictCursor)
     curs.execute("""INSERT INTO review (dormID, roomNumber, BID, 
     				rating, comment) VALUES (%s, %s, %s, %s, %s)""", [dormID, roomNumber, comment, rating, BID]);

# update review, add photos functionality
def updateReview(conn, dormID, roomNumber, comment, rating, BID):
    '''update review'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("""UPDATE review SET dormID=%s, roomNumber=%s, 
    				BID=%s, comment=%s, rating=%s WHERE dormID=%s 
    				AND roomNumber=%s AND BID=%s""", [dormID, roomNumber, BID, comment, rating, dormID, roomNumber, BID])

# add photos 
def addPhotos(conn, dormID, roomNumber, BID, path, alt):
	'''update images associated with the room'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("""INSERT INTO photo (dormID, roomNumber, BID, path, alt)
					 VALUES (%s, %s, %s, %s, %s)""",[dormID, roomNumber, BID, path, alt])  
   
# Functions for displaying roominfo
# ================================================================

def getroomInfo(conn, dormID, roomNumber):
    '''get informaiton of the room'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("""SELECT roomType, avgRating, comment FROM review 
    				INNER JOIN room on review.dormID = room.dormID 
    				AND review.roomNumber = room.roomNumber WHERE 
    				review.dormID=%s AND review.roomNumber=%s"""
    				, [dormID, roomNumber])
    return curs.fetchall()

def getroomPhoto(conn, dormID, roomNumber):
    '''get photo of the room'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("""SELECT path, alt FROM photo INNER JOIN room on 
    				photo.dormID = room.dormID AND photo.roomNumber 
    				= room.roomNumber WHERE photo.dormID=%s AND 
    				photo.roomNumber=%s""", [dormID, roomNumber])
    return curs.fetchall()
    
def getroomType(conn, dormID, roomNumber):
    '''get roomType of the room'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("""SELECT roomType FROM room WHERE room.dormID=%s 
    				AND room.roomNumber=%s""", [dormID, roomNumber])
    return curs.fetchall()

def getdiningHal(conn, dormID, roomNumber):
    '''get diningHall info of the room'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("""SELECT dorm.diningHall FROM room INNER JOIN dorm 
    				on dorm.dormID = room.dormID WHERE room.dormID=%s 
    				AND room.roomNumber=%s""", [dormID, roomNumber])
    rows = curs.fetchall()
    if (rows[0]['diningHall'] == 0):
    	return "No"
    else:
    	return "Yes"
    	
def getGym(conn, dormID, roomNumber):
    '''get Gym info of the room'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("""SELECT dorm.gym FROM room INNER JOIN dorm on 
    				dorm.dormID = room.dormID WHERE room.dormID=%s 
    				AND room.roomNumber=%s""", [dormID, roomNumber])
    rows = curs.fetchall()
    if (rows[0]['gym'] == 0):
    	return "No"
    else:
    	return "Yes"
    
# Functions for search room page 
# ================================================================

def getListOfRoomsbyDorm(conn, dormID):
    '''get all the list of rooms based on dormID'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("""SELECT room.dormID, dormName, roomNumber, dorm.gym, 
    				dorm.diningHall from room INNER JOIN dorm ON 
    				room.dormID = dorm.dormID WHERE room.dormID=%s""",[dormID])
    return curs.fetchall()
    
def getListOfRoomsbyFilter(conn, location, dormType, roomType, gym, diningHall ,rating): 
    '''get all the list of rooms based on user preference'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor) 
    curs.execute("""SELECT room.dormID, dormName, roomNumber, dorm.gym, 
    				dorm.diningHall from room INNER JOIN dorm ON room.dormID 
    				= dorm.dormID WHERE location= %s AND dorm.dormType=%s AND 
    				room.roomType =%s AND dorm.gym=%s AND dorm.diningHall=%s 
    				AND room.avgRating>=%s """, [location, dormType, roomType, gym, diningHall, rating])
    return curs.fetchall()

def getListOfDorms(conn):
    '''get list of all dorms'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("select dormName, dormID from dorm where dormName != 'NULL'")
    return curs.fetchall()

# Functions for flashing indicators / alerts
# ================================================================

def errorMarkup(s):
    d = "<div class='alert alert-dismissible alert-primary'>"
    d += "<strong>Error.</strong> "
    d += s
    d += "</div>"
    return d

def dangerMarkup(s):
    d = "<div class='alert alert-dismissible alert-danger'>"
    d += "<strong>Oh Snap!</strong> "
    d += s
    d += "</div>"
    return d

def successMarkup(s):
    print "successMarkup called"
    d = "<div class='alert alert-dismissible alert-success'>"
    d += "<strong>Success!</strong> "
    d += s
    d += "</div>"
    return d

# ================================================================
# This starts the ball rolling, *if* the script is run as a script,
# rather than just being imported.    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: {name} nm".format(name=sys.argv[0])
    else:
        dsn = get_dsn()
        conn = dbconn2.connect(dsn)

