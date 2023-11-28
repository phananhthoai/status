from flask import Flask, render_template, jsonify
from os import environ
import subprocess
from datetime import datetime

app = Flask(__name__)
class Server:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
    @property
    def data(self):
        return {
            'name': self.name,
            'ip': self.ip,
        }
servers = [
    Server("Vietnix", "14.225.204.46"),
    Server("CDN-Vietnix", "14.225.255.209"),
    Server("Test", "1.2.3.4")
]
def ping_servers(servers):
    status_summary = []
    for item in servers:
        command = ['ping', '-c', '1', item.ip]
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if result.returncode == 0:
                status_summary.append({**item.data, 'status': 'OK', 'updated_at': time, 'ip': item.ip})
            else:
                status_summary.append({**item.data, 'status': 'ERROR', 'updated_at': time, 'ip': item.ip})
        except subprocess.TimeoutExpired:
            status_summary.append({**item.data, 'status': 'TIMEOUT', 'updated_at': time, 'ip': item.ip})

    return status_summary

@app.route('/api/status', methods=['GET'])
def get_servers_status():
    status_summary = ping_servers(servers)
    return jsonify({'status_summary': status_summary})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/content')

def content():
    status = ping_servers(servers)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return {
        'servers': list(map(lambda x: x.data, servers)),
        'status': status,
        'current_time': current_time,
    }

if __name__ == '__main__':
  app.run('0.0.0.0', '5000', debug=True)
