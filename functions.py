'''
	Filename : functions.py
	Description : functions for findYourRoom 
	By : Serena Fan, Mana Muchaku
'''

import sys
import MySQLdb
import dbconn2

def get_dsn(db='yourroom_db'):
    dsn = dbconn2.read_cnf()
    dsn['db'] = db
    return dsn

def getConn(dsn):
    return dbconn2.connect(dsn)


#check if username exists in the table
def emailcorrect(conn, email):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("select * from user where email=%s", [email]) 
    rows = curs.fetchall()
    return len(rows)==1
    
#check if password is correct, return true if passwords match, false if not
def passwordcorrect(conn, email, password1): 
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("select pwd from user where email=%s",[email])
    passwordDict = curs.fetchone() #passwordDict returns dictionary
    password2 = passwordDict['pwd'] #extract password from passwordDict
    return password1 == password2 #compare if user input password matches existing password for that email
	
#check if the username chosen by user already exists, return dict/row
def usernameexists(conn, email): #this works
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT email FROM user WHERE email = %s', [email])
    row = curs.fetchone()
    return row

#insert user information into the table, returns nothing
def insertinfo(conn, email, password, bid, classyear): 
	print ("insert info is happening")
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('INSERT into user(email, pwd, BID, classYear) VALUES(%s,%s,%s,%s)',
							 [email, password, bid, classyear])





#check if the room exists
def roomExists(conn, dormID, roomNumber):
    '''Execute SQL statement to check if the room exists'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * FROM room WHERE dormID=%s AND roomNumber=%s',[dormID, roomNumber])
    return curs.fetchone()

#insert room
def addRoom(dormID,roomNumber):#avg rating? ):
    '''Execute SQL statement to insert room into db'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('INSERT INTO room (dormID, roomNumber) VALUES (dormID=%s, roomNumber=%s)', [dormID, roomNumber])
 
    
#make sure to compute avgRating before putting in argument 
def updateAvgRating(conn, dormID, RoomNum, avgRating):
    '''Execute SQL statement to update avgRating'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('INSERT INTO movie VALUES avgRating=%s WHERE dormID=%s AND roomNumber = %s',[avgRating,RID,RoomNum])
 
#check if the table associated with the room exists already 
def reviewExists(conn, dormID, roomNum, review, pros, cons):
    '''Execute SQL statement to check if the review for that room exists'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * FROM review WHERE dormID=%s AND roomNumber=%s',[dormID,roomNum])
    return curs.fetchone()


def updateReview(conn, dormID, roomNum, review):
    '''Execute SQL statement to add Review'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('INSERT INTO review VAlUES review=%s,pros=%s,cons=%s WHERE dormID=%s AND roomNumber = %s',[review, pros, cons, RID, RoomNum])

#this have to be updated 
def addPhotos(conn, dormID, roomNumber, size, path):
    '''Execute SQL statement to update images associated with the room'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('INSERT INTO pic VALUES size = %s, path = %s, WHERE dormID=%s AND roomNumber = %s',[size, path, dormID, roomNumber]) 

#currently only filtering based on res hall name and average rating. 
#add rating filter later
def getListOfRoomsbyDorm(conn, dormID):
    '''Execute SQL statement to get all the list of rooms based on dormID'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT dormName, roomNumber from room INNER JOIN dorm ON room.dormID = dorm.dormID WHERE room.dormID=%s',[dormID])
    return curs.fetchall()

#currently filtering only through location, dormType and roomType
# special, gym, dinninghall and rating will be added later 
def getListOfRoomsbyFilter(conn, location, dormType, roomType):
    '''Execute SQL statement to get all the list of rooms based on user preference'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor) 
    curs.execute('SELECT dormName, roomNumber from room INNER JOIN dorm ON room.dormID = dorm.dormID WHERE location= %s AND dorm.dormType=%s AND room.roomType =%s', [location, dormType, roomType])
    return curs.fetchall()
   
def getListOfDorms(conn):
    '''Execute SQL statement to get list of all dorms'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("select dormName from dorm where dormName != 'NULL'")
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

