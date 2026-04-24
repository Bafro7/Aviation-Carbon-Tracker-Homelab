import requests
from requests.auth import HTTPBasicAuth
import mysql.connector
import math
from geopy.geocoders import Nominatim

# PLACEHOLDERS - Replace with your actual credentials locally
OS_USER, OS_PASS = "YOUR_OPENSKY_USERNAME", "YOUR_OPENSKY_PASSWORD"
DB_CONFIG = {
    "host": "localhost",
    "user": "TrackerApp",
    "password": "YOUR_DB_PASSWORD",
    "database": "JetTrackerDB",
    "use_pure": True
}

geolocator = Nominatim(user_agent="SkyWatchTracker")

def get_loc(lat, lon):
    try:
        res = geolocator.reverse((lat, lon), language='en', timeout=5)
        return res.raw.get('address', {}).get('city') or "Unknown" if res else "Unknown"
    except: return "Geocode Error"

def get_dist(lat1, lon1, lat2, lon2):
    if None in [lat1, lon1, lat2, lon2]: return 0.0
    R = 3958.8
    dLat, dLon = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dLon/2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1-a)))

try:
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT HexCode, AircraftStatus, CurrentLat, CurrentLon FROM AircraftStats")
    db_state = {row['HexCode'].lower(): row for row in cursor.fetchall()}

    api_url = "https://opensky-network.org/api/states/all?" + "&".join([f"icao24={h}" for h in db_state.keys()])
    data = requests.get(api_url, auth=HTTPBasicAuth(OS_USER, OS_PASS), timeout=20).json()

    if data.get('states'):
        for s in data['states']:
            hex_code = s[0].lower()
            n_lat, n_lon, n_stat = s[6], s[5], ("Grounded" if s[8] else "Active/Flying")
            old = db_state.get(hex_code)
            
            dist = 0.0
            if old and old['AircraftStatus'] == "Active/Flying" and n_stat == "Active/Flying":
                dist = get_dist(float(old['CurrentLat']), float(old['CurrentLon']), n_lat, n_lon)

            cursor.execute("UPDATE AircraftStats SET CurrentLat=%s, CurrentLon=%s, AircraftStatus=%s, TotalMiles=TotalMiles+%s WHERE HexCode=%s", 
                           (n_lat, n_lon, n_stat, dist, hex_code))
    db.commit()
finally: db.close()
