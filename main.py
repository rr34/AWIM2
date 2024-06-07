from tkinter import Tk, filedialog # messagebox, Entry, filedialog, Menu, StringVar, Frame, Label, scrolledtext, WORD, END, font as tkfont, Listbox
from tkinter.ttk import *
from tkinter import scrolledtext, END, font as tkfont
from time import perf_counter
import XMPtext

class AppWindow(Tk):
    def __init__(self):
        super().__init__()
        #---------------------------------------- App Initialization ------------------------------
        self.title('AstroWideImageMapper2 by Time v3 Technology')
        self.state('normal')

        #---------------------------------------- Frames Container --------------------------------
        self.prompt_font = tkfont.Font(family='Helvetica', size=20)
        self.small_font = tkfont.Font(family='Helvetica', size=12)
        self.container = Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        #---------------------------------------- Controller Variables ----------------------------

        #---------------------------------------- Generate Frames ---------------------------------
        self.frames = {}

        for F in (XMPdisplay, lensVisualization):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            frame.pack(side='top', fill='both', expand=True)

            self.frames[page_name] = frame

        self.current_frame = 'XMPdisplay'
        self.show_frame('XMPdisplay')

        self.bind_all('<Control-Key-1>', self.show1)

    def show_frame(self, page_name):
        for frame in self.frames.values():
            frame.pack_forget()
        frame = self.frames[page_name]
        frame.pack(side='top', fill='both', expand=True)
        frame.focus()
        self.current_frame = page_name

    def show1(self, event):
        self.show_frame('XMPdisplay')

    def save_and_exit(self, event):
        self.current_game.save_log_file()
        self.destroy()

class XMPdisplay(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.bind('<Control-Key-f>', self.select_XMPdirectory)
        self.bind('<Control-Key-r>', self.readXMPfiles)

    def select_XMPdirectory(self, event):
        self.controller.XMPdirectory = filedialog.askdirectory(title='Select XMP directory.')

    def readXMPfiles(self, event):
        XMPtext.readXMPfiles(self.controller.XMPdirectory)

        # this frame will display the selected fields from XMP files and allow to modify by defining keyframes etc

class lensVisualization(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller



#------------------------------------------- Procedural --------------------------------------
if __name__ == '__main__':
    AWIM2 = AppWindow()
    AWIM2.mainloop()