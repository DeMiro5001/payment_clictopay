from indico.core.plugins import IndicoPlugin, IndicoPluginBlueprint
from indico.modules.events.payment import PaymentEventSettingsProxy
from indico.web.forms import IndicoForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

class ClicToPaySettingsForm(IndicoForm):
    merchant_user = StringField('Merchant Username', validators=[DataRequired()])
    merchant_password = StringField('Merchant Password', validators=[DataRequired()])
    api_environment = SelectField('API Environment', choices=[('test', 'Test'), ('production', 'Production')], validators=[DataRequired()])

    def populate_obj(self, obj):
        super().populate_obj(obj)
        if self.api_environment.data == 'test':
            obj.api_base_url = 'https://test.clictopay.com/payment/rest'
        elif self.api_environment.data == 'production':
            obj.api_base_url = 'https://ipay.clictopay.com/payment/rest'

class ClicToPayPlugin(IndicoPlugin):
    """ClicToPay Payment Plugin"""

    configurable = True
settings_proxy = PaymentEventSettingsProxy('payment_clictopay', {
    'merchant_user': '',
    'merchant_password': '',
    'api_base_url': 'https://test.clictopay.com/payment/rest/',  # Default to test
    'environment': 'test',  # Add a new setting for environment
})

    def init(self):
        super().init()
        self.template_hook('event-management-sidemenu', 'payment_clictopay:sidemenu')

    def get_settings_form(self):
        return ClicToPaySettingsForm()

