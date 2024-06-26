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

        self.bind('<Control-Key-d>', self.select_XMPdirectory)
        self.bind('<Control-Key-1>', self.step1_initial_label_XMPs)
        self.bind('<Control-Key-2>', self.step2_interpolate)

        self.first_row = 0
        self.columns_to_display = ['exif DateTimeOriginal', 'crs Temperature', 'crs Tint', 'crs Exposure2012', 'exif FNumber', 'awim CommaSeparatedTags'] # need to add comma-separated tags

    def select_XMPdirectory(self, event):
        self.controller.XMPdirectory = filedialog.askdirectory(title='Select XMP directory.')

    def read_XMPs(self):
        self.controller.XMP_snapshot, self.controller.lapse_latlng = XMPtext.readXMPfiles(self.controller.XMPdirectory)
        self.controller.XMP2 = self.controller.XMP_snapshot.copy()

    def step1_initial_label_XMPs(self, event):
        # read XMP files
        self.read_XMPs()
        # set variables for sun and moon calculations
        moments_list = self.controller.XMP2['exif DateTimeOriginal'].values
        moments_list = formatters.format_datetimes(input_datetime=moments_list, direction='from list of ISO 8601 strings')
        print(self.controller.lapse_latlng)
        # calculate sun and moon values
        sun_az_list, sun_art_list = astropytools.get_AzArts(earth_latlng=self.controller.lapse_latlng, moments=moments_list, celestial_object='sun')
        moon_az_list, moon_art_list = astropytools.get_AzArts(earth_latlng=self.controller.lapse_latlng, moments=moments_list, celestial_object='moon')
        # convert sun and moon values to day, night, twilight labels, format numbers, add to dataframe
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
        # concatenate new tags together with the old tags, comma-separated
        self.controller.XMP2['awim CommaSeparatedTags'] = self.controller.XMP2.apply(lambda x:'%s,%s' % (x['awim CommaSeparatedTags'], x['awim DayNightTwilight']), axis=1)
        # save dataframe to CSV file
        timenow = datetime.datetime.now()
        time_string = formatters.format_datetimes(timenow, 'to string for filename')
        filename = f'XMP_step1 {time_string}.csv'
        filepath = os.path.join(self.controller.XMPdirectory, filename)
        self.controller.XMP2.to_csv(filepath)
        # self.display_dataframe() # unnecessary, but wanted to see what it looks like
        # write the comma-separated tags to the XMP files
        XMPtext.addTags(self.controller.XMP_snapshot, self.controller.XMP2, self.controller.XMPdirectory)
        print('Completed step 1 labelling XMP files with cellestial events.')


    def display_dataframe(self):
        self.display_dataframe = self.controller.XMP2[self.columns_to_display]
        self.table = pt = pandastable.Table(self, dataframe=self.display_dataframe, showtoolbar=True, showstatusbar=True)

        pt.show()
        # this frame will display the selected fields from XMP files and allow to modify by defining keyframes etc

    def step2_interpolate(self, event):
        self.read_XMPs()
        self.controller.columns_to_interpolate = ['crs Temperature', 'crs Tint', 'crs Exposure2012', 'crs Contrast2012', 'crs Highlights2012', 'crs Shadows2012', 'crs Whites2012', 'crs Blacks2012', 'crs Texture', 'crs Clarity2012', 'crs Dehaze', 'crs Vibrance', 'crs Saturation']
        self.controller.XMP2 = XMPtext.interpolate(self.controller.XMP_snapshot, self.controller.columns_to_interpolate)
        # save dataframe to CSV file
        timenow = datetime.datetime.now()
        time_string = formatters.format_datetimes(timenow, 'to string for filename')
        filename = f'XMP_step2 {time_string}.csv'
        filepath = os.path.join(self.controller.XMPdirectory, filename)
        self.controller.XMP2.to_csv(filepath)
        # self.display_dataframe() # unnecessary, but wanted to see what it looks like
        # write the new values to the XMP files
        XMPtext.write_values(self.controller.XMP2, self.controller.columns_to_interpolate, self.controller.XMPdirectory)
        print('Completed step 2 interpolating between the keyframes and writing to XMP files.')


class lensVisualization(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller



#------------------------------------------- Procedural --------------------------------------
if __name__ == '__main__':
    AWIM2 = AppWindow()
    AWIM2.mainloop()