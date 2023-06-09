from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
import mysql.connector
import mysql.connector.pooling
import sys
import json
import jinja2

app = Flask(__name__)
# mysql = MySQL(app)

#Trying to connect
config = {
  'user': 'root',
  'password': 'rasna123',
  'host': '127.0.0.1',
  'database': 'flight_management',
  'raise_on_warnings': True
}

pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=7, **config)




@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')
    

@app.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
    msg = ''
    if request.method == 'POST':
        airlineID = request.form['airlineID']
        tail_num = request.form['tail_num']
        seat_capacity = request.form['seat_capacity']
        speed = request.form['speed']
        locationID = request.form['locationID']
        plane_type = request.form['plane_type']
        skids = request.form['skids']
        propellers = request.form['propellers']
        jet_engines = request.form['jet_engines']

        # validate input values
        if not seat_capacity.isdigit() or int(seat_capacity) < 0:
            msg += 'Seat capacity should be a positive integer.<br>'
        if not speed.isdigit() or int(speed) < 0:
            msg += 'Speed should be a positive integer.<br>'
        if not propellers.isdigit() or int(propellers) < 0:
            msg += 'Propellers should be a positive integer.<br>'
        if not jet_engines.isdigit() or int(jet_engines) < 0:
            msg += 'Jet engines should be a positive integer.<br>'

        if msg:
            return render_template('add_airplane.html', msg=msg)

        try:
            db_connection = pool.get_connection()
            cursor = db_connection.cursor()
            cursor.callproc('add_airplane', [airlineID, tail_num, seat_capacity, speed, locationID, plane_type, skids, propellers, jet_engines])
            db_connection.commit()
            cursor.execute('SELECT * FROM airplane')
            result = cursor.fetchall()
            # Close the cursor
            cursor.close()
            db_connection.close()
        except:
            msg += 'Cursor not created error'
            return render_template('add_airplane.html', msg=msg)
        else:
            return render_template('add_airplane1.html', result=result, msg=msg)
    else:
        return render_template('add_airplane.html')


@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():

    msg = ''
    if request.method == 'POST':
        airportID = request.form['airportID']
        airport_name = request.form['airport_name']
        city = request.form['city']
        state = request.form['state']
        locationID = request.form['locationID']

        db_connection = pool.get_connection()
        cursor = db_connection.cursor()
        cursor.callproc('add_airport', [airportID, airport_name, city, state, locationID])
        db_connection.commit()

        cursor.execute('SELECT * FROM airport')
        result = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return render_template('add_airport1.html', result=result, msg=msg)
    else:
        return render_template('add_airport.html')

@app.route('/add_person', methods=['GET', 'POST'])
def add_person():

    msg = ''
    if request.method == 'POST':
        personID = request.form['personID']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        locationID = request.form['locationID']
        taxID = request.form['taxID']
        experience = request.form['experience']
        flying_airline = request.form['flying_airline']
        flying_tail = request.form['flying_tail']
        miles = request.form['miles']

        # validate input values
        if not experience.isdigit() or int(experience) < 0:
            msg += 'Experience should be a positive integer.<br>'
        if not miles.isdigit() or int(miles) < 0:
            msg += 'miles should be a positive integer.<br>'

        if msg:
            return render_template('add_person.html', msg=msg)

        db_connection = pool.get_connection()
        cursor = db_connection.cursor()
        cursor.callproc('add_person', [personID, first_name, last_name, locationID, taxID, experience, flying_airline, flying_tail, miles])
        db_connection.commit()

        cursor.execute('SELECT * FROM person')
        result = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return render_template('add_person1.html', result=result, msg=msg)
    else:
        return render_template('add_person.html')

@app.route('/grant_pilot_license', methods=['GET', 'POST'])
def grant_pilot_license():
    msg = ''
    if request.method == 'POST':
        personID = request.form['personID']
        license = request.form['license']

        db_connection = pool.get_connection()
        cursor = db_connection.cursor()
        cursor.callproc('grant_pilot_license', [personID, license])
        db_connection.commit()

        cursor.execute('SELECT * FROM pilot_licenses')
        result = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return render_template('grant_pilot_license1.html', result=result, msg=msg)
    else:
        return render_template('grant_pilot_license.html')



@app.route('/offer_flight', methods=['GET', 'POST'])
def offer_flight():

    msg = ''
    if request.method == 'POST':
        flightID = request.form['flightID']
        routeID = request.form['routeID']
        support_airline = request.form['support_airline']
        support_tail = request.form['support_tail']
        progress = request.form['progress']
        airplane_status = request.form['airplane_status']
        next_time = request.form['next_time']

        # validate input values
        if not progress.isdigit() or int(progress) < 0:
            msg += 'progress should be a positive integer.<br>'

        if msg:
            return render_template('offer_flight.html', msg=msg)

        db_connection = pool.get_connection()
        cursor = db_connection.cursor()
        cursor.callproc('offer_flight', [flightID, routeID, support_airline, support_tail, progress, airplane_status, next_time])
        db_connection.commit()

        cursor.execute('SELECT * FROM flight')
        result = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return render_template('offer_flight1.html', result=result, msg=msg)
    else:
        return render_template('offer_flight.html')


@app.route('/purchase_ticket_and_seat', methods=['GET', 'POST'])
def purchase_ticket_and_seat():

    msg = ''
    if request.method == 'POST':
        ticketID = request.form['ticketID']
        cost = request.form['cost']
        carrier = request.form['carrier']
        customer = request.form['customer']
        deplane_at = request.form['deplane_at']
        seat_number = request.form['seat_number']

        # validate input values
        if not cost.isdigit() or int(cost) < 0:
            msg += 'cost should be a positive integer.<br>'
        if not seat_number.isdigit() or int(seat_number) < 0:
            msg += 'seat number should be a positive integer.<br>'    

        if msg:
            return render_template('purchase_ticket_and_seat.html', msg=msg)

        db_connection = pool.get_connection()
        cursor = db_connection.cursor()
        cursor.callproc('purchase_ticket_and_seat', [ticketID, cost, carrier, customer, deplane_at, seat_number])
        db_connection.commit()

        cursor.execute('SELECT * FROM ticket')
        result = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return render_template('purchase_ticket_and_seat1.html', result=result, msg=msg)
    else:
        return render_template('purchase_ticket_and_seat.html')


@app.route('/add_update_leg', methods=['GET', 'POST'])
def add_update_leg():

    msg = ''
    if request.method == 'POST':
        legID = request.form['legID']
        distance = request.form['distance']
        departure = request.form['departure']
        arrival = request.form['arrival']

        # validate input values
        if not distance.isdigit() or int(distance) < 0:
            msg += 'distance should be a positive integer.<br>'

        if msg:
            return render_template('add_update_leg.html', msg=msg)

        db_connection = pool.get_connection()
        cursor = db_connection.cursor()
        cursor.callproc('add_update_leg', [personID, license])
        db_connection.commit()

        cursor.execute('SELECT * FROM leg')
        result = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return render_template('add_update_leg1.html', result=result, msg=msg)
    else:
        render_template('add_update_leg.html')


@app.route('/start_route', methods=['GET', 'POST'])
def start_route():

    msg = ''
    if request.method == 'POST':
        routeID = request.form['routeID']
        legID = request.form['legID']

        db_connection = pool.get_connection()
        cursor = db_connection.cursor()
        cursor.callproc('start_route', [routeID, legID])
        db_connection.commit()

        cursor.execute('SELECT * FROM route')
        result = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return render_template('start_route1.html', result=result, msg=msg)
    else:
        return render_template('start_route.html')


@app.route('/extend_route', methods=['GET', 'POST'])
def extend_route():

    msg = ''
    if request.method == 'POST':
        routeID = request.form['routeID']
        legID = request.form['legID']

        db_connection = pool.get_connection()
        cursor = db_connection.cursor()
        cursor.callproc('extend_route', [routeID, legID])
        db_connection.commit()

        cursor.execute('SELECT * FROM route')
        result = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return render_template('extend_route1.html', result=result, msg=msg)
    else:
        return render_template('extend_route.html')

@app.route('/flight_landing', methods=['GET', 'POST'])
def flight_landing():

    msg = ''
    if request.method == 'POST':
        flightID = request.form['flightID']

        db_connection = pool.get_connection()
        cursor = db_connection.cursor()
        cursor.callproc('flight_landing', [flightID])
        db_connection.commit()

        cursor.execute('SELECT * FROM flight')
        result = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return render_template('flight_landing1.html', result=result, msg=msg)
    else:
        return render_template('flight_landing.html')


@app.route('/flight_takeoff', methods=['GET', 'POST'])
def flight_takeoff():

    msg = ''
    if request.method == 'POST':
        flightID = request.form['flightID']

        db_connection = pool.get_connection()
        cursor = db_connection.cursor()
        cursor.callproc('flight_takeoff', [flightID])
        db_connection.commit()

        cursor.execute('SELECT * FROM flight')
        result = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return render_template('flight_takeoff1.html', result=result, msg=msg)
    else:
        return render_template('flight_takeoff.html')



@app.route('/passengers_board', methods=['GET', 'POST'])
def passengers_board():

    msg = ''
    if request.method == 'POST':
        flightID = request.form['flightID']

        db_connection = pool.get_connection()
        cursor = db_connection.cursor()
        cursor.callproc('passengers_board', [flightID])
        db_connection.commit()

        cursor.execute('SELECT * FROM person')
        result = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return render_template('passengers_board1.html', result=result, msg=msg)
    else:
        return render_template('passengers_board.html')



@app.route('/passengers_disembark', methods=['GET', 'POST'])
def passengers_disembark():

    msg = ''
    if request.method == 'POST':
        flightID = request.form['flightID']

        db_connection = pool.get_connection()
        cursor = db_connection.cursor()
        cursor.callproc('passengers_disembark', [flightID])
        db_connection.commit()

        cursor.execute('SELECT * FROM person')
        result = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return render_template('passengers_disembark1.html', result=result, msg=msg)
    else:
        return render_template('passengers_disembark.html')


@app.route('/assign_pilot', methods=['GET', 'POST'])
def assign_pilot():

    msg = ''
    if request.method == 'POST':
        flightID = request.form['flightID']
        personID = request.form['personID']

        db_connection = pool.get_connection()
        cursor = db_connection.cursor()
        cursor.callproc('assign_pilot', [flightID, personID])
        db_connection.commit()

        cursor.execute('SELECT * FROM pilot')
        result = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return render_template('assign_pilot1.html', result=result, msg=msg)
    else:
        return render_template('assign_pilot.html')


@app.route('/recycle_crew', methods=['GET', 'POST'])
def recycle_crew():

    msg = ''
    if request.method == 'POST':
        flightID = request.form['flightID']

        db_connection = pool.get_connection()
        cursor = db_connection.cursor()
        cursor.callproc('recycle_crew', [flightID])
        db_connection.commit()

        cursor.execute('SELECT * FROM pilot')
        result = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return render_template('recycle_crew1.html', result=result, msg=msg)
    else:
        return render_template('recycle_crew.html')




@app.route('/retire_flight', methods=['GET', 'POST'])
def retire_flight():

    msg = ''
    if request.method == 'POST':
        flightID = request.form['flightID']

        db_connection = pool.get_connection()
        cursor = db_connection.cursor()
        cursor.callproc('retire_flight', [flightID])
        db_connection.commit()

        cursor.execute('SELECT * FROM flight')
        result = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return render_template('retire_flight1.html', result=result, msg=msg)
    else:
        return render_template('retire_flight.html')





@app.route('/remove_passenger_role', methods=['GET', 'POST'])
def remove_passenger_role():

    msg = ''
    if request.method == 'POST':
        personID = request.form['personID']

        db_connection = pool.get_connection()
        cursor = db_connection.cursor()
        cursor.callproc('remove_passenger_role', [personID])
        db_connection.commit()

        cursor.execute('SELECT * FROM passenger')
        result = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return render_template('remove_passenger_role1.html', result=result, msg=msg)
    else:
        return render_template('remove_passenger_role.html')





@app.route('/remove_pilot_role', methods=['GET', 'POST'])
def remove_pilot_role():

    msg = ''
    if request.method == 'POST':
        personID = request.form['personID']
        db_connection = pool.get_connection()
        cursor = db_connection.cursor()
        cursor.callproc('remove_pilot_role', [personID])
        db_connection.commit()

        cursor.execute('SELECT * FROM pilot')
        result = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return render_template('remove_pilot_role1.html', result=result, msg=msg)
    else:
        return render_template('remove_pilot_role.html')




@app.route('/flights_in_the_air', methods=['GET'])
def flights_in_the_air():
    db_connection = pool.get_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM flights_in_the_air")
    results = cursor.fetchall()
    cursor.close()
    db_connection.close()
    
    # Render the HTML template with the query results
    return render_template('flights_in_the_air.html', results=results)


@app.route('/flights_on_the_ground', methods=['GET'])
def flights_on_the_ground():
    db_connection = pool.get_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM flights_on_the_ground")
    results = cursor.fetchall()
    cursor.close()
    db_connection.close()

    # Render the HTML template with the query results
    return render_template('flights_on_the_ground.html', results=results)


@app.route('/people_in_the_air', methods=['GET'])
def people_in_the_air():
    db_connection = pool.get_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM people_in_the_air")
    results = cursor.fetchall()
    cursor.close()
    db_connection.close()

    # Render the HTML template with the query results
    return render_template('people_in_the_air.html', results=results)



@app.route('/people_on_the_ground', methods=['GET'])
def people_on_the_ground():
    db_connection = pool.get_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM people_on_the_ground")
    results = cursor.fetchall()
    cursor.close()
    db_connection.close()

    # Render the HTML template with the query results
    return render_template('people_on_the_ground.html', results=results)


@app.route('/route_summary', methods=['GET'])
def route_summary():
    db_connection = pool.get_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM route_summary")
    results = cursor.fetchall()
    cursor.close()
    db_connection.close()

    # Render the HTML template with the query results
    return render_template('route_summary.html', results=results)


@app.route('/alternative_airports', methods=['GET'])
def alternative_airports():
    db_connection = pool.get_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM alternative_airports")
    results = cursor.fetchall()
    cursor.close()
    db_connection.close()

    # Render the HTML template with the query results
    return render_template('alternative_airports.html', results=results)



@app.route('/simulation_cycle', methods=['GET', 'POST'])
def simulation_cycle():
    msg = ''
    if request.method == 'POST':
        try:
            db_connection = pool.get_connection()
            cursor = db_connection.cursor()
            cursor.callproc('simulation_cycle')
            db_connection.commit()
            result = cursor.fetchall()
            cursor.close()
            db_connection.close()
        except:
            msg =+ 'Error in cursor and db_connection'
            return render_template('simulation_cycle.html', msg=msg)
        else:
            return render_template('simulation_cycle1.html', **result)
    else:
        return render_template('simulation_cycle.html')





if __name__ == "__main__":
    app.run(debug=True)
