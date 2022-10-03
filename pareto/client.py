from pareto.signer import Signer
from pareto import constants
from pareto.utils import get_query_path, create_session, make_request


class Client:
    r"""Client for interacting with the Pareto API.
    Arguments:
    --
    host (string): Host for the endpoint
    eth_private_key (Optional[string], default: None): Private key for ETH
    timeout (integer): Number of ms to wait prior to timeout
    """

    def __init__(self, host, eth_private_key=None, timeout=constants.DEFAULT_API_TIMEOUT):
        if host.endswith('/'):
            host = host[:-1]

        # Create public and private versions
        self._public = PublicClient(host, timeout=timeout)
        self._private = None

        if eth_private_key is not None:
            signer = Signer(eth_private_key)
            # Open private only if the key is provided
            self._private = PrivateClient(host, signer, timeout=timeout)

    @property
    def public(self):
        r"""Get the public module, used for interacting with public endpoints"""
        return self._public

    @property
    def private(self):
        r"""Get the private module, used for interacting with private endpoints"""
        if self._private is None:
            raise Exception('Private endpoints not supported ' + 
                            'since private key was not specified')
        return self._private


class PublicClient:
    r"""Public client for interacting with the Pareto public API.
    Arguments:
    --
    host (string): Host URL path
    timeout (integer): Number of ms to wait prior to timeout
    """
    def __init__(self, host, timeout=constants.DEFAULT_API_TIMEOUT):
        self.host = host
        self.timeout = timeout
        self.session = create_session()

    def _get(self, request_path, headers=None, params={}):
        r"""General GET request
        Arguments:
        --
        request_path (string): endpoint e.g. /ping. Includes URI params
        params (Dict[string, any]): Map of query parameters
        """
        uri = get_query_path(f'{self.host}{request_path}', params)
        return make_request(self.session,
                            uri,
                            'GET',
                            headers=headers,
                            timeout=self.timeout,
                            )

    def ping(self):
        r"""Endpoint to ping server to check communication."""
        uri = '/ping'
        return self._get(uri)

    def get_depth(self, underlying, strike, order_type):
        r"""Endpoint to get the depth of the order book.
        Arguments:
        --
        underlying: see `constants.VALID_UNDERLYING`
        strike: see `constants.VALID_STRIKE`
        order_type: see `constants.VALID_ORDER_TYPE`
        """
        assert underlying in constants.VALID_UNDERLYING
        assert strike in constants.VALID_STRIKE
        assert order_type in constants.VALID_ORDER_TYPE
        uri = f'/public/depth/{underlying}'
        params = {
            'strike': strike,
            'isCall': order_type,
        }
        return self._get(uri, params=params)

    def get_expiry(self, underlying):
        r"""Endpoint to get the active expiry of the order book.
        Arguments:
        --
        underlying: see `constants.VALID_UNDERLYING`
        """
        assert underlying in constants.VALID_UNDERLYING
        uri = f'/public/expiry/{underlying}'
        return self._get(uri)

    def get_sigma(self, underlying, strike, order_type, order_side):
        r"""Endpoint to look up an implied volatility.
        Arguments:
        --
        underlying: see `constants.VALID_UNDERLYING`
        strike: see `constants.VALID_STRIKE`
        order_type: see `constants.VALID_ORDER_TYPE`
        order_side: see `constants.VALID_ORDER_SIDE`
        """
        assert underlying in constants.VALID_UNDERLYING
        assert strike in constants.VALID_STRIKE
        assert order_type in constants.VALID_ORDER_TYPE
        assert order_side in constants.VALID_ORDER_SIDE
        uri = f'/public/sigma/{underlying}'
        params = {
            'strike': strike,
            'isCall': order_type,
            'isBuy': order_side,
        }
        return self._get(uri, params=params)

    def get_price(self,
                  underlying,
                  strike,
                  quantity,
                  order_type,
                  order_side,
                  ):
        r"""Endpoint to get market price of a potential order.
        Arguments:
        --
        underlying: see `constants.VALID_UNDERLYING`
        quantity (integer): Number of units in order. Rounded to nearest 0.01.
        strike: see `constants.VALID_STRIKE`
        order_type: see `constants.VALID_ORDER_TYPE`
        order_side: see `constants.VALID_ORDER_SIDE`
        """
        assert underlying in constants.VALID_UNDERLYING
        assert strike in constants.VALID_STRIKE
        assert order_type in constants.VALID_ORDER_TYPE
        assert order_side in constants.VALID_ORDER_SIDE
        quantity = round(quantity, 2)
        assert quantity > 0
        uri = f'/public/price/market/{underlying}'
        params = {
            'strike': strike,
            'quantity': quantity,
            'isCall': order_type,
            'isBuy': order_side,
        }
        return self._get(uri, params=params)

    def get_strikes(self, underlying):
        r"""Endpoint to get market price of a potential order.
        Arguments:
        --
        underlying: see `constants.VALID_UNDERLYING`
        """
        assert underlying in constants.VALID_UNDERLYING
        uri = f'/public/price/strikes/{underlying}'
        return self._get(uri)

    def get_mark(self, underlying):
        r"""Endpoint to get Black-Scholes mark price of active call and put strikes.
        Arguments:
        --
        underlying: see `constants.VALID_UNDERLYING`
        """
        assert underlying in constants.VALID_UNDERLYING
        uri = f'/public/price/mark/{underlying}'
        return self._get(uri)

    def get_greeks(self, underlying, strike, order_type):
        r"""Endpoint to get greeks of a specified option.
        Arguments:
        --
        underlying: see `constants.VALID_UNDERLYING`
        strike: see `constants.VALID_STRIKE`
        order_type: see `constants.VALID_ORDER_TYPE`
        """
        assert underlying in constants.VALID_UNDERLYING
        assert strike in constants.VALID_STRIKE
        assert order_type in constants.VALID_ORDER_TYPE
        uri = f'/public/price/greeks/{underlying}'
        params = {
            'strike': strike,
            'isCall': order_type,
        }
        return self._get(uri, params=params)

    def get_breakeven(self,
                      underlying,
                      strike,
                      order_type,
                      order_side,
                      ):
        r"""Endpoint to get breakeven price of a specified order.
        Arguments:
        --
        underlying: see `constants.VALID_UNDERLYING`
        strike: see `constants.VALID_STRIKE`
        order_type: see `constants.VALID_ORDER_TYPE`
        order_side: see `constants.VALID_ORDER_SIDE`
        """
        assert underlying in constants.VALID_UNDERLYING
        assert strike in constants.VALID_STRIKE
        assert order_type in constants.VALID_ORDER_TYPE
        assert order_side in constants.VALID_ORDER_SIDE
        uri = f'/public/price/breakeven/{underlying}'
        params = {
            'strike': strike,
            'isCall': order_type,
            'isBuy': order_side,
        }
        return self._get(uri, params=params)

    def get_initial_margin_new_order(self,
                                     underlying,
                                     strike,
                                     quantity,
                                     order_type,
                                     order_side,
                                     ):
        r"""Endpoint to get breakeven price of a specified order.
        Arguments:
        --
        underlying: see `constants.VALID_UNDERLYING`
        quantity (integer): Number of units in order. Rounded to nearest 0.01.
        strike: see `constants.VALID_STRIKE`
        order_type: see `constants.VALID_ORDER_TYPE`
        order_side: see `constants.VALID_ORDER_SIDE`
        """
        assert underlying in constants.VALID_UNDERLYING
        assert strike in constants.VALID_STRIKE
        assert order_type in constants.VALID_ORDER_TYPE
        assert order_side in constants.VALID_ORDER_SIDE
        quantity = round(quantity, 2)
        assert quantity > 0
        uri = f'/public/price/margin/{underlying}'
        params = {
            'strike': strike,
            'quantity': quantity,
            'isCall': order_type,
            'isBuy': order_side,
        }
        return self._get(uri, params=params)


class PrivateClient:
    r"""Private client for interacting with the Pareto private API.
    Arguments:
    --
    host (string): Host URL path
    signer (Signer): Class to sign transactions for authentication
    timeout (integer): Number of ms to wait prior to timeout
    """
    def __init__(self, host, signer, timeout=constants.DEFAULT_API_TIMEOUT):
        self.host = host
        self.signer = signer
        self.timeout = timeout
        self.session = create_session()

    def _get(self, request_path, headers=None, params={}):
        r"""General GET request
        Arguments:
        --
        request_path (string): Endpoint e.g. /ping. Includes URI params
        params (Dict[string, any]): Dictionary of query parameters
        """
        uri = get_query_path(f'{self.host}{request_path}', params)
        if headers is None:
            headers = {}
        headers = self.signer.add_headers('GET',
                                          get_query_path(request_path, params),
                                          {},
                                          headers,
                                          )
        return make_request(self.session,
                            uri,
                            'GET',
                            headers=headers,
                            timeout=self.timeout,
                            )

    def _post(self, request_path, headers=None, body={}):
        r"""General POST request
        Arguments:
        --
        request_path (string): Endpoint e.g. /ping. Includes URI params
        body (Dict[string, any]): Dictionary of body parameters
        """
        uri = f'{self.host}{request_path}'
        if headers is None:
            headers = {}
        headers = self.signer.add_headers('POST',
                                          request_path, 
                                          body,
                                          headers,
                                          )
        return make_request(self.session,
                            uri,
                            'POST',
                            headers,
                            body,
                            timeout=self.timeout,
                            )

    def get_order_by_id(self, underlying, id):
        r"""Endpoint to get order by id.
        Arguments:
        --
        underlying: see `constants.VALID_UNDERLYING`
        id: String identifier
        """
        assert underlying in constants.VALID_UNDERLYING
        uri = f'/user/order/{underlying}/{id}'
        return self._get(uri)

    def get_orders(self, underlying):
        r"""Endpoint to get unmatched (open) orders owned by caller.
        Does not return any matched or expired orders.
        Arguments:
        --
        underlying: see `constants.VALID_UNDERLYING`
        """
        assert underlying in constants.VALID_UNDERLYING
        uri = f'/user/orders/{underlying}'
        return self._get(uri)

    def get_positions(self, underlying):
        r"""Endpoint to get positions owned by caller.
        Does not return any open (unmatched) orders.
        Arguments:
        --
        underlying: see `constants.VALID_UNDERLYING`
        """
        assert underlying in constants.VALID_UNDERLYING
        uri = f'/user/positions/{underlying}'
        return self._get(uri)

    def get_open_interest(self,
                          underlying,
                          strike,
                          order_type,
                          order_side,
                          ):
        r"""Endpoint to get open interest of caller's margin account.
        Arguments:
        --
        underlying: see `constants.VALID_UNDERLYING`
        strike: see `constants.VALID_STRIKE`
        order_type: see `constants.VALID_ORDER_TYPE`
        order_side: see `constants.VALID_ORDER_SIDE`
        """
        assert underlying in constants.VALID_UNDERLYING
        assert strike in constants.VALID_STRIKE
        assert order_type in constants.VALID_ORDER_TYPE
        assert order_side in constants.VALID_ORDER_SIDE
        uri = f'/user/openinterest/{underlying}'
        params = {
            'strike': strike,
            'isCall': order_type,
            'isBuy': order_side,
        }
        return self._get(uri, params=params)

    def get_available_balance(self, underlying):
        r"""Endpoint to get available balance in caller's margin account.
        Arguments:
        --
        underlying: see `constants.VALID_UNDERLYING`
        """
        assert underlying in constants.VALID_UNDERLYING
        uri = f'/user/availbalance/{underlying}'
        return self._get(uri)

    def get_account_info(self, underlying):
        r"""Endpoint to get information on caller's margin account.
        Arguments:
        --
        underlying: see `constants.VALID_UNDERLYING`
        """
        assert underlying in constants.VALID_UNDERLYING
        uri = f'/user/accountinfo/{underlying}'
        return self._get(uri)

    def create_market_order(self,
                            underlying,
                            strike,
                            quantity,
                            order_type,
                            order_side,
                            ):
        r"""Endpoint to create a new market order.
        Arguments:
        --
        underlying: see `constants.VALID_UNDERLYING`
        quantity (integer): Number of units in order. Rounded to nearest 0.01.
        strike: see `constants.VALID_STRIKE`
        order_type: see `constants.VALID_ORDER_TYPE`
        order_side: see `constants.VALID_ORDER_SIDE`
        """
        assert underlying in constants.VALID_UNDERLYING
        assert strike in constants.VALID_STRIKE
        assert order_type in constants.VALID_ORDER_TYPE
        assert order_side in constants.VALID_ORDER_SIDE
        quantity = round(quantity, 2)
        assert quantity > 0
        uri = f'/user/create/market/{underlying}'
        body = {
            'strike': strike,
            'quantity': quantity,
            'isCall': order_type,
            'isBuy': order_side,
        }
        return self._post(uri, body=body)

    def create_limit_order(self,
                           underlying,
                           strike,
                           quantity,
                           price,
                           order_type,
                           order_side,
                           ):
        r"""Endpoint to create a new limit order.
        Arguments:
        --
        underlying: see `constants.VALID_UNDERLYING`
        quantity (float): Number of units in order. Rounded to nearest 0.01.
        price (float): Price for the limit order. Rounded to nearest 0.01.
        strike: see `constants.VALID_STRIKE`
        order_type: see `constants.VALID_ORDER_TYPE`
        order_side: see `constants.VALID_ORDER_SIDE`
        """
        assert underlying in constants.VALID_UNDERLYING
        assert strike in constants.VALID_STRIKE
        assert order_type in constants.VALID_ORDER_TYPE
        assert order_side in constants.VALID_ORDER_SIDE
        quantity = round(quantity, 2)
        assert quantity > 0
        price = round(price, 2)
        assert price > 0
        uri = f'/user/create/limit/{underlying}'
        body = {
            'strike': strike,
            'quantity': quantity,
            'price': price,
            'isCall': order_type,
            'isBuy': order_side,
        }
        return self._post(uri, body=body)

    def cancel_order_by_id(self, underlying, id):
        r"""Endpoint to cancel an existing order.
        Arguments:
        --
        underlying: see `constants.VALID_UNDERLYING`
        id: String identifier
        """
        assert underlying in constants.VALID_UNDERLYING
        uri = f'/user/cancel/{underlying}/{id}'
        return self._post(uri)

    def cancel_batch(self, underlying, ids):
        r"""Endpoint to cancel a batch of orders
        Arguments:
        --
        underlying: see `constants.VALID_UNDERLYING`
        ids: String identifiers
        """
        assert underlying in constants.VALID_UNDERLYING
        uri = f'/user/cancel/batch/{underlying}'
        body = {'ids': ids}
        return self._post(uri, body=body)

    def cancel_all(self, underlying):
        r"""Endpoint to cancel all open orders
        Arguments:
        --
        underlying: see `constants.VALID_UNDERLYING`
        """
        assert underlying in constants.VALID_UNDERLYING
        uri = f'/user/cancel/all/{underlying}'
        return self._post(uri)
