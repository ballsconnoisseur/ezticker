import tkinter as tk
from tkinter import Canvas
import json

always_on_top = True
enable_drag = False

def create_widget(x, y):
    global widget_root, always_on_top
    widget_root = tk.Tk()
    widget_root.overrideredirect(True) # Remove title bar

    # Set the widget to always be on top if the always_on_top variable is True
    if always_on_top:
        widget_root.wm_attributes("-topmost", 1)
    
    # TRANSPARENCY DOESNT WORK FOR LINUX ! ! ! (later will be fixed in version dedicated for linux)
    # Set a transparent color
    transparent_color = "#010101" # You can choose any color that doesn't conflict with other colors in your widget

    # Set the transparent color for the main window
    widget_root.configure(bg=transparent_color)
    widget_root.wm_attributes('-transparentcolor', transparent_color)

    # Get screen width and height
    screen_width = widget_root.winfo_screenwidth()
    screen_height = widget_root.winfo_screenheight()

    # Calculate widget width and height
    widget_width = int(screen_width * 0.3)
    widget_height = int(screen_height * 0.1)

    # Set default position to top-right corner if x and y are not provided
    if x is None or y is None:
        x = screen_width - widget_width
        y = 0
    widget_root.geometry(f'{widget_width}x{widget_height}+{x}+{y}')
    widget_root.bind("<ButtonPress-1>", on_drag_start)
    widget_root.bind("<B1-Motion>", on_drag)

    # Set weight for rows and columns
    for i in range(5):
        widget_root.grid_rowconfigure(i, weight=1)
    for i in range(17):
        widget_root.grid_columnconfigure(i, weight=1)

    load_config()  # Load the configuration
    print("W- Config Loaded by create_widget")
    # Labels for the data
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
#0 Row
            ('titleText', 0, 0, 11, 1, 10, 1, 8, "center", 0, "nsew", "ez_ticker"), # Text
            ('bidText', 0, 11, 3, 1, 6, 1, 12, "e", 1, "nsew", " BID "), # Text
            ('hiText', 0, 14, 3, 1, 6, 1, 12, "e", 1, "nsew", " HI "), # Text
#1 Row
            ('symbol', 1, 3, 8, 1, 10, 0, 12, "center", 0, "nsew", "AAA/BBB"),
            ('bestBid', 1, 11, 3, 1, 8, 1, 12, "w", 1, "nsew", "00000.00"),
            ('highPrice', 1, 14, 3, 1, 8, 1, 12, "w", 1, "nsew", "00000.00"),
#2 Row
            ('lastPrice', 2, 0, 7, 2, 20, 2, 24, "e", 0, "nsew", "00000.00$"),
            ('changePercent', 2, 7, 4, 1, 4, 1, 12, "center", 1, "nsew", "tba % 24h"),
            ('bidtoaskPercent', 2, 11, 3, 1, 6, 1, 12, "center", 1, "nsew", "BID2ASK %"), # Calculated diffrence between bid and ask price
            ('hitoloPercent', 2, 14, 3, 1, 6, 1, 12, "center", 1, "nsew", "HI2LO %"), # Calculated diffrence between high and low price
#3 Row
            ('exchange', 3, 7, 4, 1, 4, 1, 12, "center", 1, "nsew", "EXCHANGE"), # Exchange name
            ('bestAsk', 3, 11, 3, 1, 8, 1, 12, "e", 1, "nsew", "00000.00"),
            ('lowPrice', 3, 14, 3, 1, 8, 1, 12, "e", 1, "nsew", "00000.00"),
#4 Row
            ('volume', 4, 0, 7, 1, 20, 1, 14, "e", 0, "nsew", "00000.00 VOL"),
            ('updatedAt', 4, 7, 4, 1, 8, 1, 12, "center", 1, "nsew", "--:--:--"),
            ('askText', 4, 11, 3, 1, 6, 1, 12, "w", 1, "nsew", " ASK "), # Text
            ('loText', 4, 14, 3, 1, 6, 1, 12, "w", 1, "nsew", " LO "), # Text
        ]:
        color = "#00C186" if key in ['bidText', 'hiText', 'bestBid', 'highPrice'] else "#FF5761" if key in ['bestAsk', 'lowPrice', 'askText', 'loText'] else "#fdf4dc"
        canvas = Canvas(widget_root, height=height, bg=transparent_color)  # height in pixels
        canvas.grid(row=row, column=col, columnspan=colspan, rowspan=rowspan, sticky=sticky_val)
        label = tk.Label(canvas, text=text, borderwidth=border_width, relief="solid", width=width, fg=color, font=("Fixedsys Excelsior 3.01", font_size), bg=transparent_color, anchor=anchor, padx=0, pady=0)
        label.pack(side="top", fill="both", expand=True)
        labels[key] = label  # Store the label in the labels dictionary
    
    print("W- Widget made!")
    return widget_root

#Animated value inserting
def animated_update(label, new_value, color=None):
    def update_step():
        nonlocal steps
        if steps < len(new_value):
            label.config(text=new_value[:steps+1])
            if color:
                label.config(fg=color)
            steps += 1
            label.after(65, update_step)  # 50ms delay between each update
        else:
            label.config(text=new_value)
            if color:
                label.config(fg=color)
    steps = 0
    update_step()

#Function to update and run animation
def update_widget(formatted_data):
    animated_update(labels['symbol'], formatted_data['symbol'])
    animated_update(labels['lastPrice'], formatted_data['lastPrice'])
    labels['exchange'].config(text=formatted_data['exchange'].upper())
    labels['bestBid'].config(text=formatted_data['bestBid'])
    labels['bestAsk'].config(text=formatted_data['bestAsk'])
    animated_update(labels['volume'], formatted_data['volume'])
    labels['highPrice'].config(text=formatted_data['highPrice'])
    labels['lowPrice'].config(text=formatted_data['lowPrice'])
    labels['updatedAt'].config(text=formatted_data['updatedAt'])
    bestBid = float(formatted_data['bestBid'])
    bestAsk = float(formatted_data['bestAsk'])
    if bestBid and bestAsk:
        percent_diff = ((bestAsk - bestBid) / bestBid) * 100
        labels['bidtoaskPercent'].config(text=f"{percent_diff:.3f}%")
    highPrice = float(formatted_data['highPrice'])
    lowPrice = float(formatted_data['lowPrice'])
    
    if highPrice and lowPrice:
        percent_diff_hi_lo = ((highPrice - lowPrice) / lowPrice) * 100
        labels['hitoloPercent'].config(text=f"{percent_diff_hi_lo:.2f}%")

# Function to load the configuration
def load_config():
    global always_on_top
    with open('config.json', 'r') as file:
        config = json.load(file)
    always_on_top = config.get('always_on_top', True) # Read the always_on_top setting

#Always on top live saving to config and reading
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

#Drag event deffinitions
def on_drag(event):
    if enable_drag:
        x = widget_root.winfo_x() + event.x - widget_root._drag_data["x"]
        y = widget_root.winfo_y() + event.y - widget_root._drag_data["y"]
        widget_root.geometry(f'+{x}+{y}')

def on_drag_start(event):
    widget_root._drag_data = {"x": event.x, "y": event.y}
