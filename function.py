# Mana Muchaku 
# CS304- FindYourRoom
# 2018.04.29
#!/usr/local/bin/python2.7


import sys
import MySQLdb
import dbconn2
import imghdr

# ================================================================
# The functions that do most of the work.  

def roomExists(conn, RID, RoomNum)
	'''Execute SQL statement to check if the room exists'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * FROM roomInfo WHERE RID=%s AND RoomNum=%s',[RID,RoomNum])
    return curs.fetchone()
    
#make sure to compute avgRating before putting in argument 
def updateAvgRating(conn, RID, RoomNum, avgRating)
	'''Execute SQL statement to update avgRating'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('INSERT INTO movie VALUES avgRating=%s WHERE RID=%s AND RoomNum = %s',[avgRating,RID,RoomNum]
 
#check if the table associated with the room exists already 
def reviewExists(conn, RID, RoomNum, review, pros, cons)
	'''Execute SQL statement to check if the review for that room exists'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * FROM review WHERE RID=%s AND RoomNum=%s',[RID,RoomNum])
    return curs.fetchone()

def updateReview(conn, RID, RoomNum, review)
	'''Execute SQL statement to add Review'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('INSERT INTO review VAlUES review=%s,pros=%s,cons=%s WHERE RID=%s AND RoomNum = %s',[review, pros, cons, RID, RoomNum])

#this have to be updated 
def addPhotos(conn, RID, RoomNum, size, path)
	'''Execute SQL statement to update images associated with the room'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('INSERT INTO pic VALUES size = %s, path = %s, WHERE RID=%s AND RoomNum = %s',[size, path, RID, RoomNum]) 

#currently only filtering based on res hall name and average rating. 
def getListofRooms(conn, RID, rating):
    '''Execute SQL statement to get all the list of rooms based on user preference'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('SELECT * from roomInfo WHERE RID=%s AND avgRating = %s',[RID, rating])
    return curs.fetchall)
    
#need to have more argument for user to filter /if so probably need to add more boolean to each dorm such as east/west side, has dinning hall, has gym etc
#alpha version : delete comment 


# ================================================================
# This starts the ball rolling, *if* the script is run as a script,
# rather than just being imported.    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: {name} nm".format(name=sys.argv[0])
    else:
        DSN = dbconn2.read_cnf()
        DSN['db'] = 'mmuchaku_db'     # the database we want to connect to
        dbconn2.connect(DSN)
        print lookupByNM(sys.argv[1])
