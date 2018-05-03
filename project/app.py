'''
	Filename : app.py
	Serena Fan, Renee Huang, Mana Muchaku 
	findYourRoom
'''

#notes to renee: has not been tested, bcrypt/salting not done. otherwise signup and signin are completely fleshed out

import dbconn2
import os,sys,random
import functions, bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify
app = Flask(__name__)
app.secret_key = "secret_key"

#show basic navigation 
#redirect here "when you have no place better to go"
@app.route('/')
def index():
	return render_template('index.html')

#Route for signing up a user
@app.route('/signup/', methods=["GET", "POST"])
def signup():
	#GET Request 
	if request.method == "GET":
		return render_template('signup-template.html')
	else:#else POST request
		try:
			#get user registration info
			email = request.form['email']
			passwd1 = request.form['password1']
			passwd2 = request.form['password2']
			bid = request.form['bid']
			classyear = request.form['classyear']
			dsn = functions.get_dsn()
			conn = functions.getConn(dsn)
			if passwd1 != passwd2:
				flash('The passwords you entered do not match.')
				return redirect( url_for('signup'))
			#hashed = passwd1 #what is this
			#print passwd1, type(passwd1) #what is this
			row = functions.usernameexists(conn, email)
			
			if row is not None:
				flash('That user is already taken. Please choose a different one.')
				return redirect( url_for('signup') )
			else:
				#signup successful, add information to table
				functions.insertinfo(conn, email, password, bid, classyear)
				session['email'] = email
				session['logged_in'] = True
				session['visits'] = 1
				return redirect( url_for('user', email=email) )
		except Exception as err:
			flash('form submission error '+str(err))
			return redirect( url_for('signup') )
        	

#Route for signing in a user
@app.route('/login/', methods=["GET", "POST"])
def login():
	#GET Request 
	if request.method == "GET":
		return render_template('login-template.html')
	else:
		try:
			email = request.form["email"]
			password = request.form["passwd"]
			dsn = functions.get_dsn()
			conn = functions.getConn(dsn)
			emailsuccess = functions.emailcorrect(conn, email) 
			if emailsuccess:
				passwordsuccess = functions.passwordcorrect(conn, email, password) 
				if passwordsuccess:
					flash('Successfully logged in as '+ email)
					session['email'] = email
					session['logged_in'] = True
					session['visits'] = 1 #fixed as 1?
					return redirect( url_for('user', email=email) ) #does this need to change? change user to email?
				else: 
					#no match between username and password 
					flash('Your password is incorrect. Please try again.')
					return redirect( url_for('login'))
			else: 
				#the email does not exist
				flash('The email you entered does not exist. Please try again.')
				return redirect( url_for('login-template.html'))
		except Exception as err:
			flash('form submission error ' + str(err))
			return redirect( url_for('login') )       
                
				
# Insert Room Info
@app.route('/insert/', methods=["GET", "POST"])
def insert():
	if request.method == 'GET':
		try:
			dsn = functions.get_dsn()
			conn = functions.getConn(dsn)
			data = functions.getListOfDorms(conn)
			print data
			return render_template('insert.html', data=data)
		except Exception as err:
			print err
			flash('Insert error')
			return render_template('insert.html')
	else: 
		# post method
		roomnum = request.form['roomNumber']
		dormid = request.form['dormID']
		# check if room already exists
		row = roomExists(conn, dormID, roomNumber)

		# room already exists
		if row is not None: 
			flash('This room already exists in database.')
			return redirect (url_for('insert'))
		else:
			# room doesn't exist yet, 
			flash('Room succesfully added to database.')
			return redirect (url_for('insert'))

# Search Room Options
@app.route('/search/', methods=["GET", "POST"])
def search():
	conn = dbconn2.connect(DSN)
	if request.method == 'GET':
		return render_template('search.html', dormarray = functions.getListOfDorms(conn))
	
	elif request.form['submit'] == 'dorm':
		dormName = request.form['dorm']
		roomList = functions.getListOfRoomsbyDorm(conn, functions.getdormID(conn,dormName))
		
		if not roomList:
			flash("No Result Matches Your Request!")
			return render_template('search.html', dormarray = functions.getListOfDorms(conn))
		else:
			return render_template('result.html', roomArray = roomList)
	
	elif request.form['submit'] == "filter":
		print "request filter submit"
		location = request.form['location']
   		dormType = request.form['dormType']
     	roomType = request.form['roomType']
    	special = request.form['special']
    	gym = request.form['gym']
     	dinningHall = request.form['dinningHall']
     	rating = request.form['rating']
     	
     	print "location = " + location 
     	print "dormtype = " + dormType
     	print "roomType = " + roomType
     	print "special = " + special
     	print "gym = " + gym
     	print "dinningHall = " + dinningHall
     	print "rating = " + rating
  		
     	#if the user select all, then how shoould i reflect that on the sql?
     # 	
#      	if rating == "All":
#      		rating = 0
#      	elif rating == "over1":
#      		rating = 1
#      	elif rating == "over2":
#      		rating = 2
#      	elif rating == "over3":
#      		rating = 3
#      	elif rating == "over4":
#      		rating = 4
#      	elif rating == "over5":
#      		rating = 5
    	
    	roomList = functions.getListOfRoomsbyFilter(conn, location, dormType,roomType)
    	#special, gym, dinningHall, rating)
    	print roomList
    
    	if not roomList:
      		flash("No Result Matches Your Request!")
      		return render_template('search.html', dormarray = functions.getListOfDorms(conn))
    	else:
    		return render_template('result.html', roomArray = roomList)
	
          

if __name__ == '__main__':

    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    DSN = dbconn2.read_cnf()
    DSN['db'] = 'yourroom_db'
    app.debug = True
    app.run('0.0.0.0',port)
    
    
