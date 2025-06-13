from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
@app.route('/time', methods=['GET'])
def get_time():
    now = datetime.now()
    hour = now.hour
    is_daytime = 6 <= hour <= 18
    return jsonify({
        "time": now.strftime("%H:%M:%S"),
        "hour": hour,
        "is_daytime": is_daytime
    })

if __name__ == '__main__':
    app.run(debug=True)