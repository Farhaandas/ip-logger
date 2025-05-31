from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <html>
      <head><title>IP Logger</title></head>
      <body>
        <h1>Logging your IP...</h1>
        <p>Check the server log or ip_logs.txt</p>
        <script>
          fetch('https://api.ipify.org?format=json')
            .then(response => response.json())
            .then(data => {
              console.log("Your Public IP is:", data.ip);
              fetch('/log_ip', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ ip: data.ip })
              })
              .then(response => response.json())
              .then(result => console.log(result))
              .catch(error => console.error("POST failed:", error));
            })
            .catch(error => console.error("Fetch IP failed:", error));
        </script>
      </body>
    </html>
    """

@app.route('/log_ip', methods=['POST'])
def log_ip():
    data = request.get_json()

    # Try to get real client IP via proxy header (Render, etc.)
    forwarded_for = request.headers.get('X-Forwarded-For', '')
    proxy_ip = forwarded_for.split(',')[0].strip() if forwarded_for else request.remote_addr

    # Use external IP from client if available, else use proxy IP
    ip = data.get('ip', proxy_ip)

    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    log_entry = f"{timestamp} - IP: {ip}"
    
    print(log_entry)  # Logs to terminal or Render logs

    try:
        with open("ip_logs.txt", "a") as f:
            f.write(log_entry + "\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")
        
    return jsonify({"status": "logged", "ip": ip})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Required for Render
    app.run(host="0.0.0.0", port=port, debug=True)
