# app.py
from flask import Flask, render_template, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Hardcoded MySQL credentials
#mysql_host = "mysql.python.svc.cluster.local:3306"
#mysql_user = "root"
#mysql_password = "your-root-password"
#mysql_database = "mytestpythonapp"

#mysql_host = os.getenv('MYSQL_HOST', 'localhost')
#mysql_port = os.getenv('MYSQL_PORT', '3306')
#mysql_user = os.getenv('MYSQL_USER', 'root')
#mysql_password = os.getenv('MYSQL_PASSWORD', 'your-root-password')
#mysql_database = os.getenv('MYSQL_DATABASE', 'mytestpythonapp')

mysql_host = os.getenv('MYSQL_HOST')
mysql_port = os.getenv('MYSQL_PORT')
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')
mysql_database = os.getenv('MYSQL_DATABASE')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_data():
    name = request.form['name']
    place = request.form['place']

    if not name or not place:
        return jsonify({'error': 'Name and place are required'}), 400

    # Connect to MySQL
    conn = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )

    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_data (name, place) VALUES (%s, %s)", (name, place))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Data saved successfully'}), 200

@app.route('/retrieve', methods=['GET'])
def retrieve_data():
    # Connect to MySQL
    conn = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")
    data = cursor.fetchall()
    conn.close()

    return jsonify({'data': data}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

