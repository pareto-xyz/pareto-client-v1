import time
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
        # https://eth-account.readthedocs.io/en/stable/eth_account.html#eth_account.account.Account.sign_message
        message = {
            'method': method,
            'requestPath': uri,
            'body': body,
            'timestamp': timestamp,
        }
        message_hash = encode_defunct(message)
        signed_message = Account.sign_message(message_hash, 
                                              self._private_key)
        return signed_message.signature

    def add_headers(self,
                    method,
                    uri,
                    body,
                    header={},
                    ):
        timestamp = int(time.time())
        signature = self.sign(method, uri, body, timestamp)
        header['pareto-ethereum-address'] = self.address
        header['pareto-signature'] = signature
        header['pareto-timestamp'] = timestamp
        return header
