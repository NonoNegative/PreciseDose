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
from tkinter import messagebox
from shared.action_history import dll as action_history
import time
import shared.functions as ext_funcs
from RealtimeSTT import AudioToTextRecorder
from ollama import chat
from ollama import ChatResponse
import tkinter.scrolledtext as st 
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

drawer_width = 350; drawer_height = 42
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

eye_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\eye.png"),
                                  dark_image=Image.open("assets\\icons\\eye.png"),
                                  size=(20, 20))

interactive_button = customtkinter.CTkButton(canvas, height=30, corner_radius=10, image = eye_icon ,text='Interactive', compound=tk.LEFT, font=('Alte Haas Grotesk', 15, 'bold'), text_color='White', width=90, fg_color='Grey40', hover_color='Grey30')
interactive_button.place(x=((screen_width)//2)+35, y=5, anchor=tk.NE)

canvas.create_line(((screen_width)//2)+43, 4, ((screen_width)//2)+43, drawer_height-4, fill='#e3e3e3', width=4)
# ------------------------End------------------------

# -----------------Patient Intialize-----------------
patient = random.choice(os.listdir("content\\patients")) # Select a random patient
patient_id = int(patient.rstrip(".json"))
patient = json.load(open(f"content\\patients\\{patient}")) # Parse JSON to Dictionary
parameter_map = patient['parameters']
op_procedure = patient['graph']
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

full_profile_button = customtkinter.CTkButton(master=canvas, image=full_profile_icon, text='Complete\nDetails', font=('Alte Haas Grotesk', 15, 'bold'), compound=tk.TOP, width=120, height=150, corner_radius=12, bg_color='White', border_color='White', command= lambda: ext_funcs.open_pdf('Patient Profile', 'content\\documents\\1_profile.pdf', p_height=1250))
full_profile_button.place(x=12, y=265)

medical_records_button = customtkinter.CTkButton(master=canvas, image=medical_records_icon, text='Medical\nHistory', font=('Alte Haas Grotesk', 15, 'bold'), compound=tk.TOP, width=120, height=150, corner_radius=12, bg_color='White', border_color='White', command= lambda: ext_funcs.open_pdf('Patient History', 'content\\documents\\1_history.pdf'))
medical_records_button.place(x=145, y=265)

action_history_button = customtkinter.CTkButton(master=canvas, image=action_history_icon, text='Action\nHistory', font=('Alte Haas Grotesk', 15, 'bold'), compound=tk.TOP, width=120, height=150, corner_radius=12, bg_color='White', border_color='White', command=lambda: ext_funcs.show_action_history(op_procedure))
action_history_button.place(x=277, y=265)

canvas.create_line(13, 430, 397, 430, fill='#e7e7e7', width=4)
# -----------------------------End-----------------------------

# ----------------------Captured Parameters--------------------
button_list = []

def update_parameters(start_x=23, start_y=580, row_spacing=13, padding=5, max_width=391):

    global button_list

    for i in button_list:
        i.destroy()

    x, y = start_x, start_y 
    button_height = 20 
    
    for key, value in parameter_map.items():
        
        if value == 0 or value == '' or value == None:
            continue

        # Create a segmented button with key and value as options
        element = customtkinter.CTkSegmentedButton(
            master=canvas,
            values=[f' {key} ', f' {value} '],
            font=('Alte Haas Grotesk', 14, 'bold'),
            corner_radius=7,
            height=button_height
        )
        element.set(f' {key} ')
        
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
        border_width=0,
        command= lambda: ext_funcs.add_parameter(parameter_map, update_parameters)
    )

    add_button.place(x=x, y=y, anchor='nw')
    button_list.append(add_button)
    
    return button_list

def clear_parameters():
    global parameter_map
    parameter_map = {
        "Age": 0,
        "Gender": 0,
        "Height": 0,
        "Weight": 0,
        "BMI": 0,
        "Heartrate": 0,
        "SPO2": 0,
        "Blood Pressure": 0,
        "Temperature": 0 
    }
    update_parameters()

json_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\json.png"),
                                  dark_image=Image.open("assets\\icons\\json.png"),
                                  size=(20, 20))

json_button = customtkinter.CTkButton(master=canvas, image=json_icon, text='Edit Raw Hashmap', compound=tk.LEFT, font=('Alte Haas Grotesk', 15, 'bold'), width=385, height=33, corner_radius=8, bg_color='White', border_color='White')
json_button.place(x=12, y=486)

delete_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\delete.png"),
                                  dark_image=Image.open("assets\\icons\\delete.png"),
                                  size=(20, 20))

delete_button = customtkinter.CTkButton(master=canvas, image=delete_icon, text='Clear All Elements', compound=tk.LEFT, font=('Alte Haas Grotesk', 15, 'bold'), width=385, height=33, corner_radius=8, bg_color='White', border_color='White', command= lambda: clear_parameters() if messagebox.askyesno('Clear all parameters', 'Are you sure you want to clear all parameters?') == True else None)
delete_button.place(x=12, y=526)

update_parameters()
# -----------------------------End-----------------------------

# ---------------------------STT Tab---------------------------
previous = []
recorder = AudioToTextRecorder()

ini_prompt = '''
Can you extract the essential information from this text and return it in a JSON format. Take key features and return with the format, for example:

"parameters": {
    "Age": 0,
    "Gender": 0,
    "Height": 0,
    "Weight": 0,
    "BMI": 0,
    "Heartrate": 0,
    "SPO2": 0,
    "Blood Pressure": 0,
    "Temperature": 0,
    "Respiratory Rate": 0
}

If there are no key features in the text at all, just say 'No features detected in input'. Make sure also include text features like the current state of the patient. If a specific parameter is not mentioned, let it be 0, regardless of what parameter it is.
The messages below would be your task. Just return the JSON format, and nothing else.
'''

response: ChatResponse = chat(model='llama3.2', messages=[
        {
            'role': 'user',
            'content': ini_prompt,
        },
        ])
print(response['message']['content'])

def ollama_chat():
    if previous != []:
        response: ChatResponse = chat(model='llama3.2', messages=[
        {
            'role': 'user',
            'content': ini_prompt + previous[len(previous)-1],
        },
        ])
        option_toplevel = tk.Toplevel()
        option_toplevel.title("Response")
        option_toplevel.config(bg="Grey20")
        screen_width = option_toplevel.winfo_screenwidth(); screen_height = option_toplevel.winfo_screenheight()
        width = 372; height = 300
        x = screen_width / 2 - width / 2; y = screen_height / 2 - height / 2
        option_toplevel.geometry('%dx%d+%d+%d' % (width, height, x, y))
        option_toplevel.resizable(False, False)
        tk.Label(option_toplevel, text="Response:", font=('Alte Haas Grotesk', 14, 'bold'), bg="Grey20", fg='White', justify='center').grid(column = 0, row = 0)
        text_area = st.ScrolledText(option_toplevel, 
                        width = 30,  
                        height = 8,  
                        font = ("Cascadia Code", 14)) 
        text_area.grid(column = 0, pady = 10, padx = 10) 
        text_area.insert(tk.INSERT, response['message']['content'].replace(', ', ',\n'))
        text_area.configure(state ='disabled') 

def start_recording():
    recorder.start()
    canvas.delete('stt')
    canvas.create_text(30, 883, text="Speak now...", tags='stt', anchor=tk.NW, font=('Alte Haas Grotesk', 14, 'bold'), fill='Grey25')

def print_to_output():
    global previous
    canvas.delete('stt')
    canvas.create_text(30, 883, text="Transcribing...", tags='stt', anchor=tk.NW, font=('HAlte Haas Grotesk', 14, 'bold'), fill='Grey25')
    transcription = recorder.text()
    previous.append(transcription)
    canvas.delete('stt')
    canvas.create_text(30, 883, text=transcription, tags='stt', width=354, anchor=tk.NW, font=('Alte Haas Grotesk', 14, 'bold'), fill='Grey20')

start_recording_button = customtk.create_image_button(root, 'assets\\icons\\start_recording.jpg', 261, 824, 25, 25, bg='#3e3e3e', active_bg='#3e3e3e', disable_btn_press_anim=True, command=start_recording)
stop_recording_button = customtk.create_image_button(root, 'assets\\icons\\stop_recording.jpg', 307, 825, 25, 25, bg='#3e3e3e', active_bg='#3e3e3e', disable_btn_press_anim=True, command=print_to_output)
transcribe_button = customtk.create_image_button(root, 'assets\\icons\\transcript.jpg', 351, 823, 28, 28, bg='#3e3e3e', active_bg='#3e3e3e', disable_btn_press_anim=True, command=ollama_chat)
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

none_tk_image = customtk.create_tk_image('assets\\icons\\none.png', 80, 80)

drug_image = tk.Label(canvas, background='White', fg='White', borderwidth=0, image=none_tk_image)
drug_image.place(x=1642, y=449, anchor=tk.NW)

def update_calibrate_tab(drug):
    global drug_tk_image
    drug_tk_image = customtk.create_tk_image(f'content\\medicines\\{drug}.png', 80, 80)
    drug_image.config(image=drug_tk_image)
    drug_name_label.configure(text=drug)
    drug_desc_label.configure(text=drug_dict[drug]['description'])
# -----------------------------End-----------------------------

# ----------------------Simulation Results---------------------
canvas.create_text(1766, 693, text='None yet.', font=('Alte Haas Grotesk', 12), anchor=tk.CENTER, fill='Grey50', tags='Sim')
# -----------------------------End-----------------------------

# ------------------------Administer Tab-----------------------

administer_methods = settings['administer_methods']

def update_cb_2(route):
    combobox_2.set("Select Method...")
    combobox_2.configure(values=administer_methods[route])

combobox_1 = customtkinter.CTkComboBox(canvas, values=["Enteral Route", "Parenteral Route", "Topical Route"], width=280, height=33, font=('Alte Haas Grotesk', 14), state='readonly', corner_radius=7, command=update_cb_2)
combobox_1.place(x=1628, y=830); combobox_1.set("Select Route...")
combobox_2 = customtkinter.CTkComboBox(canvas, values=[], width=280, height=33, font=('Alte Haas Grotesk', 14), state='readonly', corner_radius=7)
combobox_2.place(x=1628, y=874); combobox_2.set("Select Method...")

administer_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\administer.png"),
                                  dark_image=Image.open("assets\\icons\\administer.png"),
                                  size=(20, 20))

administer_button = customtkinter.CTkButton(master=canvas, image=administer_icon, text='Administer Drug', compound=tk.LEFT, font=('Alte Haas Grotesk', 15, 'bold'), width=280, height=33, corner_radius=8, bg_color='White', border_color='White')
administer_button.place(x=1628, y=1036)
# -----------------------------End-----------------------------

# ---------------------------Effects---------------------------
canvas.create_text(1766, 993, text='None yet.', font=('Alte Haas Grotesk', 12), anchor=tk.CENTER, fill='Grey50', tags='Sim')
# -----------------------------End-----------------------------

# --------------------------Interactive------------------------
pointers = customtk.create_tk_image('assets\\static\\pointers.png', 1920, 1080)
canvas.create_image(0, 0, image=pointers, anchor=tk.NW, tags='interactive')

defib = customtkinter.CTkButton(canvas, corner_radius=0, text='Attach Defibrilator', font=('Alte Haas Grotesk', 14, 'bold'), fg_color='White', hover_color='#e3e3e3', text_color='Grey30', bg_color='Black', border_width=2, border_color='Grey50', width=170, command= lambda: action_history.append(['Defibrilator shocked', '10 kJ']))
defib.place(x=1402, y=723, anchor=tk.N)

iv = customtkinter.CTkButton(canvas, corner_radius=0, text='IV Status', font=('Alte Haas Grotesk', 14, 'bold'), fg_color='White', hover_color='#e3e3e3', text_color='Grey30', bg_color='Black', border_width=2, border_color='Grey50', width=100, command= lambda: action_history.append(['Checked IV status']))
iv.place(x=1483, y=361, anchor=tk.W)

cpr = customtkinter.CTkButton(canvas, corner_radius=0, text='CPR', font=('Alte Haas Grotesk', 14, 'bold'), fg_color='White', hover_color='#e3e3e3', text_color='Grey30', bg_color='Black', border_width=2, border_color='Grey50', width=70, command= lambda: action_history.append(['Administered CPR', '2 mins']))
cpr.place(x=1228, y=547, anchor=tk.W)

vitals = customtkinter.CTkButton(canvas, corner_radius=0, text='Check Vitals', font=('Alte Haas Grotesk', 14, 'bold'), fg_color='White', hover_color='#e3e3e3', text_color='Grey30', bg_color='Black', border_width=2, border_color='Grey50', width=140, command= lambda: ext_funcs.check_vitals(parameter_map))
vitals.place(x=857, y=451, anchor=tk.E)

show_interactive = True

def show_hide_interactive():
    global show_interactive
    if show_interactive == True:
        canvas.delete('interactive')
        for i in [defib, iv, cpr, vitals]:
            i.place_forget()
        show_interactive = False
    else:
        canvas.create_image(0, 0, image=pointers, anchor=tk.NW, tags='interactive')
        defib.place(x=1402, y=723, anchor=tk.N)
        iv.place(x=1483, y=361, anchor=tk.W)
        cpr.place(x=1228, y=547, anchor=tk.W)
        vitals.place(x=857, y=451, anchor=tk.E)
        show_interactive = True

show_hide_interactive()
interactive_button.configure(command = show_hide_interactive)

generate_tab_1()
root.mainloop()