
`ez_ticker` is easy to use, simple and light tool for traders, investors, or financial enthusiasts who want to monitor specific market symbols.

### Purpose:

ez_ticker app designed to display real-time market data for various financial symbols.

It provides a customizable and interactive interface to track real-time market trends without having to constantly check various websites or platforms.

Here's a brief description of its functionality and components!

RUN BY: `ez_base.py`

### Functionality:

- **Real-Time Market Data Tracking:**
        Displays real-time data for various financial symbols, updating at a specified interval.

- **Symbol Configuration:**
        Allows the user to configure up to 9 symbols from a list of available symbols.

- **Threading for Data Updating:**
        Uses a separate thread to update the market data, ensuring that the user interface remains responsive.
  
- **Draggable Widget:**
        The widget can be dragged around the screen, and this functionality can be toggled on or off.

- **Always-On-Top Option:**
        The widget can be set to always appear on top of other windows or to be under all windows.

- **Position Saving and Resetting:**
        The widget's position can be saved and reset to the top-right corner of the screen.

- **Error Handling:**
        Includes error handling for various scenarios.


### Components:

1. **Main GUI (`ez_base.py`):**
          This file serves as the main control panel for the application.
          It allows the user to configure various settings.
   
3. **Widget Display (`ez_widget.py`):**
         Responsible for creating and displaying widget.

4. **Data Fetching and Updating (`ez_update.py`):**
         Contains functions to fetch and update market data using threading.

6. **Data Formatting (`ez_res.py`):**
         Responsible for formatting the fetched market data.

8. **Configuration Management:**
         The application uses two configuration files (`config.ini`) and a JSON file (`config.json`) to manage various settings and symbols.


### Interaction Between Components:

- **`ez_base.py`:**
                  !        !        !        YOU RUN THIS FILE        !        !        !
                  Is main control panel displayed as simple `(GUI)`, interacting with `ez_widget.py` to display the widget and with `ez_update.py` to start and stop the update thread.
                  It also handles configuration management.

- **`ez_widget.py`:**
                    Responsible for the visual representation of the widget, including the ability to drag and set it to always be on top.

- **`ez_update.py`:**
                    Manages the fetching and updating of market data, working in conjunction with `ez_res.py`.

- **`ez_res.py`:**
                    Likely formats the raw market data for display in the widget.

- **`ez_api.py`:**
                    Requests raw market data for `ez_res.py` to work with.

### Debug console prints: 
B- `ez_base.py`
W- `ez_widget.py`
U- `ez_update.py`
R- `ez_res.py`
A- `ez_api.py`

Wish you Happy using, and big incomes!

Any questions DM.
