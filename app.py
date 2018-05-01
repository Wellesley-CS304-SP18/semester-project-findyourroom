'''
	Filename : app.py
	Serena Fan 
	findYourRoom
'''

#notes to renee: has not been tested, bcrypt/salting not done. otherwise signup and signin are completely fleshed out

import dbconn2
import os,sys,random
import functions
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify, bcrypt
app = Flask(__name__)



#Route for signing up a user
@app.route('/signup/', methods=["GET", "POST"])
def signup():
	#GET Request 
	if request.method == "GET":
		return render_template('signup-template.html')
	else:
		try:
			email = request.form['email']
			passwd1 = request.form['password1']
			passwd2 = request.form['password2']
			bid = request.form['bid']
			classyear = request.form['classyear']
			dsn = functions.get_dsn()
            conn = functions.getConn(dsn)
			if passwd1 != passwd2:
				flash('The passwords you entered do not match.')
				return redirect( url_for('signup-template.html'))
			#hashed = passwd1 #what is this
			#print passwd1, type(passwd1) #what is this
			row = functions.usernameexists(conn, email)
			if row is not None:
				flash('That username is already taken. Please choose a different one.')
				return redirect( url_for('signup-template.html') )
			else:
				#signup successful, add information to table
				functions.insertinfo(conn, email, password, bid, classyear)
				session['email'] = email
				session['logged_in'] = True
				session['visits'] = 1
				return redirect( url_for('user', email=email) )
		except Exception as err:
			flash('form submission error '+str(err))
			return redirect( url_for('signup-template.html') )
        	

#Route for signing in a user
@app.route('/signin/', methods=["GET", "POST"])
def signin():
	#GET Request 
	if request.method == "GET":
		return render_template('signin-template.html')
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
					return redirect( url_for('signin-template.html'))
			else: 
				#the email does not exist
				flash('The email you entered does not exist. Please try again.')
				return redirect( url_for('signin-template.html'))
		except Exception as err:
			flash('form submission error ' + str(err))
			return redirect( url_for('signin-template.html') )       
                    
			
			#do we need to set cookie?
			'''
				#set cookie
				flash("Login succeeded")
				resp = make_response(render_template('signin-template.html'))
				resp.set_cookie("email",email)
				return resp'''
			
			