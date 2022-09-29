# ---- API URLs ----
API_HOST_LOCAL = 'localhost:8080'

# ---- API Defaults ----
DEFAULT_API_TIMEOUT = 3000

# ---- Internal checks ---

ORDER_SIDE_BUY = True
ORDER_SIDE_SELL = False
ORDER_TYPE_CALL = True
ORDER_TYPE_PUT = False
UNDERLYING_ETH = 0

VALID_STRIKE = list(range(11))
VALID_ORDER_SIDE = [ORDER_SIDE_BUY, ORDER_SIDE_SELL]
VALID_ORDER_TYPE = [ORDER_TYPE_CALL, ORDER_TYPE_PUT]
VALID_UNDERLYING = [UNDERLYING_ETH]

# ---- Signature Messages ----
MARKET_ORDER_MESSAGE = "pareto_orderbook_v1_create_market_order"
LIMIT_ORDER_MESSAGE = "pareto_orderbook_v1_create_limit_order"
CANCEL_ORDER_MESSAGE = "pareto_orderbook_v1_cancel_order"
GET_ORDER_BY_ID_MESSAGE = "pareto_orderbook_v1_get_order_by_id"
GET_ORDERS_MESSAGE = "pareto_orderbook_v1_get_orders"
GET_POSITIONS_MESSAGE = "pareto_orderbook_v1_get_positions"
GET_OPEN_INTEREST_MESSAGE = "pareto_orderbook_v1_get_open_interest"
GET_AVAILABLE_BALANCE_MESSAGE = "pareto_orderbook_v1_get_available_balance"
GET_ACCOUNT_INFO_MESSAGE = "pareto_orderbook_v1_get_account_info"
PRUNE_BOOK_MESSAGE = "pareto_orderbook_v1_prune"
PAUSE_BOOK_MESSAGE = "pareto_orderbook_v1_pause"
UNPAUSE_BOOK_MESSAGE = "pareto_orderbook_v1_unpause"
SYNC_BOOK_MESSAGE = "pareto_orderbook_v1_sync"

