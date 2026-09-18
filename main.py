from flask import Flask, render_template, request, jsonify
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

latest_game_data = {
    "multiplier": "Waiting...",
    "status": "Connecting...",
    "history": []
}

connected_clients = set()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/receive-data', methods=['POST'])
def receive_data():
    global latest_game_data
    try:
        req_data = request.json
        payload = req_data.get('data')
        
        if payload:
            latest_game_data["multiplier"] = "Live Connected!"
            latest_game_data["status"] = "Active"
            # সব কানেক্টेड ক্লায়েন্টকে লাইভ ডাটা ব্রডকাস্ট করা
            for client in list(connected_clients):
                try:
                    client.send(jsonify(latest_game_data).get_data(as_text=True))
                except:
                    connected_clients.remove(client)
                    
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@sock.route('/ws')
def ws(ws):
    connected_clients.add(ws)
    try:
        while True:
            data = ws.receive()
    except:
        pass
    finally:
        connected_clients.remove(ws)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
