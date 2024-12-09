from flask import Flask, render_template, Response, session, request, redirect, flash
import os
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import cv2
from ultralytics import YOLO
from new import cam_detection  # Ensure this import is correct

app = Flask(__name__, template_folder='templates')

app.config['SECRET_KEY'] = 'VLPR_PROJECT'
app.config['UPLOAD_FOLDER'] = 'static/files'

# MySQL connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'Sam@6688',  # Replace with your MySQL password
    'database': 'ddds',  # Replace with your database name
}

# Helper function to connect to MySQL
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Function to generate frames for the webcam
def generate_frames_web(path_x):
    yolo_output = cam_detection(path_x)
    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Home page route
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():
    session.clear()
    return render_template('index.html')

# Webcam page route
@app.route("/index2", methods=['GET', 'POST'])
def index2():
    session.clear()
    return render_template('index2.html')

# Webcam video stream route
@app.route('/webcam')
def webcam():
    return Response(generate_frames_web(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')

# About page route
@app.route('/about')
def about():
    session.clear()
    return render_template('about.html')

# Main page route
@app.route('/main')
def main():
    session.clear()
    return render_template('main.html')

# Contact page route
@app.route('/contact')
def contact():
    session.clear()
    return render_template('contact.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if the email already exists in the database
            cursor.execute("SELECT * FROM dddsinfo WHERE email = %s", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                flash('Email already exists!', 'danger')
                return redirect('/signup')

            # Insert new user into the database
            cursor.execute("INSERT INTO dddsinfo (username, email, password) VALUES (%s, %s, %s)",
                           (username, email, hashed_password))
            conn.commit()
            flash('Account created successfully!', 'success')

            cursor.close()
            conn.close()

            return redirect('/login')
        except mysql.connector.Error as err:
            flash(f"Database error: {err}", 'danger')
            return redirect('/signup')

    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Check if the user exists in the database
            cursor.execute("SELECT * FROM dddsinfo WHERE email = %s", (email,))
            user = cursor.fetchone()

            if not user or not check_password_hash(user['password'], password):
                flash('Invalid credentials, please try again.', 'danger')
                return redirect('/login')

            # Store user information in session
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')

            cursor.close()
            conn.close()

            return redirect('/index2')

        except mysql.connector.Error as err:
            flash(f"Database error: {err}", 'danger')
            return redirect('/login')

    return render_template('login.html')


# Captured images route
@app.route('/captured')
def captured_images():
    image_dir = 'static/captured_images'  # Make sure this path is correct and the folder exists
    images = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
    return render_template('captured.html', images=images)

if __name__ == "__main__":
    app.run(debug=True)
