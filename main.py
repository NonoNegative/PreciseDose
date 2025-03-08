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
from functools import partial
import time
import shared.functions as ext_funcs
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
drug_list = settings["drugs"]
with open('content\\medicines\\medicines.json') as file:
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

drawer_width = 200; drawer_height = 40
drawer_edge_1 = customtk.create_tk_image("assets\\icons\\drawer.png", drawer_height, drawer_height)
drawer_edge_2 = customtk.create_tk_image("assets\\icons\\drawer.png", drawer_height, drawer_height, flip=1)
canvas.create_rectangle((screen_width-drawer_width)//2, 0, (screen_width+drawer_width)//2, drawer_height, fill='#f3f3f3', width=0)
canvas.create_image((screen_width-drawer_width)//2, 0 ,anchor=tk.NE, image=drawer_edge_1)
canvas.create_image((screen_width+drawer_width)//2, 0 ,anchor=tk.NW, image=drawer_edge_2)

time_limit = settings['time_limit']
time_elapsed = 0

def update_timer():
    global time_elapsed
    time_elapsed += 1
    ScoreL.configure(text='🕑 '+time.strftime('%M:%S', time.gmtime(time_elapsed)))
    if time_elapsed < time_limit:
        # schedule next update 1 second later
        canvas.after(1000, update_timer)

ScoreL = tk.Label(canvas, text='🕑 '+time.strftime('%M:%S', time.gmtime(time_elapsed)), bg='#f3f3f3', fg='Grey30', font=("Alte Haas Grotesk", 15, 'bold'), justify='left')
ScoreL.place(x=((screen_width-drawer_width)//2) - 12, y=5, anchor=tk.NW)
canvas.after(1000, update_timer)
finish_button = customtkinter.CTkButton(canvas, height=30, corner_radius=10, text='Finish', font=('Alte Haas Grotesk', 15, 'bold'), text_color='White', width=70)
finish_button.place(x=((screen_width+drawer_width)//2)+12, y=5, anchor=tk.NE)
halt_button = customtkinter.CTkButton(canvas, height=30, corner_radius=10, text='Halt', font=('Alte Haas Grotesk', 15, 'bold'), text_color='White', width=60, fg_color='IndianRed2', hover_color='IndianRed4')
halt_button.place(x=((screen_width+drawer_width)//2)-63, y=5, anchor=tk.NE)

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

full_profile_button = customtkinter.CTkButton(master=canvas, image=full_profile_icon, text='Complete\nDetails', font=('Alte Haas Grotesk', 15, 'bold'), compound=tk.TOP, width=120, height=150, corner_radius=12, bg_color='White', border_color='White', command= lambda: ext_funcs.open_pdf('Patient Profile', 'content\\documents\\1_profile.pdf'))
full_profile_button.place(x=12, y=265)

medical_records_button = customtkinter.CTkButton(master=canvas, image=medical_records_icon, text='Medical\nHistory', font=('Alte Haas Grotesk', 15, 'bold'), compound=tk.TOP, width=120, height=150, corner_radius=12, bg_color='White', border_color='White')
medical_records_button.place(x=145, y=265)

action_history_button = customtkinter.CTkButton(master=canvas, image=action_history_icon, text='Action\nHistory', font=('Alte Haas Grotesk', 15, 'bold'), compound=tk.TOP, width=120, height=150, corner_radius=12, bg_color='White', border_color='White')
action_history_button.place(x=277, y=265)

canvas.create_line(13, 430, 397, 430, fill='#e7e7e7', width=4)
# -----------------------------End-----------------------------

# ----------------------Captured Parameters--------------------
json_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\json.png"),
                                  dark_image=Image.open("assets\\icons\\json.png"),
                                  size=(20, 20))

json_button = customtkinter.CTkButton(master=canvas, image=json_icon, text='Edit Raw Hashmap', compound=tk.LEFT, font=('Alte Haas Grotesk', 15, 'bold'), width=385, height=33, corner_radius=8, bg_color='White', border_color='White')
json_button.place(x=12, y=486)

delete_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\delete.png"),
                                  dark_image=Image.open("assets\\icons\\delete.png"),
                                  size=(20, 20))

delete_button = customtkinter.CTkButton(master=canvas, image=delete_icon, text='Clear All Elements', compound=tk.LEFT, font=('Alte Haas Grotesk', 15, 'bold'), width=385, height=33, corner_radius=8, bg_color='White', border_color='White')
delete_button.place(x=12, y=526)

parameters = {
    'age': 20,
    'height': 180,
    'gender': 'Male',
    'heartrate': 60,
    'blood pressure': '120/60'
}

def update_parameters(canvas, parameters, start_x=23, start_y=580, row_spacing=13, padding=5, max_width=391):
    x, y = start_x, start_y 
    button_height = 20 
    button_list = [] 
    
    for key, value in parameters.items():
        # Create a segmented button with key and value as options
        element = customtkinter.CTkSegmentedButton(
            master=canvas,
            values=[f' {key.title()} ', f' {value} '],
            font=('Alte Haas Grotesk', 14, 'bold'),
            corner_radius=7,
            height=button_height
        )
        element.set(f' {key.title()} ')
        
        # Measure button width
        canvas.update_idletasks()
        button_width = element.winfo_reqwidth()
        
        # If the next button exceeds max_width, move to the next row
        if x + button_width > max_width:
            x = start_x 
            y += button_height + row_spacing

        element.place(x=x, y=y, anchor='nw')
        button_list.append(element)
        
        # Update x position for next button
        x += button_width + padding

    add_button = customtkinter.CTkButton(
        master=canvas,
        text='+',
        font=('Alte Haas Grotesk', 18, 'bold'),
        width=28, height=28,
        corner_radius=7,
        bg_color='#e7e7e7',
        border_color='#e7e7e7',
        border_spacing=0,
        border_width=0
    )

    add_button.place(x=x, y=y, anchor='nw')
    
    return button_list

update_parameters(canvas, parameters)
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
        drug_button = customtkinter.CTkButton(master=drug_list_canvas, text=drug, font=('Alte Haas Grotesk', 15, 'bold'), width=252, height=33, corner_radius=7, bg_color=tabview_1.cget('fg_color')[0], command=partial(update_calibrate_tab, drug))
        drug_list_canvas.create_window(0, y, window=drug_button, anchor=tk.NW)
        y = y + 38
    root.update()
    drug_list_canvas.configure(scrollregion=drug_list_canvas.bbox("all"))

# -----------------------------End-----------------------------

# ------------------------Calibrate Tab------------------------
calibrate_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\calibrate.png"),
                                  dark_image=Image.open("assets\\icons\\calibrate.png"),
                                  size=(20, 20))

calibrate_button = customtkinter.CTkButton(master=canvas, image=calibrate_icon, text='Run Simulation', compound=tk.LEFT, font=('Alte Haas Grotesk', 15, 'bold'), width=280, height=33, corner_radius=8, bg_color='White', border_color='White')
calibrate_button.place(x=1628, y=548)

drug_name_label = customtkinter.CTkLabel(master=canvas, text="None", font=('Alte Haas Grotesk', 12, 'bold'), width=162, height=23, corner_radius=6, bg_color='White', fg_color="#e7e7e7", text_color='Grey25')
drug_name_label.place(x=1745, y=437, anchor=tk.NW)

drug_desc_label = customtkinter.CTkLabel(master=canvas, text="Select a drug to view its description.", font=('Alte Haas Grotesk', 12), width=160, height=74, bg_color='White', fg_color="White", wraplength=162, justify='left', anchor=tk.NW, text_color='Grey20')
drug_desc_label.place(x=1747, y=464, anchor=tk.NW)

def update_calibrate_tab(drug):
    drug_name_label.configure(text=drug)
    drug_desc_label.configure(text=drug_dict[drug]['description'])
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

generate_tab_1()
root.mainloop()

