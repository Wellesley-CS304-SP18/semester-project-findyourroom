'''
	Filename : app.py
	Serena Fan, Renee Huang, Mana Muchaku 
	findYourRoom
'''

import dbconn2
import os,sys,random, datetime
import functions, bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify, session, Markup
from werkzeug import secure_filename
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
			hashed = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
			row = functions.usernameexists(conn, email)
			
			if row is not None: 
				flash('That user is already taken. Please choose a different one.')
				return redirect( url_for('signup') )
			else:
				#signup successful, add information to table
				functions.insertinfo(conn, email, password1, bid, classyear)
				functions.inserthashed(conn, bid, hashed)
				
				#session will be updated in the later version 
				session['email'] = email
				session['logged_in'] = True
				session['BID'] = bid
				
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
			
			if functions.emailcorrect(conn, email) :
				bid = functions.getBID(conn, email) 
				row = functions.gethashed(conn, bid)

				if row is None:
					# Same response as wrong password, so no information about what went wrong
					flash('login incorrect. Try again or join')
					return redirect( url_for('login'))
				else:
					hashed = row['hashed']
					
				#Checks if the password matches
				if ((bcrypt.hashpw(password.encode('utf-8'),hashed.encode('utf-8')))[:50]) == hashed:
					flash('Successfully logged in as '+ email)
					session['email'] = email
					session['logged_in'] = True
					bidRow = functions.getBID(conn, email)	
					print bidRow 				
					#session['BID'] = bidRow['BID']
					session['BID'] = bidRow
					
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
	session.clear()
	return render_template('logout.html')
	
	
@app.route('/account/', methods=["GET","POST"])
def account():
	dsn = functions.get_dsn()
	conn = functions.getConn(dsn)
	if request.method == "GET":
		print session['BID']
		return render_template('account.html', roomarray = functions.pullReviews(conn,session['BID']))
	elif request.method == "POST":
		if request.form['submit']=='delete':
			
			print 'you clicked on delete'
			#if i finally get that working then will probably get error on not finding dormID or roomNUmber so then test this
			dormID = request.form['dormID'] #will these two request.form lines work? 
			roomNumber = request.form['roomNumber']
			print dormID
			print roomNumber
			functions.deleteReview(conn, session['BID'],dormID,roomNumber)
			flash('Room was deleted successfully')
			return render_template('account.html', roomarray = functions.pullReviews(conn,session['BID']))
	 
#paste deleted stuff for update here

# Insert Room Info
@app.route('/insert/', methods=["GET", "POST"])
def insert():
	# check if user logged in:
	if "logged_in" in session and session["logged_in"] is True:	
		conn = connFromDSN(functions)
		data = dataFromDSN(functions)
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
				data = dataFromDSN(functions)
				return render_template('insert.html', data=data)
	else: 
		flash("Please log in!")
		return redirect( url_for('login'))
	    
#maybe through roomnumber too?	    
# Search Room Options
# to-do: rating to the filter check
@app.route('/search/', methods=["GET", "POST"])
def search():
	if "logged_in" in session and session["logged_in"] is True:
		dsn = functions.get_dsn()
		conn = functions.getConn(dsn)
		dormarray = functions.getListOfDorms(conn)
		
		if request.method == 'GET':
			return render_template('search.html', dormarray = dormarray)
		
		elif request.form['submit'] == 'dorm': #if user search room through dorm name 
			dormList = request.form.getlist("dorm")
			roomList =[]
			for dorm in dormList:
				if dorm is not None:
					roomList += functions.getListOfRoomsbyDorm(conn, dorm)
			
			if not roomList:
				flash("No Result Matches Your Request!")
				return render_template('search.html', dormarray = dormarray)
			else:
				return render_template('result.html', roomArray = roomList)
	
		elif request.form['submit'] == "filter": #if user search room through other filters  
			location = request.form['location']
			dormType = request.form['dormType']
			roomType = request.form['roomType']
			gym = request.form['gym']
			dinningHall = request.form['dinningHall']
			rating = request.form['rating']
	 
			roomList = functions.getListOfRoomsbyFilter(conn, location, dormType, roomType, gym, dinningHall, rating)
			   
			if not roomList:
				flash("No Result Matches Your Request!")
				return render_template('search.html', dormarray = dormarray)
			else:
				return render_template('result.html', roomArray = roomList)

	else: 
		flash("Please log in!")
		return redirect( url_for('login'))

#have to fix somepart like when the user does not put those to 
#I think we should check if that user has alraedy put a review for that room.
# if so then edit that page instead of uploading a new one?
# is it repetitive though (having 2 ways of editing the comment - one throug the account and one throuhg this?)
# Review  Room Info                                                                                                            
@app.route('/review/<dormID>/<roomNumber>', methods=["GET", "POST"])
def review(dormID, roomNumber):
	# check if user logged in:                                       
	if "logged_in" in session and session["logged_in"] is True:
		conn = connFromDSN(functions)
        data = dataFromDSN(functions)
        if request.method == "GET":
        	return render_template('review.html')
        else:
			# get review from form
			room_rating = request.form['stars']
			comment = request.form['comment']
			pro_or_con = request.form['stars2']
			BID = session['BID']
			roomMsg = dormID +" " +roomNumber		
		
			#if user uploaded an image save them into the photo folder
			if request.files['pic'] is not None:
				file = request.files['pic']
				sfname = 'images/'+str(secure_filename(file.filename))
				file.save(sfname)
				functions.addPhotos(conn, dormID, roomNumber, BID,sfname)
			
			# check if review exists in database by bid
			row = functions.reviewExists(conn, dormID, roomNumber, BID)
			
			#if user already has review for this room, then update the review 
			if row is not None:
				functions.updateReview(conn, dormID, roomNumber, BID, room_rating, comment)
				#update the avgrating of the room. haven't tested yet
				functions.updateRating(conn, room_rating, dormID,roomNumber)
				flash ("You have updated your review for " + roomMsg)
         		# next, give them option to update review
        
			# else insert a new review entry into database
			else:
				functions.insertReview(conn,dormID, roomNumber,BID, room_rating, comment)
				flash ("Review succesfully written for " + roomMsg)	

	else: 
 		flash("Please log in!")
 		return redirect( url_for('login'))

# Room Info page                                                                                                           
@app.route('/room/<dormID>/<roomNumber>', methods=["GET"])
def roomInfo(dormID, roomNumber):
	# check if user logged in:                                       
	if "logged_in" in session and session["logged_in"] is True:
		conn = connFromDSN(functions)
        data = dataFromDSN(functions)
        if request.method == "GET":
        	try :
        		rowInfo = functions.getroomInfo(conn, dormID, roomNumber)
        		print rowInfo
        		rowPhoto = functions.getroomPhoto(conn, dormID, roomNumber)
        		print rowPhoto
        		
        		if rowInfo[0] is not None:
        			if rowPhoto[0] is not None:
        				return render_template('roominfo.html', roomlist = rowInfo, photolist = rowPhoto, dormID = dormID, roomNumber = roomNumber)
        			else:
        				flash ("Currently no photo entry for this room")
        				return render_template('roominfo.html', roomlist = rowInfo, dormID = dormID, roomNumber = roomNumber)
        		else:
        			flash ("Currently no review for this room")
        			return render_template('roominfo.html', roomlist = rowInfo, dormID = dormID, roomNumber = roomNumber) 	
        						
        	except Exception as err:
        		flash ("Currently no review for this room")
        		return render_template('roominfo.html', roomlist = rowInfo, dormID = dormID, roomNumber = roomNumber) 	 
        		
	else: 
 		flash("Please log in!")
 		return redirect( url_for('login'))
          		
			
# Function to get data from conn
# ================================================================                          

def dataFromDSN(fcn):
	conn = connFromDSN(fcn)
	return fcn.getListOfDorms(conn)	

def connFromDSN(fcn):
	dsn = fcn.get_dsn()
	return fcn.getConn(dsn)

# ================================================================        
if __name__ == '__main__':
	app.debug = True
	port = os.getuid()
	print('Running on port ' + str(port))
	app.run('0.0.0.0', port)


