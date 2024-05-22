import tkinter as tk
import datetime

import calendar_api
import get_time
import display

class Schedule():
    def __init__(self):
        self.now = None
        self.prints = None
    
    def update(self):
        self.update_time()
        if self.now is None:
            return
        self.update_prints()
    
    def update_time(self):
        self.now = get_time.utc_to_local(get_time.get_utc_time())

    def update_prints(self):
        today = get_time.get_date(get_time.utc_to_local(self.now))
        later = today + datetime.timedelta(days = 5)
        self.prints = calendar_api.get_events(today, later)
        

def update_window(schedule):
    schedule.update()
    if (schedule.now is not None) and (schedule.prints is not None):
        print('Update: {}'.format(schedule.now))
        display.display_schedule(canvas, schedule)
    else:
        print('Failed Update')
    root.after(1000, update_window, schedule)    

root = tk.Tk()
root.geometry('800x600')
#root.attributes('-fullscreen',True)

schedule = Schedule()

canvas = tk.Canvas(root, width=800, height=600)
canvas.create_text(400, 300, text="LOADING SCHEDULE...",
                   fill="black", font=('Courier 24'),
                   anchor = 'n', angle=90)
canvas.pack()

root.after(1000, update_window, schedule)

root.mainloop()
