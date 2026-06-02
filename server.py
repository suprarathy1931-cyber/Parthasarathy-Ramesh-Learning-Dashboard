from flask import Flask, jsonify, request
from flask_cors import CORS
import csv, json, os

app = Flask(__name__)
CORS(app)

CSV_FILE = os.path.join(os.path.dirname(__file__), 'progress.csv')

DEFAULT_STATE = {
    "learnChecked": {},
    "projectBuilt": {},
    "phaseOpen": {},
    "dsaTopics": {"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0},
    "dsaHeatmap": [0]*182,
    "langPct": {str(i):0 for i in range(18)},
    "langSessions": {str(i):0 for i in range(18)},
    "schedule": {str(i):False for i in range(35)},
    "notes": [],
    "xp": 0,
    "streak": 0,
    "lastActive": ""
}

def load_csv():
    if not os.path.exists(CSV_FILE):
        return dict(DEFAULT_STATE)
    state = dict(DEFAULT_STATE)
    try:
        with open(CSV_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2:
                    key, val = row
                    try:
                        state[key] = json.loads(val)
                    except:
                        state[key] = val
    except Exception as e:
        print(f"Load error: {e}")
    return state

def save_csv(data):
    try:
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for key, val in data.items():
                writer.writerow([key, json.dumps(val)])
        return True
    except Exception as e:
        print(f"Save error: {e}")
        return False

@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify(load_csv())

@app.route('/api/state/bulk', methods=['POST'])
def save_state():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
    if save_csv(data):
        return jsonify({"status": "ok"})
    return jsonify({"error": "Save failed"}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "running"})

if __name__ == '__main__':
    print("🚀 Dev Roadmap Tracker running at http://localhost:7411")
    app.run(port=7411, debug=True)
