import tkinter as tk
import threading
import time
import ez_update
import json

update_thread = None
update_running = False
enable_drag = False

# Function to load the configuration
def load_config():
    global symbols, interval
    with open('config.json', 'r') as file:
        config = json.load(file)
    symbols = config['symbols']
    interval = config['interval']


def on_drag(event):
    if enable_drag:
        x = widget_root.winfo_x() + event.x - widget_root._drag_data["x"]
        y = widget_root.winfo_y() + event.y - widget_root._drag_data["y"]
        widget_root.geometry(f'+{x}+{y}')

def on_drag_start(event):
    widget_root._drag_data = {"x": event.x, "y": event.y}

def update_values():
    global update_running
    print("update_values started")
    symbol_index = 0
    while update_running:  # Check the update_running variable
        load_config()  # Load the configuration
        try:
            symbol = symbols[symbol_index]  # Get the current symbol
            formatted_data = ez_update.fetch_data(symbol)  # Fetch data from the separate module
            print("Formatted data:", formatted_data)

            if formatted_data:
                last_price_color = "#00C186" if formatted_data['lastPriceUpDown'] == "up" else "#FF5761"
                labels['symbol'].config(text=formatted_data['symbol'])
                labels['lastPrice'].config(text=formatted_data['lastPrice'], fg=last_price_color)

                change_percent = formatted_data['changePercent']
                if change_percent.startswith("+"):
                    change_percent_color = "#00C186"  # Green
                elif change_percent.startswith("-"):
                    change_percent_color = "#FF5761"  # Red
                else:
                    change_percent_color = "#0000FF"  # Blue
                labels['changePercent'].config(text=change_percent, fg=change_percent_color)
                labels['bestBid'].config(text=formatted_data['bestBid'])
                labels['bestAsk'].config(text=formatted_data['bestAsk'])
                labels['volume'].config(text=formatted_data['volume'])
                labels['highPrice'].config(text=formatted_data['highPrice'])
                labels['lowPrice'].config(text=formatted_data['lowPrice'])
                labels['updatedAt'].config(text=formatted_data['updatedAt'])
            
            # Increment the symbol index, looping back to the start if necessary
            symbol_index = (symbol_index + 1) % len(symbols)

        except Exception as e:
            print("Exception in update_values:", e)

        print("wait...")
        # Break the sleep into smaller intervals and check update_running
        for _ in range(interval):
            if not update_running:
                break
            time.sleep(1)
            print("wait.")


def create_widget(x, y,):
    global widget_root, update_thread, update_running
    widget_root = tk.Tk()
    widget_root.overrideredirect(True) # Remove title bar

    # Get screen width and height
    screen_width = widget_root.winfo_screenwidth()
    screen_height = widget_root.winfo_screenheight()

    # Calculate widget width and height
    widget_width = int(screen_width * 0.18)
    widget_height = int(screen_height * 0.09)

    # Set default position to top-right corner if x and y are not provided
    if x is None or y is None:
        x = screen_width - widget_width
        y = 0

    widget_root.geometry(f'{widget_width}x{widget_height}+{x}+{y}')
    widget_root.configure(bg='#2c2c2c') # Set background color

    widget_root.bind("<ButtonPress-1>", on_drag_start)
    widget_root.bind("<B1-Motion>", on_drag)

    # Set weight for rows and columns
    for i in range(3):
        widget_root.grid_rowconfigure(i, weight=1)
    for i in range(5):
        widget_root.grid_columnconfigure(i, weight=1)

    load_config()  # Load the configuration

    # Create labels for the data
    global labels
    labels = {
        'symbol': tk.Label(widget_root),
        'lastPriceUpDown': tk.Label(widget_root),
        'lastPrice': tk.Label(widget_root),
        'changePercent': tk.Label(widget_root),
        'bestBid': tk.Label(widget_root),
        'bestAsk': tk.Label(widget_root),
        'volume': tk.Label(widget_root),
        'highPrice': tk.Label(widget_root),
        'lowPrice': tk.Label(widget_root),
        'updatedAt': tk.Label(widget_root),
    }

        # Initialize labels with empty or placeholder values
    for key, row, col, colspan in [
            ('symbol', 0, 0, 2),
            ('lastPriceUpDown', 0, 2, 1),
            ('lastPrice', 0, 3, 3),
            ('changePercent', 0, 6, 2),
            ('bestBid', 1, 0, 2),
            ('bestAsk', 1, 2, 2),
            ('volume', 1, 4, 4),
            ('highPrice', 2, 0, 2),
            ('lowPrice', 2, 2, 2),
            ('updatedAt', 2, 4, 4),
        ]:
            label = tk.Label(widget_root, text="", borderwidth=1, relief="solid")
            label.grid(row=row, column=col, columnspan=colspan, sticky="nsew")
            labels[key] = label  # Store the label in the labels dictionary
            #label.config(highlightthickness=1, highlightbackground=border_color)
            #if col == 3:  # If this is the lastPrice label
            #    label.config(fg=last_price_color)  # Set the text color based on lastPriceUpDown
    print("Widget made")
    # Create and start the update thread
    update_running = True
    update_thread = threading.Thread(target=update_values)
    update_thread.daemon = True
    update_thread.start()
    print("TH running")
    return widget_root



def stop_update_thread():
    global update_thread, update_running
    update_running = False
    if update_thread:
        update_thread.join()
        update_thread = None
        print("th stoping")
    print("idk why is that")