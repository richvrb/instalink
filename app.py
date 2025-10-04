from flask import Flask, request, redirect, render_template_string
from datetime import datetime
import os
import requests
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Configuratie
INSTAGRAM_USERNAME = "richvrb"
REDIRECT_URL = "https://www.nu.nl"

# Database connectie
def get_db_connection():
    # Probeer eerst DATABASE_URL, anders bouw uit Railway variabelen
    database_url = os.environ.get('DATABASE_URL')

    if database_url:
        conn = psycopg2.connect(database_url)
    else:
        # Gebruik Railway's individuele PostgreSQL variabelen
        conn = psycopg2.connect(
            host=os.environ.get('PGHOST'),
            database=os.environ.get('POSTGRES_DB'),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            port=5432
        )
    return conn

# Maak database tabel aan als deze niet bestaat
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tracking_data (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            ip_address VARCHAR(45) NOT NULL,
            country VARCHAR(100),
            city VARCHAR(100),
            browser TEXT,
            device VARCHAR(50),
            referrer TEXT
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

# Initialiseer database bij opstarten
try:
    init_db()
except Exception as e:
    print(f"Database initialization error: {e}")

def get_location(ip):
    """Haal locatie op basis van IP adres"""
    try:
        if ip == '127.0.0.1' or ip.startswith('192.168'):
            return 'Local', 'Local'
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=3)
        data = response.json()
        if data['status'] == 'success':
            return data.get('country', 'Unknown'), data.get('city', 'Unknown')
    except:
        pass
    return 'Unknown', 'Unknown'

@app.route('/')
def track():
    """Hoofdroute - log bezoeker en redirect naar Instagram"""
    # Verzamel data
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ',' in ip:
        ip = ip.split(',')[0].strip()

    country, city = get_location(ip)
    browser = request.headers.get('User-Agent', 'Unknown')
    referrer = request.headers.get('Referer', 'Direct')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Bepaal device type
    user_agent = browser.lower()
    if 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent:
        device = 'Mobile'
    elif 'tablet' in user_agent or 'ipad' in user_agent:
        device = 'Tablet'
    else:
        device = 'Desktop'

    # Sla data op in database
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO tracking_data (timestamp, ip_address, country, city, browser, device, referrer) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (timestamp, ip, country, city, browser, device, referrer)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error writing to database: {e}")

    # Redirect naar Instagram
    return redirect(REDIRECT_URL, code=302)

@app.route('/dashboard')
def dashboard():
    """Dashboard om tracking data te bekijken"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM tracking_data ORDER BY timestamp DESC')
        data = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")
        data = []

    # Bereken statistieken
    total_clicks = len(data)
    countries = {}
    devices = {}

    for row in data:
        country = row['country']
        device = row['device']
        countries[country] = countries.get(country, 0) + 1
        devices[device] = devices.get(device, 0) + 1

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Instagram Bio Link Tracker - @{INSTAGRAM_USERNAME}</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            }}
            h1 {{
                color: #333;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }}
            .stat-box {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
            }}
            .stat-box h3 {{
                margin: 0 0 10px 0;
                font-size: 14px;
                opacity: 0.9;
            }}
            .stat-box .number {{
                font-size: 32px;
                font-weight: bold;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #667eea;
                color: white;
                font-weight: 600;
            }}
            tr:hover {{
                background-color: #f5f5f5;
            }}
            .refresh {{
                background: #667eea;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                margin-bottom: 20px;
            }}
            .refresh:hover {{
                background: #5568d3;
            }}
        </style>
        <meta http-equiv="refresh" content="30">
    </head>
    <body>
        <div class="container">
            <h1>📊 Instagram Bio Link Tracker - @{INSTAGRAM_USERNAME}</h1>
            <button class="refresh" onclick="location.reload()">🔄 Refresh</button>

            <div class="stats">
                <div class="stat-box">
                    <h3>TOTAL CLICKS</h3>
                    <div class="number">{total_clicks}</div>
                </div>
                <div class="stat-box">
                    <h3>COUNTRIES</h3>
                    <div class="number">{len(countries)}</div>
                </div>
                <div class="stat-box">
                    <h3>TOP DEVICE</h3>
                    <div class="number">{max(devices.items(), key=lambda x: x[1])[0] if devices else 'N/A'}</div>
                </div>
            </div>

            <h2>📍 Clicks by Country</h2>
            <table>
                <tr>
                    <th>Country</th>
                    <th>Clicks</th>
                </tr>
                {''.join([f'<tr><td>{country}</td><td>{count}</td></tr>' for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True)])}
            </table>

            <h2>📱 Recent Clicks</h2>
            <table>
                <tr>
                    <th>Timestamp</th>
                    <th>IP</th>
                    <th>Country</th>
                    <th>City</th>
                    <th>Device</th>
                    <th>Referrer</th>
                </tr>
                {''.join([f"<tr><td>{row['timestamp']}</td><td>{row['ip_address']}</td><td>{row['country']}</td><td>{row['city']}</td><td>{row['device']}</td><td>{row['referrer'][:50]}...</td></tr>" for row in data])}
            </table>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
