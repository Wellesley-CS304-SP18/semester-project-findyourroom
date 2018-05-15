'''
	Filename : app.py
	Serena Fan, Renee Huang, Mana Muchaku 
	findYourRoom
'''

#do we need datetime??
import dbconn2
import os,sys,random,bcrypt
import functions
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify, session, Markup, send_from_directory
from werkzeug import secure_filename
from flask_cas import CAS

app = Flask(__name__)
app.secret_key = "123456789"  #should we have something here?

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
				message = Markup(functions.dangerMarkup('The passwords you entered do not match.'))
				flash(message)
				return redirect( url_for('signup'))
				
			hashed = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
			row = functions.emailexists(conn, email)
			if row is not None: 
				message = Markup(functions.dangerMarkup('That user is already taken. Please choose a different one.'))
				flash(message)
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
			message = Markup(functions.errorMarkup('form submission error '+str(err)))
 			flash(message)
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
					message = Markup(functions.dangerMarkup('Incorrect login. Try again or sign up'))
					flash(message)
					return redirect( url_for('login'))
				else:
					hashed = row['hashed']
					
				#Checks if the password matches
				if ((bcrypt.hashpw(password.encode('utf-8'),hashed.encode('utf-8')))[:50]) == hashed:
					session['email'] = email
					session['logged_in'] = True
					bidRow = functions.getBID(conn, email)	
					session['BID'] = bidRow
					msg = functions.successMarkup("Logged in as " + email)
					message = Markup(msg)
					flash(message)
					return redirect( url_for('insert', email=email) ) 
				else: 
					#no match between username and password 
					message = Markup(functions.dangerMarkup('Your password is incorrect. Please try again.'))
					flash(message)
					return redirect( url_for('login'))
			else: 
				#the email does not exist
				message = Markup(functions.dangerMarkup('The email you entered does not exist. Please try again.'))
				flash(message)
				return redirect( url_for('login'))
		except Exception as err:
			message = Markup(functions.errorMarkup('form submission error ' + str(err)))
			flash(message)
			return redirect( url_for('login') )       

#Route for logging out a user
@app.route('/logout/')
def logout():
	if "logged_in" in session and session["logged_in"] is True:
		#clear sessions
		session['logged_in'] = False
		session.clear()
		return render_template('logout.html')
	else:
		message = Markup(functions.dangerMarkup('Please log in!'))
        flash(message)
        return redirect( url_for('login'))
	
#Route for viewing user's existing reviews
@app.route('/account/', methods=["GET","POST"])
def account():
# check if user logged in:                                                                                                                  
    if "logged_in" in session and session["logged_in"] is True:
    	conn = functions.getConn()
    	if request.method == "GET":
			return render_template('account.html', roomarray = functions.pullReviews(conn,session['BID']))
    else:
        message = Markup(functions.dangerMarkup('Please log in!'))
        flash(message)
        return redirect( url_for('login'))

#route for deleting review	
@app.route('/delete/', methods=["POST"])
def delete():
	print 'you went into delete'
	try:
		conn = functions.getConn()
		dormID = request.form['dormID']  
		roomNumber = request.form['roomNumber'] 
		functions.deleteReview(conn, session['BID'],dormID,roomNumber)
		
		message = Markup(functions.successMarkup(dormID + ' ' + roomNumber + ' was succesfully deleted'))
		flash(message)
		
		return redirect( url_for('account'))
	except Exception as err:
		print 'Error: ',err
		message = Markup(functions.errorMarkup('error {}'.format(err)))
		flash(message)
		return redirect( url_for('account'))
	
#route for updating review
@app.route('/update/', methods=["GET","POST"])
def update():
	try:
		conn = functions.getConn()
		if request.method == "GET":
			dormID = request.args.get('dormID')
			roomNumber = request.args.get('roomNumber')
			session['dormID']=dormID
			session['roomNumber']=roomNumber
			return render_template('update.html', review = functions.loadReview(conn, session['BID'], dormID, roomNumber), photo = functions.loadPhoto(conn,session['BID'], dormID, roomNumber))
		
		else:
			#retrieve new rating, comment, and photo description
 			room_rating = request.form['stars']
 			comment = request.form['comment']
 			alt = request.form['alt']
 			photo = functions.loadPhoto(conn,session['BID'], session['dormID'], session['roomNumber'])
 			
 			#retrieve new photo
			newpicture = request.files['pic']
			sfname = 'images/'+str(secure_filename(newpicture.filename))

			#old photo
			oldpicture = photo.get('path')
			
			#update the review in the database
			functions.updateReview(conn, session['dormID'], session['roomNumber'], comment, room_rating, session['BID'])
			
			if newpicture is not None: 
  				#update path and alt of photo
  				newpicture.save('static/images/'+str(secure_filename(newpicture.filename)))
  				functions.updatePhoto(conn,session['BID'],session['dormID'],session['roomNumber'],alt,sfname)
  			else:
 				#update alt of photo
 				functions.updatePhoto(conn,session['BID'],session['dormID'],session['roomNumber'],alt,oldpicture) 
			return redirect( url_for('account'))
	except Exception as err:
		print 'Error: ',err
		message = Markup(functions.errorMarkup('error {}'.format(err)))
		flash(message)
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
					message = Markup(functions.dangerMarkup('Please choose a dorm, room type, and room number.'))
					flash(message)
					return render_template('insert.html', data=data)
				elif dormID == "none" and roomType == 'none':
					message = Markup(functions.dangerMarkup('Please choose a dorm and room type.'))
					flash(message)
					return render_template('insert.html', data=data)
				elif dormID == "none" and not roomNumber:
					message = Markup(functions.dangerMarkup('Please choose a dorm and room number.'))
					flash(message)
					return render_template('insert.html', data=data)
				elif not roomNumber and roomType == 'none':
					message = Markup(functions.dangerMarkup('Please choose a room number and room type.'))
					flash(message)
					return render_template('insert.html', data=data)
				elif dormID == 'none':
					message = Markup(functions.dangerMarkup('Please choose a dorm.'))
					flash(message)
					return render_template('insert.html', data=data)
				elif not roomNumber:
					message = Markup(functions.dangerMarkup('Please choose a room number.'))
					flash(message)
					return render_template('insert.html', data=data)
				else: 
					msg = dormID + " " + roomNumber
					row = functions.roomExists(conn, dormID, roomNumber, roomType)
					if row is not None:
						message = Markup(functions.dangerMarkup(msg + ' already exists'))
						flash(message)
						return render_template('insert.html', data=data)
					else:
						functions.addRoom(conn, dormID, roomNumber, roomType)
						message = Markup(functions.successMarkup(msg + ' succesfully  added.'))
						flash(message)
						return render_template('insert.html', data=data)
			except Exception as err:
				message = Markup(functions.errorMarkup('Sorry, an error occurred.'))
				flash(message)
				data = dataFromDSN(functions)
				return render_template('insert.html', data=data)
	else: 
		message = Markup(functions.dangerMarkup('Please log in!'))
		flash(message)
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
				message = Markup(functions.dangerMarkup("No Result Matches Your Request!"))
				flash(message)
				return render_template('search.html', dormarray = dormarray)
			else:
				return render_template('result.html', roomArray = roomList)
	
		#if user search room through other filters
		elif request.form['submit'] == "filter":   
			location = request.form['location']
			dormType = request.form['dormType']
			roomType = request.form['roomType']
			gym = request.form['gym']
			diningHall = request.form['diningHall']
			rating = request.form['rating']

	 		if rating == "All":
	 			roomList = functions.getListOfRoomsbyFilterNoRating(conn, location, dormType, roomType, gym, diningHall)
	 		else: 
				roomList = functions.getListOfRoomsbyFilter(conn, location, dormType, roomType, gym, diningHall, rating)
			
			if not roomList:
				message = Markup(functions.dangerMarkup("No Result Matches Your Request!"))
				flash(message)
				return render_template('search.html', dormarray = dormarray)
			else:
				return render_template('result.html', roomArray = roomList)

	else: 
		message = Markup(functions.dangerMarkup('Please log in!'))
                flash(message)
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
				message = Markup(functions.dangerMarkup("You have already reviewed this room! Please go to your account to edit!"))
				flash (message)
				return redirect( url_for('search'))
			else: 
				return render_template('review.html')

		else:
			try: 
				room_rating = request.form['stars']	
			except Exception as err:
				message = Markup(functions.errorMarkup('Please rate the room'))
				flash(message)
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
			message = Markup(functions.successMarkup("Review succesfully written for " + dormID +" " +roomNumber))
			flash (message)
			return redirect( url_for('search'))
		
	else:
		message = Markup(functions.dangerMarkup('Please log in!'))
                flash(message)
		return redirect( url_for('login'))

@app.route('/static/<sfname>')
def pic(sfname):
	 print sfname
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
        			gym = functions.getGym(conn, dormID, roomNumber)
        			diningHall = functions.getdiningHal(conn, dormID, roomNumber)
        			return render_template('roominfo.html', roomlist = rowInfo, photolist = rowPhoto, dormID = dormID, roomNumber = roomNumber, roomType = roomType, avgRating = avgRating, gym = gym, diningHall = diningHall )	 	
        		else:
        			messsage = Markup(functions.dangerMarkup("Currently no photo entry for this room"))
        			flash(message)
        			gym = functions.getGym(conn, dormID, roomNumber)
        			diningHall = functions.getdiningHal(conn, dormID, roomNumber)
        			return render_template('roominfo.html', roomlist = rowInfo, dormID = dormID, roomNumber = roomNumber, roomType = roomType, avgRating = avgRating, gym = gym, diningHall = diningHall)
        	else:
        		message = Markup(functions.dangerMarkup("Currently no review for this room"))
        		flash (message)
          		roomType = functions.getroomType(conn, dormID, roomNumber)[0]['roomType']
          		gym = functions.getGym(conn, dormID, roomNumber)
        		diningHall = functions.getdiningHal(conn, dormID, roomNumber)
        		
        		return render_template('roominfo.html', roomlist = rowInfo, dormID = dormID, roomNumber = roomNumber, roomType = roomType, gym = gym, diningHall = diningHall )	 		

	else: 
 		message = Markup(functions.dangerMarkup('Please log in!'))
                flash(message)
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


