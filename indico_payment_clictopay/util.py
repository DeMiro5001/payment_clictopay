import requests
from flask import current_app

def get_api_base_url():
    environment = current_app.config['payment_clictopay']['environment']
    return 'https://test.clictopay.com/payment/rest/' if environment == 'test' else 'https://ipay.clictopay.com/payment/rest/'

def create_clictopay_transaction(order_id, amount, return_url, fail_url, language='en'):
    api_base_url = get_api_base_url()
    payload = {
        'userName': current_app.config['payment_clictopay']['merchant_user'],
        'password': current_app.config['payment_clictopay']['merchant_password'],
        'orderNumber': order_id,
        'amount': int(amount * 100),
        'currency': 788,
        'returnUrl': return_url,
        'failUrl': fail_url,
        'language': language,  # Set the language
    }
    response = requests.post(f"{api_base_url}register.do", data=payload)
    response_data = response.json()
    if response_data.get('errorCode') == '0':
        return response_data['formUrl']
    else:
        raise Exception(f"Failed to create payment: {response_data.get('errorMessage')}")


    
    # Sending the payment request
    response = requests.post(f"{api_base_url}/register.do", data=payload)
    response_data = response.json()
    
    if response_data.get('errorCode') == '0':
        return response_data['formUrl']
    else:
        raise Exception(f"Failed to create payment: {response_data.get('errorMessage')}")

def get_clictopay_status(order_id):
    # Get the API base URL from the plugin configuration
    api_base_url = current_app.config['payment_clictopay']['api_base_url']

    payload = {
        'userName': current_app.config['payment_clictopay']['merchant_user'],
        'password': current_app.config['payment_clictopay']['merchant_password'],
        'orderId': order_id,
    }
    
    # Request the order status
    response = requests.post(f"{api_base_url}/getOrderStatus.do", data=payload)
    response_data = response.json()
    return response_data.get('OrderStatus')
