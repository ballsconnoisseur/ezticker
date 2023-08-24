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

def minimize_gui():
    root.iconify()

# Function to toggle widget drag
def toggle_drag():
    widget_window.enable_drag = var_drag.get() == 1
    save_config() # Save the new setting to the config file

# Function to toggle "always on top" setting
def toggle_always_on_top():
    if widget:
        widget_window.toggle_always_on_top() # Call the function in the widget_window module
    save_config() # Save the new setting to the config file

# Function to read available symbols from a file
def read_available_symbols(filename='ez_symbol_list.txt'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Function to save symbols to config.json
def save_symbols_to_config(symbols):
    config_data = {"symbols": symbols, "interval": 7}
    with open('config.json', 'w') as file:
        json.dump(config_data, file)

# Function to read symbols from config.json
def read_symbols_from_config():
    with open('config.json', 'r') as file:
        return json.load(file)['symbols']

# Function to open symbol configuration window
def config_symbols():
    global config_window
    if config_window:
        config_window.lift()  # Bring the existing window to the front
        return

    config_window = tk.Toplevel(root)
    config_window.title("Config Symbols")
    config_window.protocol("WM_DELETE_WINDOW", close_config_window) # Close instead of destroy

    available_symbols = read_available_symbols()
    current_symbols = read_symbols_from_config()

    symbol_vars = []
    for i in range(9):
        var_symbol = tk.StringVar(config_window)
        var_symbol.set(current_symbols[i])  # Set the default value

        # Create a Combobox and set its values and height
        combobox = ttk.Combobox(config_window, textvariable=var_symbol, values=available_symbols, height=11)
        combobox.grid(row=i, column=0)

        entry_field = tk.Entry(config_window, textvariable=var_symbol)
        entry_field.grid(row=i, column=1)
        symbol_vars.append(var_symbol)

    def save_config_symbols():
        global config_window  # Add this line
        selected_symbols = [var.get() for var in symbol_vars]
        save_symbols_to_config(selected_symbols)
        close_widget()
        show_widget()   # Show the widget again with the new configuration
        print("Preset saved")

    button_save_config_symbols = tk.Button(config_window, text="Save", command=save_config_symbols)
    button_save_config_symbols.grid(row=9, column=0, columnspan=2)

def close_config_window():
    global config_window
    if config_window:  # Check if config_window is not False
        config_window.destroy()
        config_window = False

def save_config():
    config['Position']['x'] = str(widget_window.widget_root.winfo_x())
    config['Position']['y'] = str(widget_window.widget_root.winfo_y())
    config['Settings']['enable_drag'] = str(var_drag.get())
    config['Settings']['always_on_top'] = str(var_always_on_top.get())
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def show_widget():
    global widget
    if widget:
        close_widget()
        print("Was Open")
    else:
        # If the widget is not open, create and show it
        x, y = config.get('Position', 'x'), config.get('Position', 'y')
        widget = widget_window.create_widget(x, y)
        widget.mainloop()
        print("Opened")

        #start_update()
        #print("Updating begin")
        
def close_widget():
    global widget
    if widget:
        stop_update()
        print("TH Killed")
        widget.destroy()
        widget = None
        print("Closed")


def start_update():
    global updating
    global widget
    if widget:
        # Start the update thread
        ez_update.start_update_thread()
        updating = True
        print("Updating Active")
    print("No widget opened")

def stop_update():
    global updating
    # Stop the update thread when needed
    ez_update.stop_update_thread()
    updating = False
    print("Updating Stoped")

def exit_gui():
    global config_window
    if config_window:
        close_config_window()
    
    close_widget()
    root.destroy()

def reset_position():
    screen_width = root.winfo_screenwidth()
    widget_width = int(screen_width * 0.18)

    # Set position to top-right corner
    x = screen_width - widget_width
    y = 0

    config.set('Position', 'x', str(x))
    config.set('Position', 'y', str(y))
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    show_widget()

config = configparser.ConfigParser()
config.read('config.ini')
if 'Position' not in config:
    config['Position'] = {'x': '0', 'y': '0'}
if 'Settings' not in config:
    config['Settings'] = {'enable_drag': '0', 'always_on_top': '0'}

# Read the settings
enable_drag = int(config['Settings']['enable_drag'])
always_on_top = int(config['Settings']['always_on_top'])


# Gui elements
root = tk.Tk()
root.title("EZ Ticker")
root.protocol("WM_DELETE_WINDOW", minimize_gui) # Minimize instead of close

# Enable Drag checkbox
var_drag = tk.IntVar()
var_drag.set(enable_drag)
check_drag = tk.Checkbutton(root, text="Enable Drag", variable=var_drag, command=toggle_drag)
check_drag.pack()

# Always on Top checkbox
var_always_on_top = tk.IntVar()
var_always_on_top.set(always_on_top)
check_always_on_top = tk.Checkbutton(root, text="Always on Top", variable=var_always_on_top, command=toggle_always_on_top)
check_always_on_top.pack()

# Config Symbols button
button_config_symbols = tk.Button(root, text="Config Symbols", command=config_symbols)
button_config_symbols.pack()

# Buttons
button_show = tk.Button(root, text="Show Widget", command=show_widget)
button_show.pack()
button_show = tk.Button(root, text="Run Update", command=start_update)
button_show.pack()
button_save = tk.Button(root, text="Save Position", command=save_config)
button_save.pack()
reset_button = tk.Button(root, text="Reset Position", command=reset_position)
reset_button.pack()
button_exit = tk.Button(root, text="Exit", command=exit_gui)
button_exit.pack()
root.mainloop()

