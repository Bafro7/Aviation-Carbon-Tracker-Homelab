import mysql.connector

# --- DATABASE CONFIG ---
db_config = {
    "host": "localhost",
    "user": "TrackerApp",
    "password": "YOUR_DB_PASSWORD", # Replace this on your VM, but keep as is for GitHub!
    "database": "JetTrackerDB",
    "use_pure": True
}

# The Full Fleet Audit - 2026 Accurate
# Format: "TailNumber": ("Celebrity/Owner", "Model", "Hex", GallonsPerMile)
jet_data = {
    "N628TS": ("Elon Musk", "G650ER", "A835AF", 1.25),
    "N272BG": ("Elon Musk", "G550", "A2AE0A", 1.10),
    "N8628":  ("Elon Musk (G800)", "G800", "ABD9B5", 1.20),
    "N3200X": ("Taylor Swift", "Falcon 7X", "A37452", 0.95),
    "N1980K": ("Kim Kardashian", "G650ER", "A188D7", 1.25),
    "N810KJ": ("Kylie Jenner", "Global 7500", "AB0A46", 1.15),
    "N11AF":  ("Jeff Bezos", "G700", "A029E0", 1.35),
    "N767CJ": ("Drake (Air Drake)", "Boeing 767", "AA5BC4", 3.80),
    "N757AF": ("Donald Trump", "Boeing 757", "AA3410", 4.10),
    "N887WM": ("Bill Gates", "Global Express", "AC3B0E", 1.10),
    "N194WM": ("Walmart (Walton)", "G650", "A1787C", 1.20),
    "N652WE": ("Eric Schmidt (Google)", "G650", "A89970", 1.20),
    "N1DC":   ("Mark Cuban", "G-V", "A0000C", 1.05),
    "N236MJ": ("Michael Jordan", "G550", "A21F53", 1.10),
    "N517TW": ("Tiger Woods", "G550", "A67D55", 1.10),
    "N162JC": ("Jim Carrey", "G-V", "A10091", 1.05),
    "N1969C": ("P. Diddy", "G-V", "A1818B", 1.05),
    "N713TS": ("Travis Scott", "G-V", "A99071", 1.05),
    "N313AR": ("Alex Rodriguez", "G-IV", "A35532", 1.00),
    "N958TB": ("Tom Brady", "G-V", "AD51C2", 1.05),
    "N221DG": ("David Geffen", "G650ER", "A1E00E", 1.25),
    "N540W":  ("Oprah Winfrey", "G650", "A6D75C", 1.20),
    "N650HA": ("Steven Spielberg", "G650", "A8952B", 1.20),
    "N506AB": ("Harrison Ford", "Citation Sovereign", "A65275", 0.65),
    "N707JT": ("John Travolta", "Boeing 707", "A97547", 4.50),
    "N1KE":   ("Nike Corp (Phil Knight)", "G650", "A03D26", 1.20),
    "N88WR":  ("Rick Ross", "G-V", "A84013", 1.05),
    "N758PB": ("Pitbull", "G650ER", "AA347D", 1.25),
    "N817GS": ("Steve Wynn", "G650", "AB2444", 1.20),
    "N898CE": ("Larry Ellison", "G650", "AC69F9", 1.20),
    "N709DS": ("Dan Snyder", "737 BBJ", "A97843", 3.20),
    "N125RK": ("Robert Kraft (Patriots)", "G650", "A069E6", 1.20),
    "N801JJ": ("Jerry Jones (Cowboys)", "G650", "AB0088", 1.20),
    "N611AM": ("Arthur Blank (Falcons)", "G650", "A7F25D", 1.20),
    "N604SK": ("Stan Kroenke (Rams)", "Global 6000", "A7D781", 1.10),
    "N602SK": ("Shahid Khan (Jags)", "Global 6000", "A7D00B", 1.10),
    "N6453":  ("Stephen Ross (Dolphins)", "G-V", "A8835B", 1.05),
    "N151SD": ("Jim Irsay (Colts)", "G-V", "A0D597", 1.05),
    "N68885": ("Woody Johnson (Jets)", "G650", "A92BB5", 1.20),
    "N96UA":  ("Sergey Brin", "G-V", "AD2320", 1.05),
    "N378TP": ("Larry Page", "G-V", "A45B6C", 1.05),
    "N5MV":   ("Michael Bloomberg", "G-V", "A0AC54", 1.05),
    "N47EG":  ("Rupert Murdoch", "G-V", "A5C440", 1.05),
    "N8AG":   ("Warren Buffett", "G-V", "A0B98D", 1.05),
    "N444WT": ("Jackie Chan", "Legacy 650", "A55A8A", 0.85),
    "N950PB": ("Dr. Phil", "G-IV", "AD338F", 1.00),
    "N7KC":   ("Kenny Chesney", "Falcon 900EX", "AAB263", 0.90),
    "N71KR":  ("Luke Bryan", "Citation X", "AA5A9F", 0.75),
    "N474D":  ("Blake Shelton", "Challenger 350", "A5CC20", 0.70),
    "N800PM": ("George Lucas", "G-V", "AAEC1A", 1.05),
    "N10XG":  ("Elton John", "G650", "A0266D", 1.20),
    "N943FL": ("Celine Dion", "Global 7500", "AD194A", 1.15),
    "N701DB": ("Dan Bilzerian", "G-IV", "A959B5", 1.00),
    "N928KG": ("Kenneth Griffin", "G650", "AD209F", 1.20),
    "N626SC": ("Steve Cohen", "G650", "A82EF8", 1.20),
    "N1812D": ("Michael Dell", "G650", "A14C6B", 1.20),
    "N2029B": ("Richard Branson", "Global 6000", "A1943F", 1.10),
    "N444SC": ("S. Truett Cathy (Chick-fil-A)", "G650", "A55A4F", 1.20),
    "N555QB": ("Quicken Loans (Dan Gilbert)", "G650", "A7197A", 1.20),
    "N32MJ":  ("Magic Johnson", "G-IV", "A37449", 1.00),
    "N898NC": ("NetJets (Target)", "G-V", "AC69FF", 1.05)
}

try:
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    # Wipe the table before populating to ensure a clean start
    cursor.execute("TRUNCATE TABLE AircraftStats")
    
    for tail, info in jet_data.items():
        sql = "INSERT INTO AircraftStats (TailNumber, CelebrityName, AircraftModel, HexCode, GallonsPerMile) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (tail, info[0], info[1], info[2], info[3]))
    
    db.commit()
    print(f"Success: {len(jet_data)} records successfully written to JetTrackerDB.")
except Exception as e:
    print(f"Database Error: {e}")
finally:
    db.close()
