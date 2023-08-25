import tkinter as tk
import json

enable_drag = False
always_on_top = True


def create_widget(x, y):
    global widget_root, always_on_top

    widget_root = tk.Tk()
    widget_root.overrideredirect(True) # Remove title bar

    # Set the widget to always be on top if the always_on_top variable is True
    if always_on_top:
        widget_root.wm_attributes("-topmost", 1)
    
    # Set a transparent color
    transparent_color = "white" # You can choose any color that doesn't conflict with other colors in your widget

    # Set the transparent color for the main window
    widget_root.configure(bg=transparent_color)
    widget_root.wm_attributes('-transparentcolor', transparent_color)

    # Get screen width and height
    screen_width = widget_root.winfo_screenwidth()
    screen_height = widget_root.winfo_screenheight()

    # Calculate widget width and height
    widget_width = int(screen_width * 0.21)
    widget_height = int(screen_height * 0.125)

    # Set default position to top-right corner if x and y are not provided
    if x is None or y is None:
        x = screen_width - widget_width
        y = 0

    widget_root.geometry(f'{widget_width}x{widget_height}+{x}+{y}')


    widget_root.bind("<ButtonPress-1>", on_drag_start)
    widget_root.bind("<B1-Motion>", on_drag)

    # Set weight for rows and columns
    for i in range(3):
        widget_root.grid_rowconfigure(i, weight=1)
    for i in range(5):
        widget_root.grid_columnconfigure(i, weight=1)

    load_config()  # Load the configuration
    print("W- Config Loaded by create_widget")
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
    
    # Initialize labels with placeholder values, and using this genius function give them visual values
    for key, row, col, colspan, rowspan, width, height, font_size, anchor, border_width, sticky_val, text in [
            ('titleText', 0, 0, 3, 1, 10, 1, 2, "w", 0, "nsew", "ez_ticker"), # Text
            ('symbol', 0, 3, 9, 3, 10, 1, 10, "s", 0, "nsew", "AAA/BBB"),
            ('bidText', 0, 11, 3, 1, 6, 1, 6, "center", 1, "nsew", "BID"), # Text
            ('hiText', 0, 14, 3, 1, 6, 1, 6, "center", 1, "nsew", "HI"), # Text
            ('bestBid', 1, 11, 3, 2, 8, 1, 2, "w", 1, "nsew", "-----"),
            ('highPrice', 1, 14, 3, 2, 8, 1, 2, "w", 1, "nsew", "-----"),

            ('lastPrice', 3, 0, 7, 4, 20, 2, 20, "e", 0, "nsew", "-----"),
            ('changePercent', 3, 7, 4, 2, 4, 1, 12, "center", 1, "nsew", "%"),
            ('bidtoaskPercent', 3, 11, 3, 2, 6, 1, 12, "center", 1, "nsew", "%"), # Text for now
            ('hitoloPercent', 3, 14, 3, 2, 6, 1, 12, "center", 1, "nsew", "%"), # Text for now

            ('lastPriceUpDown', 5, 7, 4, 2, 4, 1, 12, "center", 1, "nsew", "-"), # Arrow
            ('bestAsk', 5, 11, 3, 2, 8, 1, 2, "w", 1, "nsew", "-----"),
            ('lowPrice', 5, 14, 3, 2, 8, 1, 2, "w", 1, "nsew", "-----"),

            ('volume', 7, 0, 7, 1, 20, 1, 8, "e", 0, "nsew", "----- VOL"),
            ('updatedAt', 7, 7, 4, 1, 8, 1, 8, "center", 1, "nsew", "--- ---"),
            ('askText', 7, 11, 3, 1, 6, 1, 6, "center", 1, "nsew", "ASK"), # Text
            ('loText', 7, 14, 3, 1, 6, 1, 6, "center", 1, "nsew", "LO"), # Text
        ]:
        label = tk.Label(widget_root, text=text, height=height, borderwidth=border_width, relief="solid", width=width, fg="#fdf4dc", font=("fixedsys", font_size), bg=transparent_color, anchor=anchor)
        label.grid(row=row, column=col, columnspan=colspan, rowspan=rowspan, sticky=sticky_val)
        label.configure(bg=label.cget("bg"))  # Set the background color to itself to apply opacity
        labels[key] = label  # Store the label in the labels dictionary

    print("W- Widget made!")
    return widget_root


def update_widget(formatted_data):
    last_price_color = "#00C186" if formatted_data['lastPriceUpDown'] == "up" else "#FF5761"
    labels['symbol'].config(text=formatted_data['symbol'])
    last_price_up_down_symbol = "↗" if formatted_data['lastPriceUpDown'] == "up" else "↘"
    labels['lastPriceUpDown'].config(text=last_price_up_down_symbol, fg=last_price_color)
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

# Function to load the configuration
def load_config():
    global always_on_top
    with open('config.json', 'r') as file:
        config = json.load(file)
    always_on_top = config.get('always_on_top', False) # Read the always_on_top setting

def toggle_always_on_top():
    global always_on_top
    always_on_top = not always_on_top
    widget_root.wm_attributes("-topmost", always_on_top) # Update the widget's topmost attribute

    # Update the config file
    with open('config.json', 'r') as file:
        config = json.load(file)
    config['always_on_top'] = always_on_top
    with open('config.json', 'w') as file:
        json.dump(config, file)


def on_drag(event):
    if enable_drag:
        x = widget_root.winfo_x() + event.x - widget_root._drag_data["x"]
        y = widget_root.winfo_y() + event.y - widget_root._drag_data["y"]
        widget_root.geometry(f'+{x}+{y}')

def on_drag_start(event):
    widget_root._drag_data = {"x": event.x, "y": event.y}



    