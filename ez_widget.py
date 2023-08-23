import tkinter as tk
import ez_res
import threading
import time

def on_drag(event):
    x = widget_root.winfo_x() + event.x - widget_root._drag_data["x"]
    y = widget_root.winfo_y() + event.y - widget_root._drag_data["y"]
    widget_root.geometry(f'+{x}+{y}')

def on_drag_start(event):
    widget_root._drag_data = {"x": event.x, "y": event.y}

def update_values():
    while True:
        formatted_data = ez_res.format_market_data(symbol)
        if formatted_data:
            last_price_color = "#00C186" if formatted_data['lastPriceUpDown'] == "up" else "#FF5761"
            labels['symbol'].config(text=formatted_data['symbol'])
            labels['lastPrice'].config(text=formatted_data['lastPrice'], fg=last_price_color)
            labels['changePercent'].config(text=formatted_data['changePercent'])
            labels['bestBid'].config(text=formatted_data['bestBid'])
            labels['bestAsk'].config(text=formatted_data['bestAsk'])
            labels['volume'].config(text=formatted_data['volume'])
            labels['highPrice'].config(text=formatted_data['highPrice'])
            labels['lowPrice'].config(text=formatted_data['lowPrice'])
            labels['updatedAt'].config(text=formatted_data['updatedAt'])
        print("wait...")
        time.sleep(5)  # Wait for 1 minute


def create_widget(x, y, symbol):
    global widget_root
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
    # Get formatted market data
    formatted_data = ez_res.format_market_data(symbol)

    if formatted_data:
        border_color = "#0c0c0c"
        last_price_color = "#00C186" if formatted_data['lastPriceUpDown'] == "up" else "#FF5761"
        for row, col, text, colspan in [
            (0, 0, formatted_data['symbol'], 2),
            (0, 2, formatted_data['lastPriceUpDown'], 1),
            (0, 3, formatted_data['lastPrice'], 3),
            (0, 6, formatted_data['changePercent'], 2),

            (1, 0, formatted_data['bestBid'], 2),
            (1, 2, formatted_data['bestAsk'], 2),
            (1, 4, formatted_data['volume'], 4),

            (2, 0, formatted_data['highPrice'], 2),
            (2, 2, formatted_data['lowPrice'], 2),
            (2, 4, formatted_data['updatedAt'], 4),
        ]:
            label = tk.Label(widget_root, text=text, borderwidth=1, relief="solid")
            label.grid(row=row, column=col, columnspan=colspan, sticky="nsew")
            label.config(highlightthickness=1, highlightbackground=border_color)
            if col == 3:  # If this is the lastPrice label
                label.config(fg=last_price_color)  # Set the text color based on lastPriceUpDown

    # Create a thread to update the values
    update_thread = threading.Thread(target=update_values)
    update_thread.daemon = True  # Daemon thread will exit when the main program exits
    update_thread.start()

    return widget_root

symbol = "PAPRY_USDT"
