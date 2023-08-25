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
quiting = False

def minimize_gui():
    root.iconify()

def center_window():
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)

    root.geometry(f'+{x_position}+{y_position}')

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
    global config_window, widget
    print("B- Config Window Opened!")
    if config_window:
        config_window.lift()  # Bring the existing window to the front
        print("B- Config Window Was Open, lifting from background")
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
        print("B- Preset saved")
        if widget:
            close_widget()
        show_widget()   # Show the widget again with the new configuration
        

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
    global quiting, widget
    if quiting:
        print("B- Quiting... can't open widget now")
        close_widget()
    else: 
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
    # Stop the update thread when needed
    ez_update.stop_update_thread()
    updating = False
    print("B- Updating Stoped")

def exit_gui():
    global quiting, widget, updating, config_window
    print("B- Shutting down...")
    quiting = True
    if config_window:
        close_config_window()
    if updating:
        stop_update()
    if widget:
        close_widget()
    root.destroy()

def reset_position():
    global widget
    print("B- Position reseted.")
    screen_width = root.winfo_screenwidth()
    widget_width = int(screen_width * 0.21)

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
    show_widget()
    print("B- Widget Reopened by Positon Reset")

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
root.title("ez_")
root.protocol("WM_DELETE_WINDOW", minimize_gui) # Minimize instead of close
root.configure(bg="#2a2a2a")

# Center the window after it has been drawn
root.after(1, center_window)


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
var_drag.set(enable_drag)
check_drag = tk.Checkbutton(root, text="Enable Drag", variable=var_drag, command=toggle_drag, **style_two)
check_drag.grid(row=4, column=0, sticky="ew")

# Always on Top checkbox
var_always_on_top = tk.IntVar()
var_always_on_top.set(always_on_top)
check_always_on_top = tk.Checkbutton(root, text="Always on Top", variable=var_always_on_top, command=toggle_always_on_top, **style_two)
check_always_on_top.grid(row=4, column=1, sticky="ew")

# Exit button
button_exit = tk.Button(root, text="E X I T", command=exit_gui, **style_three)
button_exit.grid(row=5, column=0, columnspan=2, sticky="ew")

# Set equal weight for columns to distribute space evenly
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()

