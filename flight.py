from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
# from flask_mysqldb import MySQL
import MySQLdb
import re
import sys
import json

app = Flask(__name__)
app.secret_key = ''
# mysql = MySQL(app)

#Trying to connect
db_connection = MySQLdb.connect(host="",
						   user = "",
						   passwd = "",
						   db = "",
						   port = )
# If connection is not successful




@app.route('/', methods=['GET', 'POST'])
def login():
	msg = ''
	# Making Cursor Object For Query Execution
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		# Create variables for easy access
		username = request.form['username']
		password = request.form['password']

		# Create session data, we can access this data in other routes
		session['loggedin'] = True
		session['username'] = account['username']
		session['userType'] = account['userType']
		# Redirect to home page
		return redirect(url_for('home'))
	else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
	    return render_template('index.html', msg=msg)

@app.route('/logout', methods=['GET'])
def logout():
	session.pop('loggedin', None)
        session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():

    msg = ''
    airlineID = request.form['airlineID']
    tail_num = request.form['tail_num']
    seat_capacity = request.form['seat_capacity']
    speed = requst.form['speed']
    locationID = request.form['locationID']
    plane_type = request.form['plane_type']
    skids = request.form['skids']
    propellers = request.form['propellers']
    jet_engines = request.form['jet_engines']

    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('add_airplane', [airlineID, tail_num, seat_capacity, speed, locationID, plane_type, skids, propellers, jet_engines])
    db_connection.commit()

    cursor.execute('SELECT * FROM airplane')
    result = cursor.fetchall()
    return render_template(add_airplane.html, result=result, msg=msg)

@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():

    msg = ''
    airportID = request.form['airportID']
    airport_name = request.form['airport_name']
    city = request.form['city']
    state = requst.form['state']
    locationID = request.form['locationID']

    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('add_airport', [airportID, airport_name, city, state, locationID])
    db_connection.commit()

    cursor.execute('SELECT * FROM airport')
    result = cursor.fetchall()
    return render_template(add_airport.html, result=result, msg=msg)

@app.route('/add_person', methods=['GET', 'POST'])
def add_person():

    msg = ''
    personID = request.form['personID']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    locationID = request.form['locationID']
    taxID = request.form['taxID']
    experience = request.form['experience']
    flying_airline = request.form['flying_airline']
    flying_tail = request.form['flying_tail']
    miles = request.form['miles']

    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('add_person', [personID, first_name, last_name, locationID, taxID, experience, flying_airline, flying_tail, miles])
    db_connection.commit()

    cursor.execute('SELECT * FROM person')
    result = cursor.fetchall()
    return render_template(add_person.html, result=result, msg=msg)

@app.route('/grant_pilot_license', methods=['GET', 'POST'])
def grant_pilot_license():

    msg = ''
    personID = request.form['personID']
    license = request.form['license']

    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('grant_pilot_license', [personID, license])
    db_connection.commit()

    cursor.execute('SELECT * FROM pilot')
    result = cursor.fetchall()
    return render_template(grant_pilot_license.html, result=result, msg=msg)


@app.route('/offer_flight', methods=['GET', 'POST'])
def offer_flight():

    msg = ''
    flightID = request.form['flightID']
    routeID = request.form['routeID']
    support_airline = request.form['support_airline']
    support_tail = request.form['support_tail']
    progress = request.form['progress']
    airplane_status = request.form['airplane_status']
    next_time = request.form['next_time']

    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('offer_flight', [flightID, routeID, support_airline, support_tail, progress, airplane_status, next_time])
    db_connection.commit()

    cursor.execute('SELECT * FROM flight')
    result = cursor.fetchall()
    return render_template(offer_flight.html, result=result, msg=msg)


@app.route('/purchase_ticket_and_seat', methods=['GET', 'POST'])
def purchase_ticket_and_seat():

    msg = ''
    ticketID = request.form['ticketID']
    cost = request.form['cost']
    carrier = request.form['carrier']
    customer = request.form['customer']
    deplane_at = request.form['deplane_at']
    seat_number = request.form['seat_number']

    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('purchase_ticket_and_seat', [ticketID, cost, carrier, customer, deplane_at, seat_number])
    db_connection.commit()

    cursor.execute('SELECT * FROM ticket')
    cursor.execute('SELECT * FROM ticket_seat')
    result = cursor.fetchall()
    return render_template(purchase_ticket_and_seat.html, result=result, msg=msg)


@app.route('/add_update_leg', methods=['GET', 'POST'])
def add_update_leg():

    msg = ''
    legID = request.form['legID']
    distance = request.form['distance']
    departure = request.form['departure']
    arrival = request.form['arrival']

    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('add_update_leg', [personID, license])
    db_connection.commit()

    cursor.execute('SELECT * FROM leg')
    result = cursor.fetchall()
    return render_template(add_update_leg.html, result=result, msg=msg)


@app.route('/start_route', methods=['GET', 'POST'])
def start_route():

    msg = ''
    routeID = request.form['routeID']
    legID = request.form['legID']

    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('start_route', [routeID, legID])
    db_connection.commit()

    cursor.execute('SELECT * FROM route')
    cursor.execute('SELECT * FROM route_path')
    result = cursor.fetchall()
    return render_template(start_route.html, result=result, msg=msg)


@app.route('/extend_route', methods=['GET', 'POST'])
def extend_route():

    msg = ''
    routeID = request.form['routeID']
    legID = request.form['legID']

    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('extend_route', [routeID, legID])
    db_connection.commit()

    cursor.execute('SELECT * FROM route')
    cursor.execute('SELECT * FROM route_path')
    result = cursor.fetchall()
    return render_template(extend_route.html, result=result, msg=msg)

@app.route('/flight_landing', methods=['GET', 'POST'])
def flight_landing():

    msg = ''
    flightID = request.form['flightID']

    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('flight_landing', [flightID])
    db_connection.commit()

    cursor.execute('SELECT * FROM flight')
    cursor.execute('SELECT * FROM pilot')
    cursor.execute('SELECT * FROM passenger')
    result = cursor.fetchall()
    return render_template(flight_landing.html, result=result, msg=msg)


@app.route('/flight_takeoff', methods=['GET', 'POST'])
def flight_takeoff():

    msg = ''
    flightID = request.form['flightID']

    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('flight_takeoff', [flightID])
    db_connection.commit()

    cursor.execute('SELECT * FROM flight')
    result = cursor.fetchall()
    return render_template(flight_takeoff.html, result=result, msg=msg)



@app.route('/passengers_board', methods=['GET', 'POST'])
def passengers_board():

    msg = ''
    flightID = request.form['flightID']

    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('passengers_board', [flightID])
    db_connection.commit()

    cursor.execute('SELECT * FROM person')
    result = cursor.fetchall()
    return render_template(passengers_board.html, result=result, msg=msg)



@app.route('/passengers_disembark', methods=['GET', 'POST'])
def passengers_disembark():

    msg = ''
    flightID = request.form['flightID']

    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('passengers_disembark', [flightID])
    db_connection.commit()

    cursor.execute('SELECT * FROM person')
    result = cursor.fetchall()
    return render_template(passengers_disembark.html, result=result, msg=msg)

@app.route('/assign_pilot', methods=['GET', 'POST'])
def assign_pilot():

    msg = ''
    flightID = request.form['flightID']
    personID = request.form['personID']

    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('assign_pilot', [flightID, personID])
    db_connection.commit()

    cursor.execute('SELECT * FROM pilot')
    cursor.execute('SELECT * FROM person')
    result = cursor.fetchall()
    return render_template(assign_pilot.html, result=result, msg=msg)

@app.route('/assign_pilot', methods=['GET', 'POST'])
def assign_pilot():

    msg = ''
    flightID = request.form['flightID']
    personID = request.form['personID']

    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('assign_pilot', [flightID, personID])
    db_connection.commit()

    cursor.execute('SELECT * FROM pilot')
    cursor.execute('SELECT * FROM person')
    result = cursor.fetchall()
    return render_template(assign_pilot.html, result=result, msg=msg)


@app.route('/recycle_crew', methods=['GET', 'POST'])
def recycle_crew():

    msg = ''
    flightID = request.form['flightID']

    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('recycle_crew', [flightID])
    db_connection.commit()

    cursor.execute('SELECT * FROM pilot')
    cursor.execute('SELECT * FROM person')
    result = cursor.fetchall()
    return render_template(recycle_crew.html, result=result, msg=msg)




@app.route('/retire_flight', methods=['GET', 'POST'])
def retire_flight():

    msg = ''
    flightID = request.form['flightID']

    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('retire_flight', [flightID])
    db_connection.commit()

    cursor.execute('SELECT * FROM flight')
    result = cursor.fetchall()
    return render_template(retire_flight.html, result=result, msg=msg)





@app.route('/remove_passenger_role', methods=['GET', 'POST'])
def remove_passenger_role():

    msg = ''
    personID = request.form['personID']

    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('remove_passenger_role', [personID])
    db_connection.commit()

    cursor.execute('SELECT * FROM passenger')
    cursor.execute('SELECT * FROM person')
    result = cursor.fetchall()
    return render_template(remove_passenger_role.html, result=result, msg=msg)





@app.route('/remove_pilot_role', methods=['GET', 'POST'])
def remove_pilot_role():

    msg = ''
    personID = request.form['personID']

    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.callproc('remove_pilot_role', [personID])
    db_connection.commit()

    cursor.execute('SELECT * FROM pilot')
    cursor.execute('SELECT * FROM person')
    result = cursor.fetchall()
    return render_template(remove_pilot_role.html, result=result, msg=msg)














































