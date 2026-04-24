from flask import Flask, render_template, jsonify
import mysql.connector

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "TrackerApp",
    "password": "YOUR_DB_PASSWORD",
    "database": "JetTrackerDB",
    "use_pure": True
}

@app.route('/')
def index(): return render_template('index.html')

@app.route('/api/data')
def api_data():
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM AircraftStats ORDER BY TotalMiles DESC")
    data = cursor.fetchall()
    for r in data:
        r['TotalCO2'] = float(r['TotalMiles'] or 0) * float(r['GallonsPerMile'] or 1) * 21.1
    db.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
