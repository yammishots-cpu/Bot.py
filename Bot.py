import MetaTrader5 as mt5
import time
import threading

ACCOUNT = int(os.getenv("MT5_LOGIN"))
PASSWORD = os.getenv("MT5_PASSWORD")
SERVER = os.getenv("MT5_SERVER")

SYMBOL = "XAUUSD"
LOT = 0.01
TIMEFRAME = mt5.TIMEFRAME_M5
MAGIC = 999991

running = False

def connect():
    mt5.initialize()
    authorized = mt5.login(ACCOUNT, PASSWORD, SERVER)
    print("MT5 Authorized:", authorized)

def get_candles():
    return mt5.copy_rates_from_pos(SYMBOL, TIMEFRAME, 0, 20)

def scalper_signal(c):
    last = c[-1]
    prev = c[-2]

    if last['close'] > last['open'] and last['close'] > prev['close']:
        return "BUY"

    if last['close'] < last['open'] and last['close'] < prev['close']:
        return "SELL"

    return None

def open_positions(type):
    pos = mt5.positions_get(symbol=SYMBOL)
    if pos:
        for p in pos:
            if p.type == type:
                return True
    return False

def send_order(order_type):
    price = mt5.symbol_info_tick(SYMBOL).ask if order_type == "BUY" else mt5.symbol_info_tick(SYMBOL).bid
    type_mt5 = mt5.ORDER_TYPE_BUY if order_type == "BUY" else mt5.ORDER_TYPE_SELL

    mt5.order_send({
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": LOT,
        "type": type_mt5,
        "magic": MAGIC,
        "price": price,
        "deviation": 50,
        "comment": "CloudBot"
    })

def run_bot():
    connect()
    global running
    running = True
    print("Bot Started")

    while running:
        candles = get_candles()
        signal = scalper_signal(candles)

        if signal == "BUY" and not open_positions(0):
            send_order("BUY")

        if signal == "SELL" and not open_positions(1):
            send_order("SELL")

        time.sleep(10)

def stop_bot():
    global running
    running = False
    print("Bot Stopped")
