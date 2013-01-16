
import json
import requests
from . import exceptions

RECEIPT_PRODUCTION_VALIDATION_URL = "https://buy.itunes.apple.com/verifyReceipt"
RECEIPT_SANDBOX_VALIDATION_URL = "https://sandbox.itunes.apple.com/verifyReceipt"

USE_PRODUCTION = True
USE_SANDBOX = False

def set_verification_mode(mode):
    """Set global verification mode that where allows production or sandbox.
    `production`, `sandbox`, `review` or `reject` availble. Or raise
    an exception.

    `production`: Allows production receipts only. Default.
    `sandbox`: Allows sandbox receipts only.
    `review`: Allows production receipts but use sandbox as fallback.
    `reject`: Reject all receipts.
    """
    global USE_PRODUCTION, USE_SANDBOX
    if mode == 'production':
        USE_PRODUCTION = True
        USE_SANDBOX = False
    elif mode == 'sandbox':
        USE_PRODUCTION = False
        USE_SANDBOX = True
    elif mode == 'review':
        USE_PRODUCTION = True
        USE_SANDBOX = True
    elif mode == 'reject':
        USE_PRODUCTION = False
        USE_SANDBOX = False
    else:
        raise exceptions.ModeNotAvailable(mode)


class Request(object):
    """Validation request with raw receipt. Receipt must be base64 encoded string.
    Use `verify` method to try verification and get Receipt or exception.
    """
    def __init__(self, receipt, **kwargs):
        self.receipt = receipt
        self.use_production = kwargs.get('use_production', USE_PRODUCTION)
        self.use_sandbox = kwargs.get('use_sandbox', USE_SANDBOX)
        self.response = None
        self.result = None

    def __repr__(self):
        valid = None
        if self.result:
            valid = self.result['status'] == 0
        return u'<Request(valid:{0}, data:{1}...)>'.format(valid, self.receipt[:20])

    def verify_from(self, url):
        """Try verification from given url."""
        self.response = requests.post(url, json.dumps({'receipt-data': self.receipt}), verify=False)
        if self.response.status_code != 200:
            raise exceptions.ItunesServerNotAvailable(self.response.status_code, self.response.text)
        self.result = json.loads(self.response.text)
        status = self.result['status']
        if status != 0:
            raise exceptions.InvalidReceipt(status)
        return self.result
   
    def validate(self):
        return self.verify()

    def verify(self):
        """Try verification with settings. Returns a Receipt object if successed.
        Or raise an exception. See `self.response` or `self.result` to see details.
        """
        receipt = None
        if self.use_production:
            try:
                receipt = self.verify_from(RECEIPT_PRODUCTION_VALIDATION_URL)
            except exceptions.InvalidReceipt, e:
                pass
        if not receipt and self.use_sandbox:
            receipt = self.verify_from(RECEIPT_SANDBOX_VALIDATION_URL)
        if not receipt:
            raise e
        return Receipt(receipt)


class Receipt(object):
    """Pretty interface for decoded receipt obejct.
    """
    def __init__(self, data):
        self.data = data
        self.receipt = data['receipt']
        self.receipt_keys = self.receipt.keys()

    def __repr__(self):
        return u'<Receipt({0}, {1})>'.format(self.status, self.receipt)

    @property
    def status(self):
        return self.data['status']

    def __getattr__(self, key):
        if key in self.receipt_keys:
            return self.receipt[key]
        try:
            return super(Receipt, self).__getattr__(key)
        except AttributeError:
            return super(Receipt, self).__getattribute__(key) 