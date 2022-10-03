import time, json
from simplejson.encoder import JSONEncoderForHTML
from eth_account import Account
from eth_account.messages import encode_defunct


class Signer:
    r"""Sign with private key.
    Arguments:
    --
    private_key (string): Private key
    """
    def __init__(self, private_key):
        self.address = Account.from_key(private_key).address
        self._private_key = private_key

    def sign(self,
             method,
             uri,
             body,
             timestamp,
             ):
        r"""Sign a structured message for the backend to parse.
        Arguments:
        --
        method (string): GET or POST
        uri (string): Endpoint path e.g. /ping
        body (Object): Body of the request
        timestamp (integer): Timestamp of the request
        """
        body = json.dumps(body)
        # https://eth-account.readthedocs.io/en/stable/eth_account.html#eth_account.account.Account.sign_message
        message = {
            'method': method,
            'requestPath': uri,
            'body': body,
            'timestamp': timestamp,
        }
        text = JSONEncoderForHTML(separators=(',', ':')).encode(message)
        message_hash = encode_defunct(text=text)
        signed_message = Account.sign_message(message_hash, self._private_key)
        return signed_message.signature.hex()

    def add_headers(self, method, uri, body, header={},):
        timestamp = int(time.time())
        signature = self.sign(method, uri, body, timestamp)
        header['pareto-ethereum-address'] = self.address
        header['pareto-signature'] = signature
        header['pareto-timestamp'] = str(timestamp)
        return header
