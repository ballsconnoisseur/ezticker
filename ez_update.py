import threading
import time
import ez_res
import json
from ez_widget import update_widget

update_thread = None
update_running = False
exchanges = []
symbols = []
interval = 0

def load_config():
    global exchanges, symbols, interval
    with open('config.json', 'r') as file:
        config = json.load(file)
    exchanges = config['exchanges']
    symbols = config['symbols']
    interval = config['interval']

def fetch_data(exchange, symbol):
    return ez_res.format_market_data(exchange, symbol)


def update_values():
    global update_running
    load_config()
    print("U- Updating Started")
    while update_running:
        for exchange, symbol in zip(exchanges, symbols):
            try:
                # Skip None or empty symbols or exchanges
                if not symbol or not exchange:
                    continue

                formatted_data = fetch_data(exchange, symbol)
                formatted_data['exchange'] = exchange  # Add the exchange name
                print(f"U- Exchange: {exchange}, Symbol: {symbol}")
                print("U- Formatted data: \n", formatted_data)

                if formatted_data:
                    update_widget(formatted_data)  # Call the function to update the widget

            except Exception as e:
                print("U- Exception in update_values:", e)
                continue

            # Sleep for the interval after each fetch
            for i in range(interval):
                if not update_running:
                    print("U- Waiting stoped.")
                    return
                print(f"U- Waiting... {i+1}/{interval} seconds.")
                time.sleep(1)


def start_update_thread():
    global update_thread, update_running
    update_running = True
    update_thread = threading.Thread(target=update_values)
    update_thread.daemon = True
    update_thread.start()
    print("U- TH Started")

def stop_update_thread():
    global update_thread, update_running
    update_running = False
    if update_thread:
        update_thread.join()
        update_thread = None
        print("U- TH Stoped")

        