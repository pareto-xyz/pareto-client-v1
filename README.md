# Pareto Python Client v1

Python client for Pareto v1 API. The library requires Python 3. 

## Installation

The `pareto-client-v1` package is available on PyPI. Install with `pip`:
```
pip install pareto-client-v1
```

## Getting Started

We recommend reading our [documentation](gitbook link) for an overview. This repository implements a client with different levels of authentication, modeled after the [dydx client](https://github.com/dydxprotocol/dydx-v3-python). 

### Public endpoints

No authentication information is required to access public endpoints. 

```
from pareto import Client

# 
# Access public API endpoints
# 
client = Client(host='http://localhost:8080')
client.public.ping()
```

### Private endpoints

We require the user to provide their ETH private key, which the client uses to generate signatures for actions in the Pareto API that require authentication. The private key is not stored and is not send to the backend in any HTTP requests (only signatures are sent as header messages). 

```
from pareto import Client
from pareto import UNDERLYING_ETH

# 
# Access private API endpoints
#
client = Client(host='http://localhost:8080',
                eth_private_key='0x...',
                )
orders = client.private.get_orders(underlying=UNDERLYING_ETH)
client.private.create_order(...)
```
