from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import math

app = Flask(__name__)
CORS(app)

@app.route('/receive_finance_application', methods=['POST'])
def receiveFinanceApp():
    try:
        data = request.get_json()
        print(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    response = computeAndSendDecision(data)
    print(response.get_json())
    return jsonify({'message': 'Stub has recieved application'}), 201
def computeAndSendDecision(data):
    credit_score = random.randint(580, 850)
    print(credit_score)
    if credit_score >= 780:
        apr = 0.035
        loan_term = 60
    elif credit_score >= 720:
        apr = 0.040
        loan_term = 60
    elif credit_score >= 660:
        apr = 0.050
        loan_term = 72
    elif credit_score >= 600:
        apr = 0.070
        loan_term = 72
    else:
        apr = 0.1
        loan_term = 72

    monthly_income = int(data["annual_income"]) / 12
    monthly_payment = math.ceil((int(data["purchase_price"]) * (apr / 12) * (1 + (apr / 12)) ** (loan_term)) / ((1 + (apr / 12)) ** (loan_term) - 1))
    print(monthly_payment)
    debt_to_income_ratio = (monthly_payment / monthly_income) * 100
    if (debt_to_income_ratio <= 36):
        if (credit_score >= 600):
            response = {
                'status': 'approved',
                'terms': {
                    'principal': data["purchase_price"],
                    'apr': apr,
                    'loan_term': loan_term,
                    'monthly_payment': monthly_payment
                }
            }
            return jsonify(response)
        else:
            response = {
                'status': 'declined',
                'reason': 'low credit score'
            }
            return jsonify(response)
    else:
        response = {
            'status': 'declined',
            'reason': 'cannot afford'
        }
        return jsonify(response)
if __name__ == "__main__":
    app.run(debug = True, host='localhost', port='5001')