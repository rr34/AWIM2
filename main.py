from tkinter import Tk, filedialog # messagebox, Entry, filedialog, Menu, StringVar, Frame, Label, scrolledtext, WORD, END, font as tkfont, Listbox
from tkinter.ttk import *
from tkinter import scrolledtext, END, font as tkfont
import pandas as pd
from time import perf_counter
import os, pathlib
import datetime
import XMPtext, formatters, astropytools #, awimlib
import pandastable

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
        self.bind('<Control-Key-w>', self.writeXMPfiles)

        self.first_row = 0
        self.columns_to_display = ['exif DateTimeOriginal', 'crs Temperature', 'crs Tint', 'crs Exposure2012', 'exif FNumber', 'awim CommaSeparatedTags'] # need to add comma-separated tags

    def select_XMPdirectory(self, event):
        self.controller.XMPdirectory = filedialog.askdirectory(title='Select XMP directory.')

    def readXMPfiles(self, event):
        self.controller.XMP_snapshot, self.controller.lapse_latlng = XMPtext.readXMPfiles(self.controller.XMPdirectory)
        self.controller.XMP2 = self.controller.XMP_snapshot.copy()
        self.process_XMP_data()
        self.writeXMPfiles()
    
    def process_XMP_data(self):
        moments_list = self.controller.XMP2['exif DateTimeOriginal'].values
        moments_list = formatters.format_datetimes(input_datetime=moments_list, direction='from list of ISO 8601 strings')
        print(self.controller.lapse_latlng)
        sun_az_list, sun_art_list = astropytools.get_AzArts(earth_latlng=self.controller.lapse_latlng, moments=moments_list, celestial_object='sun')
        moon_az_list, moon_art_list = astropytools.get_AzArts(earth_latlng=self.controller.lapse_latlng, moments=moments_list, celestial_object='moon')
        day_night_twilight_list = astropytools.day_night_twilight(sun_art_list, moon_art_list)
        sun_az_list = formatters.round_to_string(sun_az_list, 'azimuth')
        sun_art_list = formatters.round_to_string(sun_art_list, 'artifae')
        moon_az_list = formatters.round_to_string(moon_az_list, 'azimuth')
        moon_art_list = formatters.round_to_string(moon_art_list, 'artifae')
        self.controller.XMP2['awim SunAz'] = sun_az_list
        self.controller.XMP2['awim SunArt'] = sun_art_list
        self.controller.XMP2['awim MoonAz'] = moon_az_list
        self.controller.XMP2['awim MoonArt'] = moon_art_list
        self.controller.XMP2['awim DayNightTwilight'] = day_night_twilight_list
        self.controller.XMP2['awim CommaSeparatedTags'] = self.controller.XMP2.apply(lambda x:'%s,%s' % (x['awim CommaSeparatedTags'], x['awim DayNightTwilight']), axis=1)

        timenow = datetime.datetime.now()
        time_string = formatters.format_datetimes(timenow, 'to string for filename')
        filename = 'XMP2 %s.csv' % (time_string)
        filepath = os.path.join(self.controller.XMPdirectory, filename)
        self.controller.XMP2.to_csv(filepath)
        
        self.display_dataframe()

    def writeXMPfiles(self):
        XMPtext.addTags(self.controller.XMP_snapshot, self.controller.XMP2, self.controller.XMPdirectory)

    def display_dataframe(self):
        self.display_dataframe = self.controller.XMP2[self.columns_to_display]
        self.table = pt = pandastable.Table(self, dataframe=self.display_dataframe, showtoolbar=True, showstatusbar=True)

        pt.show()

        # this frame will display the selected fields from XMP files and allow to modify by defining keyframes etc

class lensVisualization(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller



#------------------------------------------- Procedural --------------------------------------
if __name__ == '__main__':
    AWIM2 = AppWindow()
    AWIM2.mainloop()