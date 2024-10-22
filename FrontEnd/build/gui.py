
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Swamynathan\Documents\Vijay_Official\SIH\FrontEnd\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("480x320")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 320,
    width = 480,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    240.0,
    160.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    240.0,
    55.0,
    image=image_image_2
)

canvas.create_text(
    70.0,
    40.0,
    anchor="nw",
    text="KIOSK Health Care Machine",
    fill="#3EF200",
    font=("Inter Bold", 25 * -1)
)

canvas.create_rectangle(
    46.0,
    94.0,
    229.0,
    274.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    58.0,
    105.0,
    anchor="nw",
    text="Output",
    fill="#5811CA",
    font=("Inter Bold", 10 * -1)
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    345.0,
    184.0,
    image=image_image_3
)
window.resizable(False, False)
window.mainloop()
