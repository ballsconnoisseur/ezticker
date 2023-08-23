import tkinter as tk
import ez_widget as widget_window
import configparser

symbol = "PAPRY_USDT"

def minimize_gui():
    root.iconify()

def toggle_drag():
    widget_window.enable_drag = var_drag.get() == 1

def save_config():
    config['Position']['x'] = str(widget_window.widget_root.winfo_x())
    config['Position']['y'] = str(widget_window.widget_root.winfo_y())
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def show_widget():
    global widget
    if widget:
        widget.destroy()
    x, y = config.get('Position', 'x'), config.get('Position', 'y')
    widget = widget_window.create_widget(x, y, symbol)
    widget.mainloop()

def close_widget():
    global widget
    if widget:
        widget.destroy()
        widget = None

def exit_gui():
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

# Gui elements
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", minimize_gui) # Minimize instead of close
var_drag = tk.IntVar()
check_drag = tk.Checkbutton(root, text="Enable Drag", variable=var_drag, command=toggle_drag)
check_drag.pack()
button_show = tk.Button(root, text="Show Widget", command=show_widget)
button_show.pack()
button_close = tk.Button(root, text="Close Widget", command=close_widget)
button_close.pack()
button_save = tk.Button(root, text="Save Position", command=save_config)
button_save.pack()
reset_button = tk.Button(root, text="Reset Position", command=reset_position)
reset_button.pack()
button_exit = tk.Button(root, text="Exit", command=exit_gui)
button_exit.pack()

widget = None
root.mainloop()
