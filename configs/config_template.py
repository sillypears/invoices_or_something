class Config(object):
    DEBUG = False
    PAYPAL_ACCOUNT = ''
    PAYPAL_CLIENT_ID = ''
    PAYPAL_SECRET = ''
    PAYPAL_API_URL = 'api-m.paypal.com'
    INVOICE_EMAIL = ''
    INVOICE_SITE = ''
    INVOICE_NOTE = "If you're not getting punched in the face, you're not living life to the fullest. Thanks again!"
    INVOICE_TANDC = "All goods are handmade which may cause slight variations between what you receive. Please reach out if there are any issues with your ability to use the product outside of this note. I test to make sure all keycaps fit snuggly on a Kailh Halo stem."
    INVOICE_ADDLNOTES = "Pizza"
    INVOICE_TERM = 'No refunds after 30 days.'
    INVOICE_MEMO = 'This is a long contract'
    INVOICE_TIP = True


class Development(Config):
    DEBUG = True
    PAYPAL_ACCOUNT = ""
    PAYPAL_CLIENT_ID = ""
    PAYPAL_SECRET = ""
    PAYPAL_API_URL = 'api-m.sandbox.paypal.com'

class Production(Config):
    pass

app_config = {
    'dev': Development,
    'prd': Production
}