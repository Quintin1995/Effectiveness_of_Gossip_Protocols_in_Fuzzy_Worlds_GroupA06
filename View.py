#other libraries
from itertools import permutations
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys
import time
import tkinter as Tk
from tkinter import scrolledtext

"""
Class for the frame of the GUI
"""
class View(Tk.Frame):
    def __init__(self, master):
        Tk.Frame.__init__(self, master)
        
        self.fig = Figure( figsize=(15, 6), dpi=80 )
        self.line_fig = Figure( figsize=(15, 6), dpi=80 )

        self.pack(side=Tk.RIGHT, fill=Tk.BOTH, expand=1)
        self.sidepanel=SidePanel(self)

        self.leftpanel=LeftPanel(self)

        self.exppanel = Experiment_Panel(self.leftpanel)
        self.parampanel = ParamPanel(self.sidepanel)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

        self.line_canvas = FigureCanvasTkAgg(self.line_fig, master=self)
        self.line_canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

"""
Contains information about the currently running model, including the previous calls, as well as the current state of the session.
"""
class LeftPanel(Tk.Frame):
    def __init__(self, master):
        Tk.Frame.__init__(self, master)
        self.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)

        #Frame for fields
        self.group_info = Tk.LabelFrame(self, text="Session information", padx=5, pady=5)
        self.group_info.pack(side="top", fill=Tk.BOTH)
        
        #Protocol status text
        self.model_state_lbl = Tk.Label(self.group_info, text="State: Running", fg="blue")
        self.model_state_lbl.config(font=("Courier", 33))
        self.model_state_lbl.pack(side="top", fill=Tk.BOTH)

        #amount calls made txt
        self.model_iter_lbl = Tk.Label(self.group_info, text="Calls made: 0")
        self.model_iter_lbl.pack(side="top", fill=Tk.BOTH)

        #call log
        self.model_call_log_lbl = Tk.Label(self.group_info, text="Call Log", fg="green")
        self.model_call_log_lbl.pack(side="top", fill=Tk.BOTH)
        self.model_call_log_textarea = Tk.Text(self.group_info, height=20, width=35)
        self.model_call_log_textarea.pack(side="top", fill=Tk.BOTH)

"""
Panel on the bottom left side, contains UI elements for running multiple trials and collecting data.
"""
class Experiment_Panel(Tk.Frame):
    def __init__(self, master):
        Tk.Frame.__init__(self, master)
        self.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)

        #Frame for fields
        self.exp_params_frame = Tk.LabelFrame(self, text="Experiment Parameters\nThis will not render anything in the UI", padx=5, pady=5)
        self.exp_params_frame.pack(side="top", fill=Tk.BOTH)

        #Maximum amount iterations that will be allowed
        Tk.Label(self.exp_params_frame, text="max iterations allowed").pack(side="top", fill=Tk.BOTH)
        self.max_allowed_iters = Tk.Spinbox(self.exp_params_frame, from_=1, to=1000000)
        self.max_allowed_iters.delete(0,"end")
        self.max_allowed_iters.insert(0,"9999")
        self.max_allowed_iters.pack(side="top", fill=Tk.BOTH)

        #The amount of experiments that will be performed
        Tk.Label(self.exp_params_frame, text="Trial Count").pack(side="top", fill=Tk.BOTH)
        self.experi_count = Tk.Spinbox(self.exp_params_frame, from_=1, to=1000000)
        self.experi_count.delete(0,"end")
        self.experi_count.insert(0,"100")
        self.experi_count.pack(side="top", fill=Tk.BOTH)

        #file name of folder that results will be stored
        self.data_folder_name_lbl = Tk.Label(self.exp_params_frame, text="Experiment Folder Name", fg="black")
        self.data_folder_name_lbl.pack(side="top", fill=Tk.BOTH)
        self.data_folder_name_textarea = Tk.Text(self.exp_params_frame, height=1, width=35)
        self.data_folder_name_textarea.pack(side="top", fill=Tk.BOTH)
        #set init string for this textarea
        current_time = time.strftime('%x_%X').replace('-', '_')
        default_folder = "exp_{}".format(current_time)        #put current time and date into the folder
        self.data_folder_name_textarea.insert(Tk.END, default_folder )

        #Experiment run button
        self.run_experi_butn = Tk.Button(self.exp_params_frame, text="Run Experiments")
        self.run_experi_butn.pack(side="top",fill=Tk.BOTH)

        # Progress bar 
        self.progress_bar = Tk.Label(self.exp_params_frame, text="No experiment running")
        self.progress_bar.pack(side="top", fill=Tk.BOTH)

"""
Contains the buttons for making steps in a single session.
Do iterations / Do N iterations.
"""
class SidePanel(Tk.Frame):
    def __init__(self, master):
        Tk.Frame.__init__(self, master)
        self.pack(side=Tk.RIGHT, fill=Tk.BOTH, expand=1)

        self.group_run = Tk.LabelFrame(self, text="Run model", padx=5, pady=5)
        self.group_run.pack(side="bottom", fill=Tk.BOTH)

        self.iterBut = Tk.Button(self.group_run, text="1 iteration")
        self.iterBut.pack(side="top",fill=Tk.BOTH)
        
        Tk.Label(self.group_run, text="Amount iterations").pack(side="top", fill=Tk.BOTH)
        self.amount_iterations = Tk.Spinbox(self.group_run, from_=1, to=10000)
        self.amount_iterations.pack(side="top", fill=Tk.BOTH)

        self.iterXBut = Tk.Button(self.group_run, text="Do N iterations")
        self.iterXBut.pack(side="top",fill=Tk.BOTH)


"""
Contains the UI elements for the adjustable model parameters.
"""
class ParamPanel(Tk.Frame):
    def __init__(self, master):
        Tk.Frame.__init__(self, master)
        self.pack(side=Tk.BOTTOM, fill=Tk.BOTH, expand=1)

        self.group_model = Tk.LabelFrame(self, text="Model parameters", padx=5, pady=5)
        self.group_model.pack(side="top", fill=Tk.BOTH)

        AVAILABLE_MODELS = ["ANY", "CO", "LNS", "SPI", "TOK"]
        self.selected_model = Tk.StringVar(self)
        self.selected_model.set("ANY") # default value

        Tk.Label(self.group_model, text="Protocol").pack(side="top", fill=Tk.BOTH)
        self.model_selector = Tk.OptionMenu(self.group_model, self.selected_model, *AVAILABLE_MODELS)
        self.model_selector.pack(side="top", fill=Tk.BOTH)

        # PHONEBOOK_TRANSFER_MODE = ["YES", "NO"]
        # self.selected_pb_mode = Tk.StringVar(self)
        # self.selected_pb_mode.set("YES") # default value

        # Tk.Label(self.group_model, text="Transfer phonebook").pack(side="top", fill=Tk.BOTH)
        # self.pb_mode_selector = Tk.OptionMenu(self.group_model, self.selected_pb_mode, *PHONEBOOK_TRANSFER_MODE)
        # self.pb_mode_selector.pack(side="top", fill=Tk.BOTH)

        self.pb_mode_var = Tk.IntVar()
        self.pb_mode_selector = Tk.Checkbutton(self.group_model, text="Transfer phonebook", variable=self.pb_mode_var)
        self.pb_mode_selector.pack(side="top", fill=Tk.BOTH)

        Tk.Label(self.group_model, text="Amount agents").pack(side="top", fill=Tk.BOTH)
        self.amount_agents = Tk.Spinbox(self.group_model, from_=3, to=100)
        self.amount_agents.delete(0,"end")
        self.amount_agents.insert(0,"10")
        self.amount_agents.pack(side="top", fill=Tk.BOTH)

        AVAILABLE_PHONEBOOKS = ["LIE", "MISTAKE"]
        self.selected_behavior = Tk.StringVar(self)
        self.selected_behavior.set("LIE") # default value

        Tk.Label(self.group_model, text="Behavior").pack(side="top", fill=Tk.BOTH)
        self.behavior_selector = Tk.OptionMenu(self.group_model, self.selected_behavior, *AVAILABLE_PHONEBOOKS)
        self.behavior_selector.pack(side="top", fill=Tk.BOTH)

        Tk.Label(self.group_model, text="Chance of telling the truth in percentage").pack(side="top", fill=Tk.BOTH)
        self.transfer_chance = Tk.Spinbox(self.group_model, from_=1, to=100)
        self.transfer_chance.delete(0,"end")
        self.transfer_chance.insert(0,"100")
        self.transfer_chance.pack(side="top", fill=Tk.BOTH)

        Tk.Label(self.group_model, text="Strength of a lie in percentage").pack(side="top", fill=Tk.BOTH)
        self.lie_factor = Tk.Spinbox(self.group_model, from_=0, to=1)
        self.lie_factor.delete(0,"end")
        self.lie_factor.insert(0,"25")
        self.lie_factor.pack(side="top", fill=Tk.BOTH)

        AVAILABLE_PHONEBOOKS = ["ALL", "TWO WORLDS", "PARTIAL GRAPH", "CUSTOM GRAPH"]
        self.selected_phonebook = Tk.StringVar(self)
        self.selected_phonebook.set("ALL") # default value

        Tk.Label(self.group_model, text="Phonebook").pack(side="top", fill=Tk.BOTH)
        self.phonebook_selector = Tk.OptionMenu(self.group_model, self.selected_phonebook, *AVAILABLE_PHONEBOOKS)
        self.phonebook_selector.pack(side="top", fill=Tk.BOTH)

        Tk.Label(self.group_model, text="Connectivity of the Partial Graph in percentage").pack(side="top", fill=Tk.BOTH)
        self.amount_connectivity = Tk.Spinbox(self.group_model, from_=1, to=100)
        self.amount_connectivity.delete(0,"end")
        self.amount_connectivity.insert(0,"100")
        self.amount_connectivity.pack(side="top", fill=Tk.BOTH)

        #graph creator panel
        info_string = "Graph creator, on tuples (without paranthesis)\n Example:\n 0,1\n1,0\n2,0" + "\nSet phonebook to CUSTOM GRAPH" + "\nClick on set model"
        new_info_string = "Graph Creator, example:\n ([[0,1],[1,2],[2,3],[3]],[[0],[1],[2],[3]])\nSet phonebook to CUSTOM GRAPH\nSource: https://w4eg.de/malvin/illc/webgossip"
        self.model_param_pnl_graph_creator_lbl = Tk.Label(self.group_model, text=new_info_string, fg="red")
        self.model_param_pnl_graph_creator_lbl.pack(side="top", fill=Tk.BOTH)
        self.model_param_pnl_graph_creator_textarea = Tk.Text(self.group_model, height=10, width=20)
        self.model_param_pnl_graph_creator_textarea.insert(Tk.END, "([[0,1],[1,2],[2,3],[3]],[[0],[1],[2],[3]])")
        self.model_param_pnl_graph_creator_textarea.pack(side="top", fill=Tk.BOTH)

        self.resetButton = Tk.Button(self.group_model, text="Set model")
        self.resetButton.pack(side="top",fill=Tk.BOTH)
        
    """
    Returns a figure to be used for plotting by the controller.
    """
    def retrieve_input_graph(self):
        return self.model_param_pnl_graph_creator_textarea.get("1.0",'end-1c')