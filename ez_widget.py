import tkinter as tk
import json

enable_drag = False
always_on_top = False
labels = {}
def create_widget(x, y):
    global widget_root, always_on_top

    widget_root = tk.Tk()
    widget_root.overrideredirect(True) # Remove title bar

    # Set the widget to always be on top if the always_on_top variable is True
    if always_on_top:
        widget_root.wm_attributes("-topmost", 1)
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
    def update_widget(formatted_data):
                last_price_color = "#00C186" if formatted_data['lastPriceUpDown'] == "up" else "#FF5761"
                labels['symbol'].config(text=formatted_data['symbol'])
                labels['lastPriceUpDown'].config(text=formatted_data['lastPriceUpDown'])
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
    

    # Initialize labels with empty or placeholder values
    for key, row, col, colspan, width in [
            ('symbol', 0, 0, 2, 10),
            ('lastPriceUpDown', 0, 2, 1, 5),
            ('lastPrice', 0, 3, 3, 10),
            ('changePercent', 0, 6, 2, 10),
            ('bestBid', 1, 0, 2, 10),
            ('bestAsk', 1, 2, 2, 10),
            ('volume', 1, 4, 4, 10),
            ('highPrice', 2, 0, 2, 10),
            ('lowPrice', 2, 2, 2, 10),
            ('updatedAt', 2, 4, 4, 15),
        ]:
            label = tk.Label(widget_root, text="", borderwidth=1, relief="solid", width=width)
            label.grid(row=row, column=col, columnspan=colspan, sticky="nsew")
            labels[key] = label  # Store the label in the labels dictionary


    print("Widget made")
    return widget_root


def update_widget(formatted_data):
                last_price_color = "#00C186" if formatted_data['lastPriceUpDown'] == "up" else "#FF5761"
                labels['symbol'].config(text=formatted_data['symbol'])
                labels['lastPriceUpDown'].config(text=formatted_data['lastPriceUpDown'])
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



    