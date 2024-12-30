import requests
from flask import current_app

def create_clictopay_transaction(order_id, amount, return_url, fail_url):
    # Get the API base URL from the plugin configuration
    api_base_url = current_app.config['payment_clictopay']['api_base_url']

    payload = {
        'userName': current_app.config['payment_clictopay']['merchant_user'],
        'password': current_app.config['payment_clictopay']['merchant_password'],
        'orderNumber': order_id,
        'amount': int(amount * 100),  # Convert to minor units (e.g., cents)
        'currency': 788,  # TND (ISO 4217)
        'returnUrl': return_url,
        'failUrl': fail_url,
    }
    
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
