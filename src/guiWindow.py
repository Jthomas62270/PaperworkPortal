import tkinter as tk
import sockcon
import requests

class portWindow: 

    def __init__(self): 
        self.root = tk.Tk()
        self.root.title("Port window")

        self.label = tk.Label(self.root, text="IP address: ")
        self.label.pack()

        self.IP = tk.Entry(self.root)
        self.IP.pack()

        self.label = tk.Label(self.root, text="Port address: ")
        self.label.pack()

        self.PORT = tk.Entry(self.root)
        self.PORT.pack()

        self.label = tk.Label(self.root, text="Command: ")
        self.label.pack()

        self.command = tk.Entry(self.root)
        self.command.pack()

        self.button = tk.Button(self.root, text="Send Command", command=self.sendCommand)
        self.button.pack()

        self.status = tk.Label(self.root, text="")
        self.status.pack()

    def sendCommand(self): 
        IP = self.IP.get()
        PORT = self.PORT.get() 
        command = self.command.get()

        exitStatus = sockcon.socketTransmit(IP, int(PORT), command)

        if exitStatus == 1: 
            return 1
        else: 
            self.status.config(text=str(exitStatus))
    
    def run(self): 
        self.root.mainloop()

class MainWindow:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Paperwork Management Portal")

    def getData(): 
        response = requests.get('http://127.0.0.1:5000/api/post/cues/Finding%20Nemo%20Jr.')

    def run(self): 
        self.root.mainloop()
