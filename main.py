import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from threading import Thread
import requests


class AsyncDownload(Thread):
    def __init__(self, url):
        super().__init__()
        self.html = None
        self.url = url

    def run(self):
        response = requests.get(self.url)
        self.html = response.text


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Webpage Download")
        self.geometry("680x430")
        self.resizable(False, False)

        self.createHeaderFrame()
        self.createBodyFrame()
        self.createFooterFrame()

    def createHeaderFrame(self):
        self.header = ttk.Frame(self)
        self.header.columnconfigure(0, weight = 1)
        self.header.columnconfigure(1, weight = 10)
        self.header.columnconfigure(2, weight = 1)

        self.label = ttk.Label(self.header, text = "URL")
        self.label.grid(column = 0, row = 0, sticky = tk.W)

        self.urlVar = tk.StringVar()
        self.urlEntry = ttk.Entry(
            self.header,
            textvariable = self.urlVar,
            width = 80
        )
        self.urlEntry.grid(column = 1, row = 0, sticky = tk.EW)

        self.downloadButton = ttk.Button(self.header, text = "Download")
        self.downloadButton["command"] = self.handleDownload
        self.downloadButton.grid(column = 2, row = 0, sticky = tk.E)

        self.header.grid(column = 0, row = 0, sticky = tk.NSEW, padx = 10, pady = 10)

    def createBodyFrame(self):
        self.body = ttk.Frame(self)
        self.html = tk.Text(self.body, height = 20)
        self.html.grid(column = 0, row = 1)

        scrollBar = ttk.Scrollbar(
            self.body,
            orient = "vertical",
            command = self.html.yview
        )
        scrollBar.grid(column = 1, row = 1, sticky = tk.NS)
        self.html["yscrollcommand"] = scrollBar.set

        self.body.grid(column = 0, row = 1, sticky = tk.NSEW, padx = 10, pady = 10)

    def createFooterFrame(self):
        self.footer = ttk.Frame(self)
        self.footer.columnconfigure(0, weight = 1)

        self.exitButton = ttk.Button(
            self.footer,
            text = "Exit",
            command = self.destroy
        )
        self.exitButton.grid(column = 0, row = 0, sticky = tk.E)

        self.footer.grid(column = 0, row = 2, sticky = tk.NSEW, padx = 10, pady = 10)

    def handleDownload(self):
        url = self.urlVar.get()

        if url:
            self.downloadButton["state"] = tk.DISABLED
            self.html.delete(1.0, "end")

            downloadThread = AsyncDownload(url)
            downloadThread.start()

            self.monitor(downloadThread)
        else:
            showerror(
                title = "Erro",
                message = "Por favor insira a URL da webpage"
            )

    def monitor(self, thread):
        if thread.is_alive():
            self.after(100, lambda: self.monitor(thread))
        else:
            self.html.insert(1.0, thread.html)
            self.downloadButton["state"] = tk.NORMAL


if __name__ == "__main__":
    app = App()
    app.mainloop()