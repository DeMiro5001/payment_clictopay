from flask import request, redirect, render_template, flash
from indico.modules.events.payment.controllers import PaymentController
from indico_payment_clictopay.util import create_clictopay_transaction
from indico.modules.events.payment.models.transactions import PaymentTransaction
from indico.modules.events.payment.util import update_transaction_status
from indico.util.i18n import _

class ClicToPayPayment(PaymentController):
    def _process(self):
        event = self.event
        order_id = f"{event.id}-{self.registration.id}"  # Create a unique order ID
        return_url = url_for('payment_clictopay.payment_return', _external=True)
        fail_url = url_for('payment_clictopay.payment_fail', _external=True)

        # Call the utility function to create a payment request
        form_url = create_clictopay_transaction( order_id, self.registration.price, return_url, fail_url, language='fr')

        # Render the payment form template
        return render_template('payment_clictopay:event_payment_form.html', form_url=form_url, order_id=order_id)


class ClicToPayReturn(PaymentController):
    def _process(self):
        order_id = request.args.get('orderId')
        status = get_clictopay_status(order_id)  # Utility function to check payment status

        if status == '2':  # Payment success
            update_transaction_status(self.registration.transaction, PaymentTransaction.Status.success)
            flash(_('Your payment has been successfully processed.'), 'success')
        else:  # Payment failed or pending
            update_transaction_status(self.registration.transaction, PaymentTransaction.Status.failed)
            flash(_('Your payment could not be processed. Please try again.'), 'error')

        return redirect(self.event.get_absolute_url())

class ClicToPayTransactionDetails(PaymentController):
    def _process(self):
        transaction = self.registration.transaction
        return render_template('payment_clictopay:transaction_details.html', transaction=transaction)
