import tkinter as tk

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

root = tk.Tk()
root.geometry("800x600")
canvas = tk.Canvas(root, width=800, height=600)

# Background Colors
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
    canvas.create_line(160 + 40 * hour, 0, 160 + 40 * hour, 600, fill = '#888888')

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

# Last Update
canvas.create_text(800, 10, text="Last Updated: 5-19-2024 4:14 PM",
                   fill="black", font=('Courier 8'),
                   anchor = 'se', angle=90)

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

# Days of Week
canvas.create_text(100, 495, text="WED 5/18",
                   fill="black", font=('Courier 12'),
                   anchor = 'n', angle=90)

canvas.create_text(100, 385, text="THU 5/19",
                   fill="black", font=('Courier 12'),
                   anchor = 'n', angle=90)

canvas.create_text(100, 275, text="FRI 5/20",
                   fill="black", font=('Courier 12'),
                   anchor = 'n', angle=90)

canvas.create_text(100, 165, text="SAT 5/21",
                   fill="black", font=('Courier 12'),
                   anchor = 'n', angle=90)

canvas.create_text(100, 55, text="SUN 5/22",
                   fill="black", font=('Courier 12'),
                   anchor = 'n', angle=90)

for day in range(5):
    canvas.create_text(120, 495 - 110 * day + 27.5, text="Vyper",
                       fill="black", font=('Courier 10'),
                       anchor = 'n', angle=90)

    canvas.create_text(120, 495 - 110 * day - 27.5, text="Ender",
                       fill="black", font=('Courier 10'),
                       anchor = 'n', angle=90)


# Time of Day
for pos, hour in enumerate(['7 AM', '8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '1 PM',
                            '2 PM', '3 PM', '4 PM', '5 PM', '6 PM',
                            '7 PM']):
    canvas.create_text(140 + 40 * pos, 575, text = hour,
                       fill="black", font=('Courier 10'),
                       anchor = 'n', angle=90)

# Busy times
canvas.create_rectangle(180, 111, 300, 164, fill = '#3F51B5', width = 2)
canvas.create_text(180, 137.5, text = 'IN USE', fill = 'white',
                   font=('Courier 9'), anchor = 'n', angle=90)

canvas.create_rectangle(180, 441, 400, 494, fill = '#3F51B5', width = 2)
canvas.create_text(180, 440 + 27.5, text = 'IN USE', fill = 'white',
                   font=('Courier 9'), anchor = 'n', angle=90)

canvas.create_rectangle(240, 496, 600, 549, fill = '#D50000', width = 2)
canvas.create_text(240, 495 + 27.5, text = 'IN USE', fill = 'white',
                   font=('Courier 9'), anchor = 'n', angle=90)


# Now Marker
canvas.create_line(314, 600, 314, 440, fill = '#00ff00', width = 4)

canvas.pack()
root.mainloop()
