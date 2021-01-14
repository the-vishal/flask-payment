from payment_server import app
from flask import json

def test_payment_server():        
    response = app.test_client().post(
        '/api-v1/process-payment/',
        data=json.dumps({
			"CreditCardNumber":"79927398713",
			"CardHolder":"Anonymous",
			"ExpirationDate":"2022-08-11T05:26:03.869245",
			"Amount":9
		}),
        content_type='application/json',
    )

    text = response.get_data(as_text=True)
    assert (response.status_code == 500 and text == 'Any error') or (response.status_code == 200 and text == 'Payment is processed') 