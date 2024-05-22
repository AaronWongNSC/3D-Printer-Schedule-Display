import tkinter as tk
import get_time
import datetime 

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

def display_schedule(canvas, schedule):
    canvas.create_rectangle(0, 0, 800, 600, fill = '#FFFFFF')
    create_static(canvas)
    show_days(canvas, schedule)
    show_last_update(canvas, schedule)
    show_busy(canvas, schedule)
    show_now(canvas, schedule)
    
    canvas.pack()

def create_static(canvas):
    # Background Shading
    for day in range(5):
        canvas.create_rectangle(120, 495 - 110 * day, 660, 495 - 110 * day + 55,
                                fill = '#d9aaaa', outline = '#d9aaaa')
        canvas.create_rectangle(120, 495 - 110 * day, 660, 495 - 110 * day - 55,
                                fill = '#ccccff', outline = '#ccccff')
    
    # Horizontal Lines
    canvas.create_line(100, 0, 100, 600)
    canvas.create_line(140, 0, 140, 600)
    canvas.create_line(800, 0, 800, 600)
    
    canvas.create_line(100, 600, 800, 600)
    canvas.create_line(100, 0, 800, 0)
    
    for hour in range(13):
        canvas.create_line(180 + 40 * hour, 0, 180 + 40 * hour, 600)
        canvas.create_line(160 + 40 * hour, 0, 160 + 40 * hour, 600, fill = '#AAAAAA')
    
    # Vertical Lines
    for day in range(5):
        canvas.create_line(100, 550 - 110 * day, 660, 550 - 110 * day)
    
    # Title
    canvas.create_text(20, 300, text="Nevada State University",
                       fill="black", font=('Courier 18'),
                       anchor = 'n', angle=90)
    
    canvas.create_text(45, 300, text="3D Printer Schedule",
                       fill="black", font=('Courier 18'),
                       anchor = 'n', angle=90)

    # Info lines
    canvas.create_text(680, 300, text="Link to the full schedule, sign-up page,",
                       fill="black", font=('Courier 14'),
                       anchor = 'n', angle=90)
    
    canvas.create_text(700, 300, text="and other information about these printers:",
                       fill="black", font=('Courier 14'),
                       anchor = 'n', angle=90)
    
    canvas.create_text(730, 300, text="https://bit.ly/NSU3D (or whatever)",
                       fill="black", font=('Courier 18'),
                       anchor = 'n', angle=90)

    # Time of Day
    for pos, hour in enumerate(['7 AM', '8 AM', '9 AM', '10 AM', '11 AM', '12 PM',
                                '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM']):
        canvas.create_text(141 + 40 * pos, 575, text = hour,
                           fill="black", font=('Courier 10'),
                           anchor = 'n', angle=90)

    # 3D Printer Labels        
    for day in range(5):
        canvas.create_text(121, 495 - 110 * day + 27.5, text="Vyper",
                           fill="black", font=('Courier 10'),
                           anchor = 'n', angle=90)

        canvas.create_text(121, 495 - 110 * day - 27.5, text="Ender",
                           fill="black", font=('Courier 10'),
                           anchor = 'n', angle=90)

def show_days(canvas, schedule):
    time = schedule.now
    for day in range(5):
        dt = time + day * datetime.timedelta(days = 1)
        canvas.create_text(101, 495 - 110 * day,
                           text=dt.strftime('%a %m/%d').upper(),
                           fill="black", font=('Courier 12'),
                           anchor = 'n', angle=90)


def show_now(canvas, schedule):
    time = schedule.now
    pos = time_position(time)
    if (pos < 140) or (pos > 660):
        return
    canvas.create_line(pos, 600, pos, 441, fill = '#00ff00', width = 4)

def show_last_update(canvas, schedule):
    time = schedule.now
    dt = get_time.disp_time(time)
    canvas.create_text(800, 10, text="Last Updated: {}".format(dt),
                       fill="black", font=('Courier 8'),
                       anchor = 'se', angle=90)

def show_busy(canvas, schedule):
    time = schedule.now
    prints = schedule.prints
    info = {
        'ender': {
            'offset': 0,
            'color': '#3F51B5'
            },
        'vyper': {
            'offset': 55,
            'color': '#D50000'
            }
        }
    
    today = get_time.get_date(get_time.utc_to_local(time))
    for event in prints:
        print('Displaying event {title}, {start} to {end} on {printer}'.format(**event))
        start_date = get_time.get_date(event['start'])
        end_date = get_time.get_date(event['end'])
        print_days = (end_date - start_date).days
        printer = info[event['printer']]

        if print_days == 0:
            offset_days = (start_date - today).days
            start_pos = time_position(event['start'])
            if start_pos < 140:
                start_pos = 140
            if start_pos > 660:
                continue

            end_pos = time_position(event['end'])
            if end_pos < 140:
                continue
            if end_pos > 660:
                end_pos = 660
            
            if start_pos == end_pos:
                continue
            
            canvas.create_rectangle(start_pos, 441 - 110 * offset_days + printer['offset'],
                                    end_pos, 441 - 110 * offset_days + printer['offset'] + 53,
                                    fill = printer['color'], width = 2)
            canvas.create_text(start_pos, 441 + 27.5 - 110 * offset_days + printer['offset'],
                               text = 'IN USE', fill = 'white', font=('Courier 9'),
                               anchor = 'n', angle=90)
        else:
            offset_days = (start_date - today).days
            if offset_days >= 0:
                start_pos = time_position(event['start'])
                if start_pos < 140:
                    start_pos = 140
                if (start_pos >= 140) and (start_pos < 660):
                    canvas.create_rectangle(start_pos, 441 - 110 * offset_days + printer['offset'],
                                            660, 441 - 110 * offset_days + printer['offset'] + 53,
                                            fill = printer['color'], width = 2)
                    canvas.create_text(start_pos, 441 + 27.5 - 110 * offset_days + printer['offset'],
                                       text = 'IN USE', fill = 'white', font=('Courier 9'),
                                       anchor = 'n', angle=90)
    
                for full_days in range(print_days - 1):
                    canvas.create_rectangle(140, 441 - 110 * (offset_days + full_days + 1) + printer['offset'],
                                            660, 441 - 110 * (offset_days + full_days + 1) + printer['offset'] + 53,
                                            fill = printer['color'], width = 2)
                    canvas.create_text(140, 441 + 27.5 - 110 * (offset_days + full_days + 1) + printer['offset'],
                                       text = 'IN USE', fill = 'white', font=('Courier 9'),
                                       anchor = 'n', angle=90)
            else:
                offset_days = (end_date - today).days
                if offset_days > 0:
                    for full_days in range(offset_days):
                        canvas.create_rectangle(140, 441 - 110 * full_days + printer['offset'],
                                                660, 441 - 110 * full_days + printer['offset'] + 53,
                                                fill = printer['color'], width = 2)
                        canvas.create_text(140, 441 + 27.5 - 110 * full_days + printer['offset'],
                                           text = 'IN USE', fill = 'white', font=('Courier 9'),
                                           anchor = 'n', angle=90)
                    
                
                    
            offset_days = (end_date - today).days
            end_pos = time_position(event['end'])
            if end_pos > 660:
                end_pos = 660
            if (end_pos > 140) and (end_pos <= 660):
                canvas.create_rectangle(140, 441 - 110 * offset_days + printer['offset'],
                                        end_pos, 441 - 110 * offset_days + printer['offset'] + 53,
                                        fill = printer['color'], width = 2)
                canvas.create_text(140, 441 + 27.5 - 110 * offset_days + printer['offset'],
                                   text = 'IN USE', fill = 'white', font=('Courier 9'),
                                   anchor = 'n', angle=90)
    
def time_position(time):
    hour = int(time.strftime('%H'))
    minute = int(time.strftime('%M'))
    return 140 + 40 * (hour - 7 + minute / 60)
