from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def log_ip():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("ip_logs.txt", "a") as f:
        f.write(f"{timestamp} - {ip}\n")
    
    return f"Hello! Your IP {ip} has been logged."

@app.route('/logs')
def view_logs():
    try:
        with open("ip_logs.txt", "r") as f:
            return f"<pre>{f.read()}</pre>"
    except FileNotFoundError:
        return "No logs yet."
