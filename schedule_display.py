import tkinter as tk
import datetime

import sys
import calendar_api
import get_time
import display

DELAY = 5 * 60000

class Schedule():
    def __init__(self):
        self.now = None
        self.prints = None
        self.status = None
    
    def update(self):
        self.update_time()
        if self.now is None:
            return
        self.update_prints()
    
    def update_time(self):
        self.now = get_time.get_utc_time()
        if self.now is not None:
            self.now = get_time.utc_to_local(self.now)

    def update_prints(self):
        today = get_time.get_date(get_time.utc_to_local(self.now))
        later = today + datetime.timedelta(days = 5)
        self.prints = calendar_api.get_events(today, later)
        

def update_window(schedule):
    schedule.update()
    delay = DELAY
    attract_delay = 5000
    if (schedule.now is not None) and (schedule.prints is not None):
        if schedule.status == 'Display':
            schedule.status = 'ART240'
            print('Show ART 240 page: {}'.format(schedule.now))
            display.attract(canvas)
            delay = attract_delay
        else:
            schedule.status = 'Display'
            print('Update: {}'.format(schedule.now))
            display.display_schedule(canvas, schedule)
    else:
        print('Failed Update')
        schedule.status = 'Fail'
        display.display_loading(canvas)
    root.after(delay, update_window, schedule)

try:
    root = tk.Tk()
    root.geometry('800x600')
    root.attributes('-fullscreen',True)
    
    schedule = Schedule()
    
    canvas = tk.Canvas(root, width=800, height=600)
    
    display.display_loading(canvas)
    canvas.pack()
    
    root.after(1000, update_window, schedule)
    
    root.mainloop()

except:
    root.destroy()
    sys.exit(1)
