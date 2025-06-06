from flask import Flask, request, jsonify

app = Flask(__name__)

alarm_state = "off"

@app.route('/turn_alarm', methods=['GET'])
def turn_alarm():
    state = request.args.get('state')

    if state not in ['on', 'off']:
        return jsonify({'error': 'Invalid state. Use ?state=on or ?state=off'}), 400

    global alarm_state
    alarm_state = state

    return jsonify({'state': f'{state}'}), 200

@app.route('/get_state', methods=['GET'])
def get_status():
    global alarm_state
    return jsonify({'state': f'{alarm_state}'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)



