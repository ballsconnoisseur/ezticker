import tkinter as tk
from tkinter import ttk
import ez_widget as widget_window
import ez_update
import configparser
import json

# Global variable for the configuration window
config_window = False
widget = None
updating = False


def center_window(window):
    window.update_idletasks()
    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    if window == config_window:
        x_position = (screen_width // 4) - (window_width // 2)
    else:
        x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)

    window.geometry(f'+{x_position}+{y_position}')

# Function to toggle widget drag
def toggle_drag():
    if widget:
        widget_window.enable_drag = var_drag.get() == 1
    else:
        print("B- No widget to toggle 'drag'.")

# Function to toggle "always on top" setting
def toggle_always_on_top():
    if widget:
        widget_window.toggle_always_on_top() # Call the function in the widget_window module
        save_config() # Save the new setting to the config file
    else:
        print("B- No widget to toggle 'on top'.")

def read_symbols_for_exchange(exchange, filename_prefix='ez_pair_list_'):
    filename = f"{filename_prefix}{exchange}.txt"
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]
    


style_one = {'fg': '#FAF9F6', 'bg': '#2c2c2c'}
style_two = {'fg': '#F9F6EE', 'bg': '#2f2f2f'}
style_three = {'fg': '#880808', 'bg': '#1c1c1c'}

# Function to open symbol configuration window
def config_symbols():
    global config_window
    if config_window:
        config_window.lift()
        return

    def update_symbols_options(exchange_var, symbol_combobox):
        exchange = exchange_var.get()
        new_options = read_symbols_for_exchange(exchange)
        symbol_combobox['values'] = new_options

    # Save to config function
    def save_config_symbols():
        new_exchanges = [var.get() for var, _ in exchange_vars if var.get()]
        new_symbols = [var.get() for var, _ in symbol_vars if var.get()]
        new_interval = int(interval_var.get())  # Convert to integer
        config_data = {"exchanges": new_exchanges, "symbols": new_symbols, "interval": new_interval}
        with open('config.json', 'w') as file:
            json.dump(config_data, file)

    # Adding row function
    def add_row():
        exchange_var = tk.StringVar()
        symbol_var = tk.StringVar()
        exchange_vars.append((exchange_var, None))
        symbol_vars.append((symbol_var, None))
        create_row(exchange_var, symbol_var)

    # Remove row function
    def remove_row(row):
        for widget in config_window.grid_slaves():
            if int(widget.grid_info()['row']) == row:
                widget.destroy()
        del exchange_vars[row]
        del symbol_vars[row]

    def create_row(exchange_var, symbol_var):
        row = len(exchange_vars)
        exchange_combobox = ttk.Combobox(config_window, textvariable=exchange_var, values=available_exchanges)
        exchange_combobox.grid(row=row, column=0)
        symbol_combobox = ttk.Combobox(config_window, textvariable=symbol_var)
        symbol_combobox.grid(row=row, column=1)
        ttk.Combobox(config_window, textvariable=exchange_var, values=available_exchanges).grid(row=row, column=0)
        tk.Entry(config_window, textvariable=symbol_var, **style_one).grid(row=row, column=2)
        tk.Button(config_window, text="-", command=lambda row=row: remove_row(row), **style_three).grid(row=row, column=4, columnspan=2)  # Remove button
        exchange_var.trace_add('write', lambda *args: update_symbols_options(exchange_var, symbol_combobox))

    
    config_window = tk.Toplevel(root)
    config_window.title("Config Symbols")
    # Center the window after it has been drawn
    center_window(config_window)
    with open('config.json', 'r') as file:
        config_data = json.load(file)
    interval_value = config_data.get('interval', 7)  # Default to 7 if not found
    available_exchanges = ["xeggex", "binance", "okx", "coinbase"]

    exchange_vars = []
    symbol_vars = []

    config_window.configure(bg="#2a2a2a")
    # Top
    tk.Label(config_window, text="Exchange", **style_two).grid(row=0, column=0, sticky="nsew")
    tk.Label(config_window, text="Pair", **style_two).grid(row=0, column=1, sticky="nsew")
    tk.Label(config_window, text="Custom", **style_two).grid(row=0, column=2, sticky="nsew")

    for exchange, symbol in zip(config_data['exchanges'], config_data['symbols']):
        exchange_var = tk.StringVar(value=exchange)
        symbol_var = tk.StringVar(value=symbol)
        exchange_vars.append((exchange_var, None))
        symbol_vars.append((symbol_var, None))
        create_row(exchange_var, symbol_var)

    interval_var = tk.StringVar(value=str(interval_value))

    # Bottom 
    tk.Label(config_window, text="Interval", **style_two).grid(row=100, column=0, sticky="nsew")
    tk.Entry(config_window, textvariable=interval_var, **style_one).grid(row=100, column=1, sticky="nsew")
    tk.Button(config_window, text="Save", command=save_config_symbols, **style_one).grid(row=100, column=2,columnspan=2)
    tk.Button(config_window, text="+", command=add_row, **style_one).grid(row=100, column=4,columnspan=2)
    

def close_config_window():
    global config_window
    if config_window:  # Check if config_window is not False
        config_window.destroy()
        config_window = False

def save_config():
    config['Position']['x'] = str(widget_window.widget_root.winfo_x())
    config['Position']['y'] = str(widget_window.widget_root.winfo_y())
    config['Settings']['always_on_top'] = str(var_always_on_top.get())
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def show_widget():
    global widget
    if widget:
        print("B- Widget Was Open, Closing widget")
        close_widget()
    else:
        # If the widget is not open, create and show it
        x, y = config.get('Position', 'x'), config.get('Position', 'y')
        widget = widget_window.create_widget(x, y)
        print("B- Widget Opened")
        widget.mainloop()
            

def close_widget():
    global widget
    global updating
    if updating:
        stop_update()
        print("B- Updating Stoped by close_widget")
        if widget:
            widget.destroy()
            widget = None
            print("B- Widget Closed")
    else: 
        widget.destroy()
        widget = None
        print("B- Widget Closed, wasn't updating.")


def start_update():
    global updating
    global widget
    if widget:
        if updating:
            print("B- Updating Was Strarted Earlier, Restarting Updating by start_update")
            stop_update()
            updating = False
            return
        else:
            # Start the update thread
            ez_update.start_update_thread()
            updating = True
            print("B- Updating Started")
    print("B- No widget opened")

def stop_update():
    global updating
    if updating:
        ez_update.stop_update_thread()
        updating = False
        print("B- Updating Stoped")

def exit_gui():
    global widget, config_window
    print("B- Shutting down...")
    if config_window:
        close_config_window()
    if widget:
        close_widget()
    root.destroy()

def reset_position():
    global widget
    print("B- Position reseted.")
    screen_width = root.winfo_screenwidth()
    widget_width = int(screen_width * 0.2)
    # Set position to top-right corner
    x = screen_width - widget_width
    y = 0
    config.set('Position', 'x', str(x))
    config.set('Position', 'y', str(y))
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    if widget:
        close_widget()
        print("B- Widget Closed by Positon Reset")


config = configparser.ConfigParser()
config.read('config.ini')
if 'Position' not in config:
    config['Position'] = {'x': '0', 'y': '0'}
if 'Settings' not in config:
    config['Settings'] = {'always_on_top': '0'}

# Read the settings
always_on_top = int(config['Settings']['always_on_top'])

# Gui elements
root = tk.Tk()
root.title("ez_")
root.protocol("WM_DELETE_WINDOW", exit_gui) # Close all processes instead of only gui process
root.configure(bg="#2a2a2a")
root.iconbitmap('ez_logotype.ico')
# Center the window after it has been drawn
center_window(root)


# Font and background colors presets/styles
style_one = {'fg': '#FAF9F6', 'bg': '#2c2c2c'}
style_two = {'fg': '#F9F6EE', 'bg': '#2f2f2f'}
style_three = {'fg': '#880808', 'bg': '#1c1c1c'}

# New title box
title_label = tk.Label(root, text="EZ Ticker Configuration", **style_two)
title_label.grid(row=0, column=0, columnspan=2, sticky="ew")

# Config Symbols button
button_config_symbols = tk.Button(root, text="Config Symbols", command=config_symbols, **style_one)
button_config_symbols.grid(row=1, column=0, columnspan=2, sticky="ew")

# Show Widget button
button_show = tk.Button(root, text="Show Widget", command=show_widget, **style_one)
button_show.grid(row=2, column=0, sticky="ew")

# Begin Updating button
button_update = tk.Button(root, text="Begin Updating", command=start_update, **style_one)
button_update.grid(row=2, column=1, sticky="ew")

# Save Position button
button_save = tk.Button(root, text="Save Position", command=save_config, **style_one)
button_save.grid(row=3, column=0, sticky="ew")

# Reset Position button
reset_button = tk.Button(root, text="Reset Position", command=reset_position, **style_one)
reset_button.grid(row=3, column=1, sticky="ew")

# Enable Drag checkbox
var_drag = tk.IntVar()
check_drag = tk.Checkbutton(root, text="Enable Drag", variable=var_drag, command=toggle_drag, **style_two)
check_drag.grid(row=4, column=0, sticky="ew")

# Always on Top checkbox
var_always_on_top = tk.IntVar()
var_always_on_top.set(always_on_top)
check_always_on_top = tk.Checkbutton(root, text="Always on Top", variable=var_always_on_top, command=toggle_always_on_top, **style_two)
check_always_on_top.grid(row=4, column=1, sticky="ew")

# Set equal weight for columns to distribute space evenly
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()

