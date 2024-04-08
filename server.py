from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/receive_finance_application', methods=['POST'])
def receiveFinanceApp():
    try:
        data = request.get_json()
        print(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'message': 'Stub has recieved application'}), 201

if __name__ == "__main__":
    app.run(debug = True, host='localhost', port='5001')