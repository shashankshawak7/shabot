# -*- coding: utf-8 -*-
from chatterbot import ChatBot
import tkinter as tk
try:
    import ttk as ttk
    import ScrolledText
except ImportError:
    import tkinter.ttk as ttk
    import tkinter.scrolledtext as ScrolledText
import time
import socket
host='192.168.1.8'
port=5530
s=socket.socket()
s.connect((host,port))
    
    



class TkinterGUIExample(tk.Tk):

	def __init__(self, *args, **kwargs):
       
		tk.Tk.__init__(self, *args, **kwargs)
		self.title("Chatterbot")

		self.initialize()
		self.chatbot = ChatBot(
            "GUI Bot",
            storage_adapter="chatterbot.storage.SQLStorageAdapter",
            logic_adapters=[
                "chatterbot.logic.BestMatch"
            ],
            input_adapter="chatterbot.input.VariableInputTypeAdapter",
            output_adapter="chatterbot.output.OutputAdapter",
            database="../database.db"
        )

	def initialize(self):
        
        	self.grid()

        	self.respond = ttk.Button(self, text='Send', command=self.get_response)
        	self.respond.grid(column=1, row=3, sticky='nesw', padx=2.5, pady=2)

        	self.usr_input = ttk.Entry(self, state='normal')
        	self.usr_input.grid(column=0, row=3, sticky='nesw', padx=2, pady=2)

        	self.conversation_lbl = ttk.Label(self, anchor=tk.E, text='Conversation:')
        	self.conversation_lbl.grid(column=0, row=1, sticky='nesw', padx=3, pady=3)

        	self.conversation = ScrolledText.ScrolledText(self, state='disabled')
        	self.conversation.grid(column=0, row=2, columnspan=2, sticky='nesw', padx=3, pady=3)
	def get_response(self):
		user_input = self.usr_input.get()
		s.send(user_input.encode())
		data=s.recv(1024)

		self.usr_input.delete(0, tk.END)

		response = data.decode()

		self.conversation['state'] = 'normal'
		self.conversation.insert(
           	 tk.END, "Human: " + user_input + "\n" + "ChatBot: " + str(data) + "\n"
        	)
		self.conversation['state'] = 'disabled'

		time.sleep(0.5)
gui_example = TkinterGUIExample()
gui_example.mainloop()
