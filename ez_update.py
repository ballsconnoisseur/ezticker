import threading
import time
import ez_res
import json
from ez_widget import update_widget

update_thread = None
update_running = False
symbols = []
interval = 0

def load_config():
    global symbols, interval
    with open('config.json', 'r') as file:
        config = json.load(file)
    symbols = config['symbols']
    interval = config['interval']

def fetch_data(symbol):
    return ez_res.format_market_data(symbol)


def update_values():
    global update_running
    load_config()
    print("U- Updating Started")
    symbol_index = 0
    while update_running:
        try:
            symbol = symbols[symbol_index]

            # Skip None or empty symbols
            if symbol is None or not symbol:
                print(f"U- Skipping empty symbol at index {symbol_index}")
                symbol_index = (symbol_index + 1) % len(symbols)
                continue

            formatted_data = fetch_data(symbol)
            print("U- Symbol: ",symbol)
            print("U- Formatted data: \n", formatted_data)

            if formatted_data:
                update_widget(formatted_data)  # Call the function to update the widget

            symbol_index = (symbol_index + 1) % len(symbols)

        except Exception as e:
            print("U- Exception in update_values:", e)
        print("U- wait...")
        # Break the sleep into smaller intervals and check update_running
        for _ in range(interval):
            if not update_running:
                break
            time.sleep(1)
            print("U- wait.")

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