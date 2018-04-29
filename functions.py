'''
	Filename : functions.py
	Description : functions for findYourRoom 
	By : Serena Fan
'''
#notes to renee: has not been tested, need to replace !!nameoftable!! with name of table that stores user info


#check if username exists in the table
def emailcorrect(conn, email):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("select * from !!nameoftable!! where email=%s", [email]) 
    rows = curs.fetchall()
    return len(rows)=1
    
#check if password matches username
def passwordcorrect(conn, email, password1):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute("select password from !!nameoftable!! where email=%s",[email])
	password2 = curs.fetchall()
	return password1 = password2
	
#check if the username chosen by user already exists
def usernameexists(conn, email):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('SELECT email FROM !!nameoftable!! WHERE email = %s', [email])
	row = curs.fetchone()
	return row

#insert user information into the table
def insertinfo(conn, email, password, bid, classyear): 
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('INSERT into !!nameoftable!!(email, password, bid, classyear) VALUES(%s,%s,%s,%s)',
							 [email, password, bid, classyear])