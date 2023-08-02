from flask import Flask,request, render_template, flash, redirect, url_for,session, logging, send_file
from flask_mysqldb import MySQL 
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateTimeField, BooleanField, IntegerField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from functools import wraps
from werkzeug.utils import secure_filename
from coolname import generate_slug
from datetime import timedelta, datetime
from flask import render_template_string
import functools
import math, random 
import json
import csv
import smtplib
from wtforms_components import TimeField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError
import mysql.connector
import MySQLdb
import re
import mongo_db
from passlib.hash import bcrypt
from flask import jsonify
from pymysql.cursors import DictCursor
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASS")  #####################################
app.config['MYSQL_DB'] = 'dbms'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# mysql = MySQL(cursorclass=DictCursor)
# mysql.init_app(app)

app.secret_key= 'ca2'

mysql = MySQL(app)




@app.before_request
def make_session_permanent():
	session.permanent = True
	app.permanent_session_lifetime = timedelta(minutes=10)

def is_logged(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, Please login','danger')
			return redirect(url_for('login'))
	return wrap

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
	if request.method == 'POST':
		cname = request.form['cname']
		cemail = request.form['cemail']
		cquery = request.form['cquery']
		# msgtocc = " ".join(["NAME:", cname, "EMAIL:", cemail, "QUERY:", cquery]) 
		# server1 = smtplib.SMTP('smtp.stackmail.com',587)
		# server1.ehlo()
		# server1.starttls()
		# server1.ehlo()
		# server1.login('youremail.com', 'password')
		# server1.sendmail(sender,cemail,"YOUR QUERY WILL BE PROCESSED!")
		# msgtocc = " ".join(["NME:", cname, "EMAIL:", cemail, "QUERY:", cquery]) 
		# server1.sendmail(sender, careEmail, msgtocc)
		# server1.quit()
		comment_doc = { 'cname' : cname, 'cemail' : cemail, 'cquery' : cquery}
		mongo_db.db.collection.insert_one(comment_doc)
		flash('Your Query has been recorded.', 'success')
		
	return render_template('contact.html')


@app.route('/register', methods=['GET','POST'])
def register():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		username = request.form['username']
		password = request.form['password']
		cpassword = request.form['cpassword']
		aadhar = request.form['aadhar']
		phone = request.form['phone']
		if(not aadhar.isnumeric()):
				flash('Enter valid Aadhar', 'success')
				return render_template('register.html', p_username=username, p_name=name, p_email=email, p_phone=phone)
		if(not phone.isnumeric()):
				flash('Enter valid Phone nunber', 'success')
				return render_template('register.html', p_username=username, p_name=name, p_email=email, p_aadhar=aadhar)
		if(not password == cpassword):
			flash('Retype password correctly', 'success')
			return render_template('register.html', p_username=username, p_name=name, p_email=email, p_aadhar=aadhar, p_phone=phone)
		e_Password = bcrypt.hash(password)
		cur = mysql.connection.cursor()
		
		try:
			cur.execute('INSERT INTO users(username, name, email, password, confirmed, aadhar, phone) values(%s,%s,%s,%s,1,%s,%s)', (username, name, email, e_Password, aadhar, phone))
			mysql.connection.commit()
			cur.close()
			session.clear()
			flash('Thanks for registering!', 'success')
			return redirect(url_for('login'))
		except (MySQLdb.Error, MySQLdb.Warning) as err:
			flash('Username number already exists', 'success')
			cur.close()
			return render_template('register.html')
		
	return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password_candidate = request.form['password']
		cur = mysql.connection.cursor()
		results = cur.execute('SELECT * from users where username = %s' , [username])
		if results > 0:
			data = cur.fetchone()
			password = data['password']
			confirmed = data['confirmed']
			name = data['name']
			if confirmed == 0:
				error = 'Please confirm email before logging in'
				return render_template('login.html', error=error)
			if confirmed == 1 and bcrypt.verify(password_candidate, password) :
				session['logged_in'] = True
				session['username'] = username
				session['name'] = name
				return redirect(url_for('dashboard'))
			else:
				error = 'Invalid password'
				return render_template('login.html', error=error)
			cur.close()
		else:
			error = 'Username not found'
			return render_template('login.html', error=error)
	return render_template('login.html')


@app.route('/changepassword', methods=["GET", "POST"])
def changepassword():
	if request.method == "POST":
		oldPassword = request.form['oldpassword']
		newPassword = request.form['newpassword']
		r_newPassword = request.form['r_newpassword']
		if(newPassword != r_newPassword):
			error = "Retype password correctly"
			return render_template("changepassword.html", error=error)
		cur = mysql.connection.cursor()
		results = cur.execute("SELECT * from users where username = '" + session['username'] + "'")
		if results > 0:
			data = cur.fetchone()
			password = data['password']
			if( bcrypt.verify(oldPassword, password) ):
				newPassword=bcrypt.hash(newPassword) 
				cur.execute("UPDATE users SET password = %s WHERE username = %s", [newPassword,session['username']])
				mysql.connection.commit()
				msg="Changed successfully"
				flash('Changed successfully.', 'success')
				cur.close()
				return render_template("dashboard.html", success=msg)
			else:
				error = "Wrong password"
				return render_template("changepassword.html", error=error)
		else:
			return render_template("changepassword.html")
	return render_template("changepassword.html")

@app.route('/dashboard')
@is_logged
def dashboard():
	return render_template('dashboard.html')

@app.route('/logout')
def logout():
	session.clear()
	flash('Successfully logged out', 'success')
	return redirect(url_for('index'))


###################################################################################################################

@app.route('/profile')
@is_logged
def profile():
	cur = mysql.connection.cursor()
	results = cur.execute("SELECT * from users where username = '" + session['username'] + "'")
	if results > 0:
		data = cur.fetchone()
		name = data['name']
		email = data['email']
		aadhar = data['aadhar']
		phone = data['phone']
		address = data['address']
	return render_template('profile.html', name=name, email=email, aadhar=aadhar, phone=phone, address=address)


@app.route('/update_details',  methods=["GET", "POST"])
@is_logged
def update_profile():
	cur = mysql.connection.cursor()
	results = cur.execute("SELECT * from users where username = '" + session['username'] + "'")
	if results > 0:
		data = cur.fetchone()
		name = data['name']
		email = data['email']
		aadhar = data['aadhar']
		phone = data['phone']
		address = data['address']
	if request.method == "POST":
		newEmail = request.form['n_email']
		newPhone = request.form['n_phone']
		newAddress = request.form['n_address']
		if(not newPhone.isnumeric()):
			flash('Enter valid Phone nunber', 'success')
			return render_template("update_details.html", name=name, email=newEmail, aadhar=aadhar, address=newAddress)
		flag=0
		if((len(newEmail)>0) & (email!=newEmail)):
			cur.execute("UPDATE users SET email = %s WHERE username = %s", [newEmail,session['username']])
			mysql.connection.commit()
			flag=1

		if((len(newPhone)==10) & (phone!=newPhone)):
			cur.execute("UPDATE users SET phone = %s WHERE username = %s", [newPhone,session['username']])
			mysql.connection.commit()
			flag=1

		if((len(newAddress)>0) & (address!=newAddress)):
			cur.execute("UPDATE users SET address = %s WHERE username = %s", [newAddress,session['username']])
			mysql.connection.commit()
			flag=1

		if(flag):
			flash('Changed successfully.', 'success')
		else:
			flash('profile not updated', 'success')

		cur.close()
		
		return render_template("dashboard.html")

	return render_template("update_details.html", name=name, email=email, aadhar=aadhar, phone=phone, address=address)



################################# VEHICLES #################################

@app.route('/display_vehicles')
@is_logged
def display_vehicles():
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM vehicle where username = %s ', (session['username'],) )
	callresults = cur.fetchall()
	cur.close()
	len_row = len(callresults)
	return render_template("display_vehicles.html", callresults = callresults, len_row = len_row)


@app.route('/add_vehicles', methods=['GET','POST'])
@is_logged
def add_vehicles():
	if request.method == 'POST':
		n_lp_number = request.form['lp_number']
		n_engine_number = request.form['engine_number']
		n_reg_date = request.form['reg_date']
		n_exp_date = request.form['exp_date']
		n_brand = request.form['brand']
		n_model = request.form['model']
		d_reg_date = datetime.strptime(n_reg_date, "%Y-%m-%d")
		d_exp_date = datetime.strptime(n_exp_date, "%Y-%m-%d")
		delta = d_exp_date-d_reg_date
		lp_pattern = r'[A-Z][A-Z][0-9][0-9][A-Z][A-Z][0-9][0-9][0-9][0-9]'
		if(not re.match(lp_pattern, n_lp_number)):
			flash('Enter valid License plate number', 'success')
			return render_template('add_vehicles.html', engine_number=n_engine_number, model=n_model, brand=n_brand)
		if(delta.days < 0 ):
			flash('Enter valid expiration date', 'success')
			return render_template('add_vehicles.html',lp_number=n_lp_number, engine_number=n_engine_number, model=n_model, brand=n_brand)
		cur = mysql.connection.cursor()
		try:
			cur.execute("INSERT INTO vehicle VALUES (%s, %s, %s, %s, %s, %s, %s)", (session['username'], n_lp_number, n_engine_number, n_model, n_brand, n_reg_date, n_exp_date))
			mysql.connection.commit()
			cur.close()
			flash('Added successfully.', 'success')
			return redirect(url_for('display_vehicles'))
		except (MySQLdb.Error, MySQLdb.Warning) as err:
			flash('License plate number already exists', 'success')
			cur.close()
			return render_template('add_vehicles.html')

	return render_template('add_vehicles.html')

@app.route('/delete_vehicle/<lp_number>', methods=['GET','POST'])
@is_logged
def delete_vehicle(lp_number):
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM vehicle WHERE lp_number = %s ', (lp_number,) )
	callresults = cur.fetchone()
	
	if request.method == 'POST':
		if request.form['two_button'] == "confirm":
			cur.execute('DELETE FROM vehicle WHERE lp_number = %s ', (lp_number,) )
			mysql.connection.commit()
			cur.close()
			flash(lp_number + ' removed', 'success')
			return redirect(url_for('display_vehicles'))
		else:
			flash(lp_number + ' not removed', 'success')
			cur.close()
			return redirect(url_for('display_vehicles'))
	cur.close()
	return render_template('delete_vehicle.html', res = callresults )


################################# INSURANCE #################################

@app.route('/display_insurance')
@is_logged
def display_insurance():
	cur = mysql.connection.cursor()
	sql_query='SELECT insurance.lp_number, i_number, i_company, i_amount, insurance.reg_date, model, insurance.exp_date FROM insurance, vehicle where insurance.username = %s AND insurance.lp_number = vehicle.lp_number'
	cur.execute(sql_query, (session['username'],) )
	callresults = cur.fetchall()
	cur.close()
	len_row = len(callresults)
	return render_template("display_insurance.html", callresults = callresults, len_row = len_row)

@app.route('/display_insurance/<lp_number>')
@is_logged
def display_insurance_1(lp_number):
	cur = mysql.connection.cursor()
	sql_query='SELECT insurance.lp_number, i_number, i_company, i_amount, insurance.reg_date, model, insurance.exp_date FROM insurance, vehicle where insurance.username = %s AND insurance.lp_number = vehicle.lp_number and insurance.lp_number = %s'
	cur.execute(sql_query, (session['username'],lp_number) )
	callresults = cur.fetchall()
	cur.close()
	len_row = len(callresults)
	return render_template("display_insurance.html", callresults = callresults, len_row = len_row)

@app.route('/add_insurance', methods=['GET','POST'])
@is_logged
def add_insurance():
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM vehicle where username = %s AND lp_number NOT IN ( SELECT lp_number FROM insurance where username = %s)', (session['username'],session['username']) )
	callresults = cur.fetchall()
	cur.close()
	len_row = len(callresults)
	if request.method == 'POST':
		n_lp_number = request.form['lp_number']
		n_i_number = request.form['i_number']
		n_i_company = request.form['i_company']
		n_i_amount = request.form['i_amount']
		n_reg_date = request.form['reg_date']
		n_exp_date = request.form['exp_date']
		cur = mysql.connection.cursor()
		d_reg_date = datetime.strptime(n_reg_date, "%Y-%m-%d")
		d_exp_date = datetime.strptime(n_exp_date, "%Y-%m-%d")
		delta = d_exp_date-d_reg_date
		if(delta.days < 0 ):
			flash('Enter valid expiration date', 'success')
			return render_template('add_insurance.html',callresults = callresults, i_number=n_i_number, i_company=n_i_company, i_amount=n_i_amount)
		
		try:
			cur.execute("INSERT INTO insurance VALUES (%s, %s, %s, %s, %s, %s, %s)", (session['username'], n_lp_number, n_i_number, n_i_company, n_i_amount, n_reg_date, n_exp_date))
			mysql.connection.commit()
			cur.close()
			flash('Added successfully.', 'success')
			return redirect(url_for('display_insurance'))
		except (MySQLdb.Error, MySQLdb.Warning) as err:
			flash('error adding insurance details', 'success')
			cur.close()
			return render_template('add_insurance.html')
		
	return render_template('add_insurance.html', callresults = callresults, len_row = len_row)

@app.route('/delete_insurance/<i_number>', methods=['GET','POST'])
@is_logged
def delete_insurance(i_number):
	cur = mysql.connection.cursor()
	cur.execute('SELECT insurance.lp_number, model, i_company, i_number FROM vehicle, insurance WHERE i_number = %s AND insurance.lp_number = vehicle.lp_number', (i_number,) )
	callresults = cur.fetchone()
	
	if request.method == 'POST':
		if request.form['two_button'] == "confirm":
			cur.execute('DELETE FROM insurance WHERE i_number = %s ', (i_number,) )
			mysql.connection.commit()
			cur.close()
			flash(i_number + ' removed', 'success')
			return redirect(url_for('display_insurance'))
		else:
			flash(i_number + ' not removed', 'success')
			cur.close()
			return redirect(url_for('display_insurance'))
	cur.close()
	return render_template('delete_insurance.html', res = callresults )


################################# VIOLATION #################################

@app.route('/display_violations')
@is_logged
def display_violations():
	cur = mysql.connection.cursor()
	sql_query='SELECT violations.lp_number, challen_number, location, type_of_violation, fine_amount, v_date, v_time, model FROM violations, vehicle where violations.username = %s AND violations.lp_number = vehicle.lp_number'
	cur.execute(sql_query, (session['username'],))
	callresults = cur.fetchall()
	cur.execute('SELECT SUM(fine_amount) FROM violations where username = %s ', (session['username'],) )
	total_fine = cur.fetchone()
	cur.close()
	len_row = len(callresults)
	return render_template("display_violations.html", callresults = callresults, len_row = len_row, total_fine = total_fine)

@app.route('/display_violations/<lp_number>')
@is_logged
def display_violations_1(lp_number):
	cur = mysql.connection.cursor()
	sql_query='SELECT violations.lp_number, challen_number, location, type_of_violation, fine_amount, v_date, v_time, model FROM violations, vehicle where violations.username = %s AND violations.lp_number = vehicle.lp_number and violations.lp_number = %s'
	cur.execute(sql_query, (session['username'],lp_number))
	callresults = cur.fetchall()
	cur.execute('SELECT SUM(fine_amount) FROM violations where username = %s and lp_number = %s', (session['username'],lp_number) )
	total_fine = cur.fetchone()
	cur.close()
	len_row = len(callresults)
	return render_template("display_violations.html", callresults = callresults, len_row = len_row, total_fine = total_fine)


###########################################  ADMIN  ###########################################
		###############################################################################


@app.route('/admin_login', methods=['GET','POST'])
def admin_login():
	if request.method == 'POST':
		password_candidate = request.form['password']

		if "123456" == password_candidate :
			session['logged_in'] = True
			session['username'] = 'Admin'
			session['name'] = 'Admin'
			return redirect(url_for('admin_dashboard'))
		else:
			error = 'Invalid password'
			return render_template('admin_login.html', error=error)
	return render_template('admin_login.html')

@app.route('/admin_dashboard')
@is_logged
def admin_dashboard():
	return render_template('admin_dashboard.html')


@app.route('/admin_contact_queries')
def admin_contact_queries():
	mongores = mongo_db.db.collection.find()
	return render_template('admin_contact_queries.html', mongores= mongores)

@app.route('/admin_display_vehicles')
@is_logged
def admin_display_vehicles():
	cur = mysql.connection.cursor()
	sql_query='SELECT users.username, aadhar, lp_number, engine_number, model, brand, reg_date, exp_date FROM users LEFT OUTER JOIN vehicle ON users.username=vehicle.username ORDER BY users.username'
	cur.execute(sql_query, )
	callresults = cur.fetchall()
	cur.close()
	len_row = len(callresults)
	return render_template("admin_display_vehicles.html", callresults = callresults, len_row = len_row)

@app.route('/admin_display_insurance')
@is_logged
def admin_display_insurance():
	cur = mysql.connection.cursor()
	sql_query='SELECT users.username, aadhar, insurance.lp_number, i_number, i_company, i_amount, insurance.reg_date, model, insurance.exp_date FROM insurance, vehicle, users where  users.username=vehicle.username AND insurance.lp_number = vehicle.lp_number ORDER BY users.username'
	cur.execute(sql_query, )
	callresults = cur.fetchall()
	cur.close()
	len_row = len(callresults)
	return render_template("admin_display_insurance.html", callresults = callresults, len_row = len_row)

@app.route('/admin_display_violations')
@is_logged
def admin_display_violations():
	cur = mysql.connection.cursor()
	sql_query='SELECT users.username, aadhar, violations.lp_number, challen_number, location, type_of_violation, fine_amount, v_date, v_time, model FROM violations, vehicle,users where users.username = vehicle.username AND violations.lp_number = vehicle.lp_number ORDER BY users.username'
	cur.execute(sql_query, )
	callresults = cur.fetchall()
	cur.close()
	len_row = len(callresults)
	return render_template("admin_display_violations.html", callresults = callresults, len_row = len_row)


@app.route('/add_violation', methods=['GET','POST'])
@is_logged
def add_violation():
	if request.method == 'POST':
		n_lp_number = request.form['lp_number']
		n_challen_number = request.form['challen_number']
		n_location = request.form['location']
		n_type = request.form['type']
		n_fine_amt = request.form['fine_amt']
		n_vi_date = request.form['vi_date']
		n_vi_time = request.form['vi_time']
		cur = mysql.connection.cursor()
		results = cur.execute('SELECT * from vehicle where lp_number = %s' , (n_lp_number,))
		if results > 0:
			data = cur.fetchone()
			username = data['username']

			cur.execute("INSERT INTO violations VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (username, n_lp_number, n_challen_number, n_location, n_type, int(n_fine_amt), n_vi_date, n_vi_time))
			mysql.connection.commit()
			cur.close()
			flash('Added successfully.', 'success')
			return redirect(url_for('admin_display_violations'))

		else:
			flash('Vehicle does not exist in database', 'success')
			render_template('add_violation.html')

	return render_template('add_violation.html')


@app.route('/admin_display_users')
@is_logged
def admin_display_users():
	cur = mysql.connection.cursor()
	sql_query='SELECT * FROM users'
	cur.execute(sql_query, )
	callresults = cur.fetchall()
	cur.close()
	len_row = len(callresults)
	return render_template("admin_display_users.html", callresults = callresults, len_row = len_row)

@app.route('/admin_delete_user/<n_username>', methods=['GET','POST'])
@is_logged
def admin_delete_user(n_username):
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM users WHERE username = %s', (n_username,) )
	callresults = cur.fetchone()
	
	if request.method == 'POST':
		if request.form['two_button'] == "confirm":
			cur.execute('DELETE FROM users WHERE username = %s ', (n_username,) )
			mysql.connection.commit()
			cur.close()
			flash(n_username + ' removed', 'success')
			return redirect(url_for('admin_display_users'))
		else:
			flash(n_username + ' not removed', 'success')
			cur.close()
			return redirect(url_for('admin_display_users'))
	cur.close()
	return render_template('admin_delete_user.html', res = callresults )


@app.route('/admin_display_statistics')
@is_logged
def admin_display_statistics():
	cur = mysql.connection.cursor()
	sql_query='SELECT username, name, email FROM users'
	cur.execute(sql_query, )
	callresults = cur.fetchall()
	row_headers = [x[0] for x in cur.description]
	json_data=[]
	for result in callresults:
		json_data.append(dict(zip(row_headers, result)))
	
	users = json.dumps(callresults)
	# print(f"json: {json.dumps(callresults)}")

	

	# INSURANCE
	sql_query='SELECT i_company, count(*) AS i_company_count FROM insurance GROUP BY i_company'
	cur.execute(sql_query, )
	callresults = cur.fetchall()
	row_headers = [x[0] for x in cur.description]
	json_data=[]
	for result in callresults:
		json_data.append(dict(zip(row_headers, result)))
	insurance_company = json.dumps(callresults)

	sql_query='SELECT vehicle.username, count(vehicle.lp_number) AS vehicle_count , count(i_number) AS i_vehicle_count FROM vehicle LEFT OUTER JOIN insurance ON vehicle.lp_number = insurance.lp_number GROUP BY vehicle.username'
	cur.execute(sql_query, )
	callresults = cur.fetchall()
	row_headers = [x[0] for x in cur.description]
	json_data=[]
	for result in callresults:
		json_data.append(dict(zip(row_headers, result)))
	insured_vehicles = json.dumps(callresults)

	# VEHICLE
	sql_query='SELECT SUBSTRING(lp_number, 1, 2) AS v_state, count(*) AS v_state_count FROM vehicle GROUP BY v_state'
	cur.execute(sql_query, )
	callresults = cur.fetchall()
	row_headers = [x[0] for x in cur.description]
	json_data=[]
	for result in callresults:
		json_data.append(dict(zip(row_headers, result)))
	vehicle_state= json.dumps(callresults)

	sql_query='SELECT brand AS v_brand, count(*) AS v_brand_count FROM vehicle GROUP BY v_brand'
	cur.execute(sql_query, )
	callresults = cur.fetchall()
	row_headers = [x[0] for x in cur.description]
	json_data=[]
	for result in callresults:
		json_data.append(dict(zip(row_headers, result)))
	vehicle_brand= json.dumps(callresults)

	# VIOLATION
	sql_query='SELECT type_of_violation, count(*) AS violation_count ,CAST(SUM(fine_amount) AS SIGNED) AS violation_total_amount FROM violations GROUP BY type_of_violation'
	cur.execute(sql_query, )
	callresults = cur.fetchall()
	row_headers = [x[0] for x in cur.description]
	json_data=[]
	for result in callresults:
		json_data.append(dict(zip(row_headers, result)))
	violation_types= json.dumps(callresults)
	
	sql_query='SELECT location, count(*) AS l_violation_count ,CAST(SUM(fine_amount) AS SIGNED) AS l_violation_total_amount FROM violations GROUP BY location'
	cur.execute(sql_query, )
	callresults = cur.fetchall()
	row_headers = [x[0] for x in cur.description]
	json_data=[]
	for result in callresults:
		json_data.append(dict(zip(row_headers, result)))
	violation_location= json.dumps(callresults)

	sql_query='SELECT MONTH(v_date) as month, count(*) AS m_violation_count ,CAST(SUM(fine_amount) AS SIGNED) AS m_violation_total_amount FROM violations GROUP BY month ORDER BY month'
	cur.execute(sql_query, )
	callresults = cur.fetchall()
	row_headers = [x[0] for x in cur.description]
	json_data=[]
	for result in callresults:
		json_data.append(dict(zip(row_headers, result)))
	violation_month= json.dumps(callresults)

	cur.close()
	return render_template("admin_display_statistics.html", users = users, insurance_company = insurance_company, insured_vehicles= insured_vehicles, vehicle_brand = vehicle_brand, vehicle_state = vehicle_state, violation_types = violation_types, violation_location = violation_location, violation_month = violation_month)


@app.route('/alpr_violations/<lp_number>')

def display_violations_2(lp_number):

	cur = mysql.connection.cursor()
	sql_query='SELECT violations.lp_number, challen_number, location, type_of_violation, fine_amount, v_date, v_time, model FROM violations, vehicle where violations.lp_number = vehicle.lp_number and violations.lp_number = %s'
	cur.execute(sql_query, (lp_number,))
	callresults = cur.fetchall()
	cur.execute('SELECT SUM(fine_amount) FROM violations where lp_number = %s', (lp_number,) )
	total_fine = cur.fetchone()
	cur.close()
	len_row = len(callresults)
	return render_template("alpr_violations.html", callresults = callresults, len_row = len_row, total_fine = total_fine)


if __name__ == "__main__":
	app.run(debug=True)
