'''
	Filename : app.py
	Serena Fan, Renee Huang, Mana Muchaku 
	findYourRoom
'''

import dbconn2
import os,sys,random, datetime
import functions, bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify, session, Markup, send_from_directory
from werkzeug import secure_filename
app = Flask(__name__)
app.secret_key = "secret_key"

#show basic navigation 
@app.route('/')
def index():
	return render_template('index.html')

#Route for signing up a user
@app.route('/signup/', methods=["GET", "POST"])
def signup():
	if request.method == "GET":
		return render_template('signup.html')
	else:	
		try:
			#get user registration info
			conn = functions.getConn()
			email = request.form['email']
			password1 = request.form['password1']
			password2 = request.form['password2']
			bid = request.form['bid']
			classyear = request.form['classyear']
			
			if password1 != password2:
				flash('The passwords you entered do not match.')
				return redirect( url_for('signup'))
				
			hashed = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
			row = functions.emailexists(conn, email)
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
@app.route('/login/', methods=["GET", "POST"])
def login():
	if request.method == "GET":
		return render_template('login.html')
	else: 
		try:
			conn = functions.getConn()
			email = request.form["email"]
			password = request.form["password"]
			emailsuccess = functions.emailcorrect(conn, email) 
			
			if emailsuccess:
				bid = functions.getBID(conn, email) 
				row = functions.gethashed(conn, bid)

				if row is None:
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

#Route for logging out a user
@app.route('/logout/')
def logout():
	#clear sessions
	session['logged_in'] = False
	session.clear()
	return render_template('logout.html')
	
#Route for viewing user's existing reviews
@app.route('/account/', methods=["GET","POST"])
def account(): 
	conn = functions.getConn()
	
	if request.method == "GET":
		return render_template('account.html', roomarray = functions.pullReviews(conn,session['BID']))
		
	elif request.method == "POST":
		if request.form['submit']=='delete':
			return redirect( url_for('delete'))
		elif request.form['submit'] == 'update':
			return redirect( url_for('update'))
# 			print request.form
# 			dormID = request.form['dormID']  #
# 			roomNumber = request.form['roomNumber'] #
# 			print dormID
# 			print roomNumber
# 			functions.deleteReview(conn, session['BID'],dormID,roomNumber)
# 			flash(dormID + ' ' + roomNumber + 'was successfully deleted')
# 			return render_template('account.html', roomarray = functions.pullReviews(conn,session['BID']))
# 		if request.form['submit'] == 'update':
# 			dormID = request.form['dormID']  
# 			roomNumber = request.form['roomNumber'] 
# 			session['dormID']=dormID
# 			session['roomNumber']=roomNumber
# 			return redirect( url_for('update'))

#route for deleting review	
@app.route('/delete/', methods=["POST"])
def delete():
	try:
		conn = functions.getConn()
		dormID = request.form['dormID']  
		roomNumber = request.form['roomNumber'] 
		functions.deleteReview(conn, session['BID'],dormID,roomNumber)
		flash(dormID + ' ' + roomNumber + 'was successfully deleted')
		return redirect( url_for('account'))
	except Exception as err:
		print 'Error: ',err
		flash('error {}'.format(err))
		return redirect( url_for('account'))
	
#route for updating review
@app.route('/update/', methods=["GET","POST"])
def update():
	conn = functions.getConn()
	dormID = request.form['dormID']  
	roomNumber = request.form['roomNumber'] 
	
	if request.method == "GET":
		return render_template('update.html', review = functions.loadReview(conn, session['BID'], dormID, roomNumber))
		
	elif request.method == "POST":
		room_rating = request.form['stars']
		comment = request.form['comment']
		functions.updateReview(conn, dormID, roomNumber, comment, room_rating, session['BID'])
		flash('Your Review has been updated')
		return redirect( url_for('account'))


# Insert Room Info
@app.route('/insert/', methods=["GET", "POST"])
def insert():
	# check if user logged in:
	if "logged_in" in session and session["logged_in"] is True:	
		conn = functions.getConn()
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
				data = dataFromDSN(functions)
				return render_template('insert.html', data=data)
	else: 
		flash("Please log in!")
		return redirect( url_for('login'))
	    
    
# Route for search room options
@app.route('/search/', methods=["GET", "POST"])
def search():
	if "logged_in" in session and session["logged_in"] is True:
		conn = functions.getConn()
		dormarray = functions.getListOfDorms(conn)
		
		if request.method == 'GET':
			return render_template('search.html', dormarray = dormarray)
	
		elif request.form['submit'] == 'dorm': #if user search room through dorm name 
			roomList =[]
			for room in request.form.getlist("dorm"):
				if room is not None:
					roomList += functions.getListOfRoomsbyDorm(conn,room)
	
			if not roomList:
				flash("No Result Matches Your Request!")
				return render_template('search.html', dormarray = dormarray)
			else:
				return render_template('result.html', roomArray = roomList)
	
		#if user search room through other filters
		elif request.form['submit'] == "filter":   
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


# Review  Room Info                                                                                                            
@app.route('/review/<dormID>/<roomNumber>', methods=["GET", "POST"])
def review(dormID, roomNumber):
	# check if user logged in:                                       
	if "logged_in" in session and session["logged_in"] is True:
		conn = functions.getConn()
		data = dataFromDSN(functions)
		dormarray = functions.getListOfDorms(conn)
		BID = session['BID']
		
		if request.method == "GET":
			# check if review exists in database by bid
			row = functions.reviewExists(conn, dormID, roomNumber, BID)
			
			if row is not None:
				flash ("You have already reviwed this room! Please go to your account to edit!")
				return redirect( url_for('search'))
			else: 
				return render_template('review.html')

		else:
			try: 
				room_rating = request.form['stars']	
			except Exception as err:
				flash('Please rate the room')
				return render_template('review.html')
			
			if len(request.form['comment']) == 0 :
				flash('Please write a comment')
				return render_template('review.html')
			else: 
				comment = request.form['comment'] 
				
			if 'pic' in request.files:
				file = request.files['pic']
				sfname = 'images/'+str(secure_filename(file.filename))
				if sfname !=  'images/':
					file.save('static/images/'+str(secure_filename(file.filename)))
					if len(request.form['alt']) == 0:
						flash('Please fill the image description')
						return render_template('review.html')
					else: 
						alt = request.form['alt']
						functions.addPhotos(conn, dormID, roomNumber, BID, sfname, alt)
			
			functions.insertReview(conn,dormID, roomNumber,BID, room_rating, comment)
			functions.updateRating(conn, room_rating, dormID,roomNumber)
			
			flash ("Review succesfully written for " + dormID +" " +roomNumber)	
			return redirect( url_for('search'))
		
	else:
		flash("Please log in!")
		return redirect( url_for('login'))

#currently without any commment it is loading 
#image alt part error should be flashed and dealt 

@app.route('/static/<sfname>')
def pic(sfname):
	 f = secure_filename(sfname)
	 mime_type = f.split('.')[-1]
	 image = send_from_directory('static',f)
	 return image

# Room Info page 
@app.route('/room/<dormID>/<roomNumber>', methods=["GET"])
def roomInfo(dormID, roomNumber):
	# check if user logged in:                                       
	if "logged_in" in session and session["logged_in"] is True:
		conn = functions.getConn()
		data = dataFromDSN(functions)
        dormarray = functions.getListOfDorms(conn)
        if request.method == "GET":
        	rowInfo = functions.getroomInfo(conn, dormID, roomNumber)
        	rowPhoto = functions.getroomPhoto(conn, dormID, roomNumber)
        
        	if len(rowInfo) >= 1:
        		roomType = rowInfo[0]['roomType']
        		avgRating = rowInfo[0]['avgRating']
        		if len(rowPhoto) >= 1:
        			return render_template('roominfo.html', roomlist = rowInfo, photolist = rowPhoto, dormID = dormID, roomNumber = roomNumber, roomType = roomType, avgRating = avgRating )
        		else:
        			flash ("Currently no photo entry for this room")
        			return render_template('roominfo.html', roomlist = rowInfo, dormID = dormID, roomNumber = roomNumber, roomType = roomType, avgRating = avgRating )
        	else:
        		flash ("Currently no review for this room")
        		roomType = functions.getroomType(conn, dormID, roomNumber)[0]['roomType']
        		return render_template('roominfo.html', roomlist = rowInfo, dormID = dormID, roomNumber = roomNumber, roomType = roomType, avgRating = "N/A" )	 		

	else: 
 		flash("Please log in!")
 		return redirect( url_for('login'))

    
# Function to get data from conn
# ================================================================                          

def dataFromDSN(fcn):
	conn = fcn.getConn()
	return fcn.getListOfDorms(conn)	
    
# ================================================================        
if __name__ == '__main__':
	app.debug = True
	port = os.getuid()
	print('Running on port ' + str(port))
	app.run('0.0.0.0', port)


