from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import pymongo, numpy as np
from datetime import datetime
from datetime import timedelta as dt
from Classes import Doctor, Patient, Specialization
from appointment import Appointment
import pymongo, datetime, calendar, math, speech_recognition as sr, numpy as np, nltk
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta as dt
from deep_translator import GoogleTranslator
from nltk.tokenize import word_tokenize
from nltk import pos_tag 
from pathlib import Path
from voice_recognition import Speech

client = pymongo.MongoClient(
    "mongodb+srv://ams1234:ams1234@cluster0.ph4hzjn.mongodb.net/"
)
db = client["AMS-Test"]

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH_wel = OUTPUT_PATH / Path(r"C:\Users\Swamynathan\Documents\Vijay_Official\SIH\FrontEnd\build_welcome\assets\frame0")
ASSETS_PATH_symp = OUTPUT_PATH / Path(r"C:\Users\Swamynathan\Documents\Vijay_Official\SIH\FrontEnd\build_symptoms\assets\frame0")
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Swamynathan\Documents\Vijay_Official\SIH\FrontEnd\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
def relative_to_assets_wel(path: str) -> Path:
    return ASSETS_PATH_wel / Path(path)
def relative_to_assets_symp(path: str) -> Path:
    return ASSETS_PATH_symp / Path(path)



def tk_output(scr, op):
    scr.destroy()
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
        text=op,
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

def tk_symptoms(scr, id):
    scr.destroy()
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
        file=relative_to_assets_symp("image_1.png"))
    image_1 = canvas.create_image(
        240.0,
        160.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets_symp("image_2.png"))
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

    canvas.create_text(
        177.0,
        150.0,
        anchor="nw",
        text="Kindly Describe your symptoms ",
        fill="#30366E",
        font=("Inter Bold", 15 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets_symp("button_1.png"))

    def call_speech():
        global s
        s = Speech()
        s.speak()

    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: call_speech(),
        relief="flat"
    )
    button_1.place(
        x=105.0,
        y=135.0,
        width=50.0,
        height=50.0
    )
    def call_app(s):
        a = Appointment(id)
        a.get_symp_decide_spltn(s)
        a.fix_doctor()
        text = a.get_out_str(Doctor(a.doctor_id))
        tk_output(window, text)

    button_image_2 = PhotoImage(
        file=relative_to_assets_symp("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: call_app(s),
        relief="flat"
    )
    button_2.place(
        x=314.0,
        y=238.0,
        width=132.0,
        height=35.0
    )

    canvas.create_text(
        326.0,
        246.0,
        anchor="nw",
        text="Book Appointment",
        fill="#3EF200",
        font=("Inter Bold", 12 * -1)
    )
    window.resizable(False, False)
    window.mainloop()

def tk_welcome():
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
        file=relative_to_assets_wel("image_1.png"))
    image_1 = canvas.create_image(
        147.0,
        160.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets_wel("image_2.png"))
    image_2 = canvas.create_image(
        137.0,
        230.0,
        image=image_image_2
    )

    canvas.create_text(
        64.0,
        151.0,
        anchor="nw",
        text="Place Your Fingerprint ",
        fill="#30366E",
        font=("Inter Bold", 10 * -1)
    )
    image_image_3 = PhotoImage(
        file=relative_to_assets_wel("image_3.png"))
    image_3 = canvas.create_image(
        383.0,
        160.0,
        image=image_image_3
    )

    canvas.create_text(
        27.0,
        35.0,
        anchor="nw",
        text=" Welcome to KIOSK   Health Care  Machine",
        fill="#31376F",
        font=("Inter", 12 * -1)
    )
    window.resizable(False, False)
    def finger(scr):
        id = input("Enter Patient ID: ")
        tk_symptoms(scr, id)



    button_image_1 = PhotoImage(
        file=relative_to_assets_wel("button_1.png"))
    
    

    
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: finger(window),
        relief="flat"
    )
    button_1.place(
        x=112.0,
        y=205.0,
        width=50.0,
        height=50.0
    )
    window.mainloop()


tk_welcome()
