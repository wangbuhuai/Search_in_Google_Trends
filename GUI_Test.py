# Created by Dayu Wang (dwang@stchas.edu) on 2022-03-01

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-03-01


import tkinter as tk
from ctypes import windll
from tkinter import ttk


def app_name(container):
    """ Creates the application name on the window.
        :param container: window to show the application name
        :type container: tk.Tk
        :return: a tkinter label of the application name
        :rtype: ttk.Label
    """
    label = ttk.Label(
        container,
        text="Wisdom Data Collector - Google Trends",
        font="Verdana 18 bold underline",
        foreground="darkblue"
    )
    return label


def developer(container):
    """ Creates the application developer on the window.
        :param container: window to show the application developer
        :type container: tk.Tk
        :return: a tkinter label of the application name
        :rtype: ttk.Label
    """
    label = ttk.Label(
        container,
        text="Application Developed by Dayu Wang",
        font="Verdana 15 italic",
        foreground="darkcyan"
    )
    return label


WINDOW_OPTIONS = {
    "title": "Wisdom Search in Google Trends",
    "state": "zoomed",
    "width_resizable": False,
    "height_resizable": False
}


root = tk.Tk()
root.title(WINDOW_OPTIONS["title"])
root.resizable(WINDOW_OPTIONS["width_resizable"], WINDOW_OPTIONS["height_resizable"])
root.state(WINDOW_OPTIONS["state"])
root.attributes("-topmost", 1)

app_name(root).pack(padx=(0, 0), pady=(40, 0))
developer(root).pack(padx=(0, 0), pady=(30, 0))

try:
    windll.shcore.SetProcessDpiAwareness(1)
finally:
    root.mainloop()
