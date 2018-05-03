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
my_sess_dir = '/home/cs304/pub/sessions/'

#show basic navigation 
#redirect here "when you have no place better to go"
@app.route('/')
def index():
	return render_template('index.html')

#Route for signing up a user
#in alpha/beta versions do the following :
# to-do: implement bcrypt/session/cookies
# to-do: check if the email is Wellesley email
# to-do: check if BID is 9 digit if not give an error 
# to-do: check if year is 4 digit if not give an error (maybe check if the year is plausible year) 

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
				session['visits'] = 1
				
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
					session['visits'] = 1 #fixed as 1?
					
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
	
	
# to-do: work on logout feature
# to-do: work on cookies 		
#@app.route('/logout/')
#def logout():
			
# to-do: make sure values inserted are a valid room number
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
			dormList = request.form.getlist("BAT")
			print dormList
	 
	# 		BAT = request.form.getlist("BAT")
	# 		BEB = request.form.getlist("BEB")
	# 		CAZ = request.form.getlist("CAZ")
	# 		CER = request.form.getlist("CER")
	# 		CLA = request.form.getlist("CLA")
	# 		DOW = request.form.getlist("DOW")
	# 		FRE = request.form.getlist("FRE")
	# 		FHC = request.form.getlist("FHC")
	# 		HEM = request.form.getlist("HEM")
	# 		INS = request.form.getlist("INS")
	# 		LAK = request.form.getlist("LAK")
	# 		MAC = request.form.getlist("MAC")
	# 		MUN = request.form.getlist("MUN")
	# 		ORC = request.form.getlist("ORC")
	# 		POM = request.form.getlist("POM")
	# 		SEV = request.form.getlist("SEV")
	# 		SHA = request.form.getlist("SHA")
	# 		SMW = request.form.getlist("SMW")
	# 		STO = request.form.getlist("STO")
	# 		TCE = request.form.getlist("TCE")
	# 		TCW = request.form.getlist("TCW")
	# 
	# 		print BAT
	# 		print BEB
	# for all possible check box , check if they are clicked and then if so run the function and then add to roomList 
	#

		
			dormName = request.form['dorm']
			roomList = functions.getListOfRoomsbyDorm(conn, functions.getdormID(conn,dormName))
		
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


