from flask import Blueprint
from indico_payment_clictopay.controllers import (
    ClicToPayPayment,
    ClicToPayReturn,
    ClicToPayTransactionDetails
)

blueprint = Blueprint(
    'payment_clictopay',
    __name__,
    url_prefix='/event/<int:event_id>/registrations/<int:reg_id>/payment/clictopay'
)

# Routes
blueprint.add_url_rule('/', 'initiate_payment', ClicToPayPayment)
blueprint.add_url_rule('/return', 'payment_return', ClicToPayReturn)
blueprint.add_url_rule('/details', 'transaction_details', ClicToPayTransactionDetails)

