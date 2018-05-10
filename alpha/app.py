'''
	Filename : app.py
	Serena Fan, Renee Huang, Mana Muchaku 
	findYourRoom
'''

import dbconn2
import os,sys,random, datetime
import functions, bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify, session
app = Flask(__name__)
app.secret_key = "secret_key"

#show basic navigation 
@app.route('/')
def index():
	return render_template('index.html')

#Route for signing up a user
#in alpha/beta versions do the following :
# to-do: implement bcrypt/session/cookies

@app.route('/signup/', methods=["GET", "POST"])
def signup():
	if request.method == "GET":
		return render_template('signup.html')
	else:	
		try:
			#get user registration info
			dsn = functions.get_dsn()
			conn = functions.getConn(dsn)
			email = request.form['email']
			password1 = request.form['password1']
			password2 = request.form['password2']
			bid = request.form['bid']
			classyear = request.form['classyear']
			
			if password1 != password2:
				flash('The passwords you entered do not match.')
				return redirect( url_for('signup'))
			row = functions.usernameexists(conn, email)
			
			if row is not None: 
				flash('That user is already taken. Please choose a different one.')
				return redirect( url_for('signup') )
			else:
				#signup successful, add information to table
				functions.insertinfo(conn, email, password1, bid, classyear)
				
				#session will be updated in the later version 
				session['email'] = email
				session['logged_in'] = True
				session['BID'] = BID
				
				#lead user back to home page or to search page
				return redirect(url_for('insert',email=email))
		except Exception as err:
			flash('form submission error '+str(err))
			return redirect( url_for('signup') )
        	

#Route for signing in a user
#in alpha/beta versions implement logging out
@app.route('/login/', methods=["GET", "POST"])
def login():
	if request.method == "GET":
		return render_template('login.html')
	else: 
		try:
			dsn = functions.get_dsn()
			conn = functions.getConn(dsn)
			email = request.form["email"]
			password = request.form["password"]
			emailsuccess = functions.emailcorrect(conn, email) 
			
			if emailsuccess:
				passwordsuccess = functions.passwordcorrect(conn, email, password) 
				if passwordsuccess:
					flash('Successfully logged in as '+ email)
					
					#session will be updated in the later 
					session['email'] = email
					session['logged_in'] = True
					session['BID'] = BID
					
					return redirect( url_for('insert', email=email) ) 
				else: 
					#no match between username and password 
					flash('Your password is incorrect. Please try again.')
					return redirect( url_for('login'))
			else: 
				#the email does not exist
				flash('The email you entered does not exist. Please try again.')
				return redirect( url_for('login'))
		except Exception as err:
			flash('form submission error ' + str(err))
			return redirect( url_for('login') )       
	
	
	
@app.route('/logout/')
def logout():
	session['logged_in'] = False
	return redirect(url_for('login')

# Insert Room Info
@app.route('/insert/', methods=["GET", "POST"])
def insert():
	# check if user logged in:
	if "logged_in" in session and session["logged_in"] is True:	
		dsn = functions.get_dsn()
		conn = functions.getConn(dsn)
		data = functions.getListOfDorms(conn)	
		if request.method == 'GET':
				return render_template('insert.html', data=data)
		else: 
			try:
				roomNumber = request.form['roomNumber']
				roomType = request.form['menu-room-type']  
				dormID = request.form['menu-dorm']
		
				 #updating if/else notifications for correct input
				if dormID == "none" and roomType == 'none' and not roomNumber:
				    flash('Please choose a dorm, room type, and room number.')
				    return render_template('insert.html', data=data)
				elif dormID == "none" and roomType == 'none':
				    flash('Please choose a dorm and room type.')
				    return render_template('insert.html', data=data)
				elif dormID == "none" and not roomNumber:
				    flash('Please choose a dorm and room number.')
				    return render_template('insert.html', data=data)
				elif not roomNumber and roomType == 'none':
				    flash('Please choose a room number and room type.')
				    return render_template('insert.html', data=data)
				elif dormID == 'none':
				    flash('Please choose a dorm.')
				    return render_template('insert.html', data=data)
				elif not roomNumber:
				    flash('Please choose a room number.')
				    return render_template('insert.html', data=data)
				else: 
					# room number and dorm provided
					msg = dormID + " " + roomNumber
					row = functions.roomExists(conn, dormID, roomNumber, roomType)
					if row is not None:
						flash(msg + ' already exists')
						return render_template('insert.html', data=data)
					else:
						functions.addRoom(conn, dormID, roomNumber, roomType)
						flash(msg + ' succesfully  added.')
						return render_template('insert.html', data=data)
			except Exception as err:
				flash('Sorry, an error occurred.')
				print err
				dsn = functions.get_dsn()
				conn = functions.getConn(dsn)
				data = functions.getListOfDorms(conn)
				return render_template('insert.html', data=data)
	else: 
		flash("Please log in!")
		return redirect( url_for('login'))
	    
	    
# Search Room Options
# to-do: add special, gym, dinninghall, rating to the filter 
@app.route('/search/', methods=["GET", "POST"])
def search():
	# check if user logged in:
	if "logged_in" in session and session["logged_in"] is True:
		dsn = functions.get_dsn()
		conn = functions.getConn(dsn)
		
		if request.method == 'GET':
			return render_template('search.html', dormarray = functions.getListOfDorms(conn))
	
		elif request.form['submit'] == 'dorm': #if user search room through dorm name 
			counter = -1
	 		roomList = []
			dormList = request.form.getlist("dorm")
	 		for dorm in dormList:
	 			counter += 1
	 			roomList += functions.getListOfRoomsbyDorm(conn, dormList[counter])
		
			if not roomList:
				flash("No Result Matches Your Request!")
				return render_template('search.html', dormarray = functions.getListOfDorms(conn))
			else:
				return render_template('result.html', roomArray = roomList)
	
		elif request.form['submit'] == "filter": #if user search room through other filters  
			location = request.form['location']
			dormType = request.form['dormType']
			roomType = request.form['roomType']
			# Below to be added later 
				# special = request.form['special']
				# gym = request.form['gym']
				# dinningHall = request.form['dinningHall']
				# rating = request.form['rating']
	 
			roomList = functions.getListOfRoomsbyFilter(conn, location, dormType,roomType)
   
			if not roomList:
				flash("No Result Matches Your Request!")
				return render_template('search.html', dormarray = functions.getListOfDorms(conn))
			else:
				return render_template('result.html', roomArray = roomList)

	else: 
		flash("Please log in!")
		return redirect( url_for('login'))
	

# ================================================================        
if __name__ == '__main__':
	app.debug = True
	port = os.getuid()
	print('Running on port ' + str(port))
	app.run('0.0.0.0', port)


