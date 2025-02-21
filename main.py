# -----------------Imports-----------------
import customtkinter
import shared.customtk as customtk
import tkinter as tk
import os, random
import json
from colorama import init as colorama_init
from termcolor import colored
from PIL import Image, ImageTk, ImageColor
from shared.transforms import RGBTransform
# -------------------End-------------------

colorama_init() # Initialize colorama for pretty printing
primary_color = '#00aeef' # Primary color of UI
customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

root = customtkinter.CTk()
root.title("PreciseDose")
root.attributes('-fullscreen', True)

screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()

# -----------------UI Initialize-----------------
canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
canvas.pack()

background_image = customtk.create_tk_image('assets\\backgrounds\\sample.jpg', screen_width, screen_height)
canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

static_img = customtk.create_tk_image('assets\\static\\static_v2.png', screen_width, screen_height)
canvas.create_image(0, 0, anchor=tk.NW, image=static_img)

color_static = Image.open("assets\\static\\color.png")
color_static = color_static.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
alpha = color_static.split()[-1]
color_static = color_static.convert("RGB")
color_static = RGBTransform().mix_with(ImageColor.getcolor(primary_color, "RGB"),factor=1).applied_to(color_static)
color_static.putalpha(alpha)
color_static = ImageTk.PhotoImage(color_static)
canvas.create_image(0, 0 ,anchor=tk.NW, image=color_static)
# ------------------------End------------------------

# -----------------Patient Intialize-----------------
patient = random.choice(os.listdir("content\\patients")) # Select a random patient
patient_id = int(patient.rstrip(".json"))
patient = json.load(open(f"content\\patients\\{patient}")) # Parse JSON to Dictionary
print(colored(" INFO ", 'black', 'on_yellow'),  f"Selected Patient: {patient['name']} [ID: {patient_id}] from path" , colored(f"'content\\patients\\{patient_id}.json'", 'light_grey', 'on_dark_grey'))

# Update Profile
canvas.create_text(152, 73, text=patient['name'], font=('Alte Haas Grotesk', 17, 'bold'), fill='Grey30', anchor=tk.NW)
patient_headshot = customtk.create_tk_image(f"content\\avatars\\{patient_id}.png", 100, 100)
canvas.create_image(30, 66, image=patient_headshot, anchor=tk.NW)
canvas.create_text(205, 126, text=patient['age'], font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey30', anchor=tk.W, justify='left')
canvas.create_text(233, 159, text=patient['gender'], font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey30', anchor=tk.W, justify='left')
canvas.create_text(88, 192, text=patient['case'], font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey30', anchor=tk.NW, justify='left', width=300)
# ------------------------End------------------------


root.mainloop()

