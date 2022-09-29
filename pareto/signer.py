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

    def sign(self, message):
        # https://eth-account.readthedocs.io/en/stable/eth_account.html#eth_account.account.Account.sign_message
        message_hash = encode_defunct(text=message)
        signed_message = Account.sign_message(message_hash, 
                                              self._private_key)
        return signed_message.signature

    def add_headers(self, message, header={}):
        signature = self.sign(message)
        header['address'] = self.address
        header['signature'] = signature
        return header
