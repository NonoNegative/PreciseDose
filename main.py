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
from datetime import datetime
# -------------------End-------------------

print(colored(" START ", 'light_grey', 'on_dark_grey'), "Execution Timestamp:", colored(datetime.now(), 'dark_grey'))

# ---------------Load Settings------------
with open('settings.json') as my_settings_file:
    settings = json.load(my_settings_file)

# ------------------Theme------------------
colorama_init() # Initialize colorama for pretty printing
selected_color_theme = settings['theme'] # This is where the magic happens
customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
default_themes = {"blue":'#3B8ED0', "green":'#2CC985', "dark-blue":'#3A7EBF'}
if selected_color_theme in default_themes:
    customtkinter.set_default_color_theme(selected_color_theme)  # Default Themes: "blue" (standard), "green", "dark-blue"
    primary_color = default_themes[selected_color_theme] # Primary color of UI
    print(colored(" THEME ", 'white', 'on_magenta'),  f"Sucessfully Loaded: '{selected_color_theme.title()}' from default themes list.")
else:
    customtkinter.set_default_color_theme(f"themes\\{selected_color_theme}.json")  # Custom Themes: "themes\\xyz.json"
    theme_json = json.load(open(f"themes\\{selected_color_theme}.json"))
    primary_color = theme_json['CTkButton']['fg_color'][0] # Primary color of UI
    print(colored(" THEME ", 'light_grey', 'on_magenta'),  f"Sucessfully Loaded: '{selected_color_theme.title()}' from path" , colored(f"'themes\\{selected_color_theme}.json'", 'dark_grey'))
    del theme_json # Why waste memory?
# -------------------End-------------------

#-----------------Load Content-------------

# Load drugs
drug_list = ["Epinephrine", "Vasopressin", "Atropine"]
with open('content\\medicines.json') as file:
    drug_dict = json.load(file)

# Load settings

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
print(colored(" INFO ", 'black', 'on_yellow'),  f"Selected Patient: {patient['name']} [ID: {patient_id}] from path" , colored(f"'content\\patients\\{patient_id}.json'", 'dark_grey'))

# Update Profile
canvas.create_line(150, 65, 387, 65, fill='White', width=1); canvas.create_line(150, 105, 387, 105, fill='White', width=1)
canvas.create_text(152, 71, text=patient['name'], font=('Alte Haas Grotesk', 17, 'bold'), fill='Grey30', anchor=tk.NW)
patient_headshot = customtk.create_tk_image(f"content\\avatars\\{patient_id}.png", 100, 100)
canvas.create_image(30, 66, image=patient_headshot, anchor=tk.NW)
canvas.create_text(205, 126, text=patient['age'], font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey30', anchor=tk.W, justify='left')
canvas.create_text(233, 159, text=patient['gender'], font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey30', anchor=tk.W, justify='left')
canvas.create_text(88, 192, text=patient['case'], font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey30', anchor=tk.NW, justify='left', width=300)
# ------------------------End------------------------

# -----------------Profile and History Buttons-----------------
full_profile_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\full_profile.png"),
                                  dark_image=Image.open("assets\\icons\\full_profile.png"),
                                  size=(80, 80))

medical_records_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\medicaL_records.png"),
                                  dark_image=Image.open("assets\\icons\\medicaL_records.png"),
                                  size=(80, 80))

action_history_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\action_history.png"),
                                  dark_image=Image.open("assets\\icons\\action_history.png"),
                                  size=(80, 80))

full_profile_button = customtkinter.CTkButton(master=canvas, image=full_profile_icon, text='Complete\nDetails', font=('Alte Haas Grotesk', 15, 'bold'), compound=tk.TOP, width=120, height=150, corner_radius=12, bg_color='White', border_color='White')
full_profile_button.place(x=12, y=265)

medical_records_button = customtkinter.CTkButton(master=canvas, image=medical_records_icon, text='Medical\nHistory', font=('Alte Haas Grotesk', 15, 'bold'), compound=tk.TOP, width=120, height=150, corner_radius=12, bg_color='White', border_color='White')
medical_records_button.place(x=145, y=265)

action_history_button = customtkinter.CTkButton(master=canvas, image=action_history_icon, text='Action\nHistory', font=('Alte Haas Grotesk', 15, 'bold'), compound=tk.TOP, width=120, height=150, corner_radius=12, bg_color='White', border_color='White')
action_history_button.place(x=277, y=265)

canvas.create_line(13, 430, 397, 430, fill='#e7e7e7', width=4)
# -----------------------------End-----------------------------

# ---------------------------STT Tab---------------------------
start_recording_button = customtk.create_image_button(root, 'assets\\icons\\start_recording.jpg', 261, 824, 25, 25, bg='#3e3e3e', active_bg='#3e3e3e', disable_btn_press_anim=True)
stop_recording_button = customtk.create_image_button(root, 'assets\\icons\\stop_recording.jpg', 307, 825, 25, 25, bg='#3e3e3e', active_bg='#3e3e3e', disable_btn_press_anim=True)
transcribe_button = customtk.create_image_button(root, 'assets\\icons\\transcript.jpg', 351, 823, 28, 28, bg='#3e3e3e', active_bg='#3e3e3e', disable_btn_press_anim=True)
# -----------------------------End-----------------------------

# --------------------------Drug Tab---------------------------
search_entry = customtkinter.CTkEntry(master=canvas, placeholder_text="Search...", corner_radius=8, width=221, height=32, bg_color='White', font=('Alte Haas Grotesk', 13))
search_entry.place(x=1628, y=101)

search_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\search.png"),
                                  dark_image=Image.open("assets\\icons\\search.png"),
                                  size=(20, 20))

search_button = customtkinter.CTkButton(master=canvas, image=search_icon, text='', width=50, height=33, corner_radius=8, bg_color='White', border_color='White')
search_button.place(x=1854, y=100)

tabview_1 = customtkinter.CTkTabview(master=canvas, width=280, height=240, bg_color='White', corner_radius=7)
tabview_1._segmented_button.configure(font=('Alte Haas Grotesk', 15, 'bold'))
tabview_1.place(x=1628, y=134)
tabview_1.add("All"); tabview_1.add("Search Results")

# Tab 1 ("All")
drug_list_canvas = tk.Canvas(tabview_1.tab("All"), width=252, height=187, highlightthickness=0, background=tabview_1.cget('fg_color')[0])
drug_list_canvas.place(x=0, y=0)
scroll_bar = customtkinter.CTkScrollbar(tabview_1.tab("All"), command=drug_list_canvas.yview, height=195)
drug_list_canvas.config(yscrollcommand=scroll_bar.set)
scroll_bar.place(x=254, y=-4)

def generate_tab_1():
    global drug_list_canvas
    y = 0  # Initial y pos
    for drug in drug_list:
        drug_button = customtkinter.CTkButton(master=drug_list_canvas, text=drug[], font=('Alte Haas Grotesk', 15, 'bold'), width=252, height=33, corner_radius=7, bg_color=tabview_1.cget('fg_color')[0])
        drug_list_canvas.create_window(0, y, window=drug_button, anchor=tk.NW)
        y = y + 38
    root.update()
    drug_list_canvas.configure(scrollregion=drug_list_canvas.bbox("all"))

generate_tab_1()
# -----------------------------End-----------------------------

# ------------------------Calibrate Tab------------------------
calibrate_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\calibrate.png"),
                                  dark_image=Image.open("assets\\icons\\calibrate.png"),
                                  size=(20, 20))

calibrate_button = customtkinter.CTkButton(master=canvas, image=calibrate_icon, text='Run Simulation', compound=tk.LEFT, font=('Alte Haas Grotesk', 15, 'bold'), width=280, height=33, corner_radius=8, bg_color='White', border_color='White')
calibrate_button.place(x=1628, y=548)
# -----------------------------End-----------------------------

# ------------------------Administer Tab-----------------------
combobox_1 = customtkinter.CTkComboBox(canvas, values=["Option 1", "Option 2", "Option 42 long long long..."], width=280, height=33, font=('Alte Haas Grotesk', 14), state='readonly', corner_radius=7)
combobox_1.place(x=1628, y=830); combobox_1.set("Select Type...")
combobox_2 = customtkinter.CTkComboBox(canvas, values=["Option 1", "Option 2", "Option 42 long long long..."], width=280, height=33, font=('Alte Haas Grotesk', 14), state='readonly', corner_radius=7)
combobox_2.place(x=1628, y=874); combobox_2.set("Select Method...")

administer_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\administer.png"),
                                  dark_image=Image.open("assets\\icons\\administer.png"),
                                  size=(20, 20))

administer_button = customtkinter.CTkButton(master=canvas, image=administer_icon, text='Administer Drug', compound=tk.LEFT, font=('Alte Haas Grotesk', 15, 'bold'), width=280, height=33, corner_radius=8, bg_color='White', border_color='White')
administer_button.place(x=1628, y=1036)
# -----------------------------End-----------------------------

root.mainloop()

