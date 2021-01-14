from flask import Flask, jsonify, request
from marshmallow import ValidationError
import json
from utils import PaymentSchema, choose_gateway

#============================ APP & API CONFIGURATIONS ==========================
app = Flask(__name__)
# api = Api(app)
# app.config["DEBUG"] = True
app.config['PROPAGATE_EXCEPTIONS'] = True



@app.errorhandler(500)
def internal_error(error):
    return "Any error", 500

# ============================ API ROUTES =======================================

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Flask based Payment Service</h1>
    <l>1. Run the server.</l><br />
    <l>2. try this cURL: </l><br />

    <pre>curl --location --request POST 'http://localhost:5000/api-v1/process-payment/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "CreditCardNumber":"79927398713",
        "CardHolder":"Anonymous",
        "ExpirationDate":"2021-08-11T05:26:03.869245",
        "Amount":9
    }'</pre><br />
    <l> 3. To run the test case run py.test</l>
    '''


@app.route('/api-v1/process-payment/', methods=['POST'])
def ProcessPayment():
    req_data = request.json
    schema = PaymentSchema()
    
    try:
        res = schema.load(req_data)
    except ValidationError as err:
        # print(err.messages)
        return "The request is invalid", 400

    gateway, retries = choose_gateway(res.get('Amount'))
    is_processed = gateway(max_retries=retries).checkout()

    if is_processed:
        return "Payment is processed", 200
    else:
        return "Any error", 500



#========================== SCRIPT SECTION ===============================

if __name__ == '__main__':
    app.run()