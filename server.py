from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime

app = Flask(__name__)
count=1
conn = psycopg2.connect(
    dbname="dashboardDB",
    user="postgres",
    password="kunal9922",
    host="localhost",
    port="5432"
)
@app.route('/', methods=['POST'])
def webStart():
    return "Hello React"
@app.route('/log', methods=['POST'])
def log_api_hit():
    global count
    data = request.json
    cursor = conn.cursor()
    # Ensure data does not exceed field length limits
    _id = data.get('id', '')[:10]+str(count)
    request_id = data.get('request_id', '')[:50]
    request_type = data.get('request_type', '')[:10]
    payload = data.get('payload', '')[:5000]  # assuming TEXT can handle large data
    content_type = data.get('content_type', '')[:100]
    ip_address = request.remote_addr[:50]
    os = data.get('os', '')[:50]
    user_agent = request.headers.get('User-Agent', '')[:200]
    count = count + 1
    cursor.execute("""
        INSERT INTO api_hits (id, request_id, request_type, request_time, payload, content_type, ip_address, os, user_agent)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        _id,
        request_id,
        request_type,
        datetime.now(),
        payload,
        content_type,
        ip_address,
        os,
        user_agent
    ))
    conn.commit()
    cursor.close()
    return jsonify({'status': 'success'}), 201

@app.route('/api/data', methods=['GET'])
def get_api_hits():
    print("method called")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM api_hits")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]
    cursor.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
