from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/receive_finance_application', methods=['POST'])
def receiveFinanceApp():
    try:
        data = request.get_json()
        print(data)
        response = computeAndSendDecision(data)
        print(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'message': 'Stub has recieved application'}), 201
def computeAndSendDecision(data):
    #print(type(request.get_json()["full_name"]))
    print(data["annual_income"])
    if (data["annual_income"] >= int(data["purchase_price"]) * 0.1):
        print("QUALIFIED SO FAR")
    return "HI"

if __name__ == "__main__":
    app.run(debug = True, host='localhost', port='5001')