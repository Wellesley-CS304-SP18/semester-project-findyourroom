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
#in alpha/beta versions implement bcrypt and cookie
@app.route('/signup/', methods=["GET", "POST"])
def signup():
	#GET Request 
	if request.method == "GET":
		return render_template('signup-template.html')
	else:#else POST request
		try:
			#get user registration info
			email = request.form['email']
			password1 = request.form['password1']
			password2 = request.form['password2']
			bid = request.form['bid']
			classyear = request.form['classyear']
			dsn = functions.get_dsn(db='yourroom_db') #!
			conn = functions.getConn(dsn)
			if password1 != password2:
				flash('The passwords you entered do not match.')
				return redirect( url_for('signup'))
			row = functions.usernameexists(conn, email)
			
			if row is not None: 
				flash('That user is already taken. Please choose a different one.')
				return redirect( url_for('signup') )
			else:
				print ("else is happening") # this is printing
				#signup successful, add information to table
				functions.insertinfo(conn, email, password1, bid, classyear) # this isn't happening because of global form error "password"?
				session['email'] = email
				session['logged_in'] = True
				session['visits'] = 1
				#lead user back to home page or to search page
				#return redirect( url_for('insert', email=email) )
				return redirect(url_for('insert',email=email))
		except Exception as err:
			flash('form submission error '+str(err))
			return redirect( url_for('signup') )
        	

#Route for signing in a user
#in alpha/beta versions implement logging out
@app.route('/login/', methods=["GET", "POST"])
def login():
	#GET Request 
	if request.method == "GET":
		return render_template('login-template.html')
	else: 
		try:
			email = request.form["email"]
			password = request.form["password"]
			dsn = functions.get_dsn(db='yourroom_db') #!
			conn = functions.getConn(dsn)
			emailsuccess = functions.emailcorrect(conn, email) 
			if emailsuccess:
				passwordsuccess = functions.passwordcorrect(conn, email, password) 
				print passwordsuccess
				if passwordsuccess:
					flash('Successfully logged in as '+ email)
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
				return redirect( url_for('login-template.html'))
		except Exception as err:
			flash('form submission error ' + str(err))
			return redirect( url_for('login') )       
	
#to be worked on for alpha			
#@app.route('/logout/')
#def logout():
   # remove the username from the session if it is there
#   session.pop('email', None)
#   return redirect(url_for('/'))
			
			#cookie notes for future
			'''
				#set cookie
				flash("Login succeeded")
				resp = make_response(render_template('signin-template.html'))
				resp.set_cookie("email",email)
				return resp'''


# Insert Room Info
@app.route('/insert/', methods=["GET", "POST"])
def insert():
		# GET request
    if request.method == 'GET':
	        dsn = functions.get_dsn()
	        conn = functions.getConn(dsn)
	        data = functions.getListOfDorms(conn)
	        return render_template('insert.html', data=data)
    else: #post method
	    try:
	    	roomNumber = request.form['roomNumber']
	    	print "roomnumber: ", roomNumber
		dormID = request.form['menu-dorm']
		print "dormID: ", dormID
		dsn = functions.get_dsn()
		conn = functions.getConn(dsn)
		data = functions.getListOfDorms(conn)
		if dormID is None and roomNumber is None:
			flash('Please choose a dorm and room number.')
			return render_template('insert.html', data=data)
		elif dormID is None:
			flash('Please choose a dorm.')
			return render_template('insert.html', data=data)
	        elif roomNumber is None:
			flash('Please choose a room number.')
			return render_template('insert.html', data=data)
		else: 
			# room number and dorm provided
			msg = dormID + " " + roomNumber
			row = functions.roomExists(conn, dormID, roomNumber)
			if row is not None:
				flash(msg + ' already exists')
			else:
				functions.addRoom(dormID, roomNumber)
				flash(msg + ' succesfully  added.')
				return render_template('insert.html', data=data)
	    except Exception as err:
		    flash('Sorry, an error occurred.')
		    print err
		    dsn = functions.get_dsn()
		    conn = functions.getConn(dsn)
		    data = functions.getListOfDorms(conn)
		    return render_template('insert.html', data=data)
	    
	    
# Search Room Options
@app.route('/search/', methods=["GET", "POST"])
def search():
	dsn = functions.get_dsn()
	conn = functions.getConn(dsn)
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
	
         

if __name__ == '__main__':
	app.debug = True
	port = os.getuid()
	print('Running on port ' + str(port))
	app.run('0.0.0.0', port)

