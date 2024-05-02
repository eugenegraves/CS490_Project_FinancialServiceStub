from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import math
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
app = Flask(__name__)

#hello

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Westwood-18@localhost/cars_dealershipx' #Abdullah Connection
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:great-days321@localhost/cars_dealershipx' #Dylan Connection 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:A!19lopej135@localhost/cars_dealershipx' # joan connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12340@192.168.56.1/cars_dealershipx'# Ismael connection
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:*_-wowza-shaw1289@localhost/cars_dealershipx' #hamza connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:42Drm400$!@localhost/cars_dealershipx'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

class Customer(db.Model):
    __tablename__ = 'customers'

    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    phone = db.Column(db.String(45), nullable=False)
    Address = db.Column(db.String(45), nullable=True)
    password = db.Column(db.String(45), nullable=False)
    usernames = db.Column(db.String(45), nullable=True, unique=True)
    social_security = db.Column(db.Integer, nullable=False, unique=True)
    
    __table_args__ = (
        CheckConstraint('LENGTH(CAST(social_security AS CHAR(9))) = 9'),
    )
    def __init__(self, first_name, last_name, email, phone, password, Address=None, usernames=None, social_security=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.Address = Address
        self.password = password
        self.usernames = usernames
        self.social_security = social_security


class CustomersBankDetails(db.Model):
    __tablename__ = 'customers_bank_details'

    bank_detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bank_name = db.Column(db.String(45), nullable=False)
    account_number = db.Column(db.String(20), nullable=False)  
    routing_number = db.Column(db.String(20), nullable=False)  
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    credit_score = db.Column(db.Integer)  


    customer = db.relationship('Customer', backref=db.backref('bank_details', lazy=True))



@app.route('/receive_finance_application', methods=['POST'])
def receiveFinanceApp():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    response = computeAndSendDecision(data)
    print(response.get_json())
    print(type(response.get_json()))
    return response.get_json()

def computeAndSendDecision(data):
    customer_id = data.get('customer_id')
    bank_details = CustomersBankDetails.query.filter_by(customer_id=customer_id).first()

    if bank_details and bank_details.credit_score is not None: 
        credit_score = bank_details.credit_score
    else:
        credit_score = random.randint(580, 850)

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
    customer_id = data.get('customer_id')
    monthly_income = int(data["annual_income"]) / 12
    down_payment = int(data["purchase_price"]) * 0.2
    monthly_payment = math.ceil(((int(data["purchase_price"]) - down_payment) * (apr / 12) * (1 + (apr / 12)) ** (loan_term)) / ((1 + (apr / 12)) ** (loan_term) - 1))
    debt_to_income_ratio = ((monthly_payment - down_payment) / monthly_income) * 100    
    if (debt_to_income_ratio <= 36):
        if (credit_score >= 600):
            response = {
                'status': 'approved',
                'credit_score': credit_score,
                'customer_id': customer_id,
                'terms': {
                    'principal': data["purchase_price"],
                    'apr': apr,
                    'loan_term': loan_term,
                    'down_payment': down_payment,
                    'monthly_payment': monthly_payment
                }
            }
            Credit_score(response)  
            return jsonify(response)
        else:
            response = {
                'status': 'declined',
                'credit_score': credit_score,
                'customer_id': customer_id,
                'reason': 'low credit score'
            }
            Credit_score(response)  
            return jsonify(response)
    else:
        response = {
            'status': 'declined',
            'credit_score': credit_score,
            'customer_id': customer_id,
            'reason': 'cannot afford'
        }
        Credit_score(response)    
        return jsonify(response)
def Credit_score(response):
    customer_id = response.get('customer_id')
    credit_score = response.get('credit_score')
    if credit_score is not None and customer_id is not None: 
        customer_bank_details = CustomersBankDetails.query.filter_by(customer_id=customer_id).first()
        if customer_bank_details:
            customer_bank_details.credit_score = credit_score
            db.session.commit()
        else:
            return jsonify({'error': 'Customer bank details not found'}), 404



@app.route('/add-customerBankInfo/<int:customer_id>', methods=['POST'])
def add_or_update_customer_bank_info(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        bank_name = request.json.get('bank_name')
        account_number = str(request.json.get('account_number'))
        routing_number = str(request.json.get('routing_number'))

        if not all([bank_name, account_number, routing_number]):
            return jsonify({'error': 'Missing bank information'}), 400

        # Validate account number and routing number format (you may need more sophisticated validation)
        if not (account_number.isdigit() and routing_number.isdigit()):
            return jsonify({'error': 'Invalid account or routing number format'}), 400

        existing_bank_details = CustomersBankDetails.query.filter_by(customer_id=customer_id).first()

        if existing_bank_details:
            existing_bank_details.bank_name = bank_name
            existing_bank_details.account_number = account_number
            existing_bank_details.routing_number = routing_number
        else:
            new_bank_details = CustomersBankDetails(
                bank_name=bank_name,
                account_number=account_number,
                routing_number=routing_number,
                customer_id=customer_id
            )
            db.session.add(new_bank_details)

        db.session.commit()

        return jsonify({'message': 'Bank details added/updated successfully'}), 201
    else:
        return jsonify({'error': 'Customer not found'}), 404


       

if __name__ == "__main__":
    app.run(debug = True, host='localhost', port='5001')