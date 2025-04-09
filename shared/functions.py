import customtkinter
import shared.customtk as customtk
import tkinter as tk
from shared.tkgif import GifLabel
from datetime import datetime
from shared.CTkPDFViewer import *
from tkinter import messagebox
from shared.action_history import dll as action_history
from shared.onnx_predict import predict_dosage

def create_top_level(title, width=600, height=600, load_captions=['Loading', 2000], bg_color='#f0f0f0'):
    image_toplevel = tk.Toplevel(); image_toplevel.wm_attributes('-toolwindow', 'true')
    image_toplevel.title(title)
    image_toplevel.config(bg=bg_color)
    screen_width = image_toplevel.winfo_screenwidth(); screen_height = image_toplevel.winfo_screenheight()
    x = screen_width / 2 - width / 2; y = screen_height / 2 - height / 2
    image_toplevel.geometry('%dx%d+%d+%d' % (width, height, x, y))
    image_toplevel.resizable(False, False)
    image_toplevel.attributes('-topmost', True)

    if load_captions != None:
        gif_label = GifLabel(image_toplevel, bd=0)
        gif_label.place(x=width/2, y=(height/2)-40, anchor=tk.CENTER)
        gif_label.load("assets\\icons\\loading.gif")
        load_caption = tk.Label(image_toplevel, text='', font=('Alte Haas Grotesk', 14), bg='#f0f0f0', fg='grey30', borderwidth=0)
        load_caption.place(x=width/2, y=(height/2)+55, anchor=tk.CENTER)

        def update_label(index=0):
            if index < len(load_captions):
                load_caption.config(text=load_captions[index])
                delay = load_captions[index + 1]
                load_caption.after(delay, update_label, index + 2)
            else:
                for widget in image_toplevel.winfo_children():
                    widget.destroy()
                image_toplevel.canvas = tk.Canvas(image_toplevel, width=width, height=height, highlightthickness=0)
                image_toplevel.canvas.place(x=0, y=0)
                image_toplevel.quit()

        update_label()
        image_toplevel.mainloop() 

    return image_toplevel

font=('Alte Haas Grotesk', 12)
def get_label_height(text, width):
    root = tk.Tk() 
    root.withdraw()  

    label = tk.Label(root, text=text, font=font, wraplength=width)
    label.update_idletasks()
    height = label.winfo_reqheight() 
    label.destroy()
    root.destroy()

    return height

def infer_image(img_path, window_name, size_x=None, size_y=None, attached_note="No further info was attached with this image.", load_captions=['Please Wait...', 500, 'Retrieving Image...', 2000, 'Processing...', 1000]):
    my_image = customtk.create_tk_image(img_path, size_x, size_y)
    width = my_image.width(); height = my_image.height()
    dynamic_note_ht = get_label_height(attached_note, width=width-20)
    note_button_height = 30; entry_height = 40; buttons_height = 30; padding = 50
    extra_height = note_button_height + dynamic_note_ht + entry_height + buttons_height + padding
    my_top = create_top_level('Vitals Check', my_image.width() if size_x == None else size_x, my_image.height() + extra_height if size_y == None else size_y + extra_height, load_captions)
    my_top.canvas.create_image(0, 0, anchor=tk.NW, image=my_image)
    my_top.canvas.image = my_image
    my_top.canvas.create_line(10, height+20, width-15, height+20, fill='#e3e3e3', width=4)
    note_button = customtkinter.CTkButton(my_top, height=20, corner_radius=7, text='Attached Note', font=('Alte Haas Grotesk', 15, 'bold'), text_color='White')
    note_button.place(x=width/2, y=height+20, anchor=tk.CENTER)
    note_label = tk.Label(master=my_top, text=attached_note, fg='Grey40', bg='#f0f0f0', font=font, wraplength=width-20, justify='center')
    note_label.place(x=width/2, y=height+35, anchor=tk.N)
    my_top.canvas.create_line(10, height+note_button_height+dynamic_note_ht+15, width-15, height+note_button_height+dynamic_note_ht+15, fill='#e3e3e3', width=4)
    height = height+note_button_height+dynamic_note_ht+30
    inference_entry = customtkinter.CTkEntry(master=my_top.canvas, placeholder_text=" Do you infer anything from this result?", corner_radius=8, width=width-20, height=entry_height, bg_color='White', font=('Alte Haas Grotesk', 15, 'bold'), text_color='Grey25', placeholder_text_color='Grey50')
    inference_entry.place(x=10, y=height, anchor=tk.NW)
    save_button = customtkinter.CTkButton(my_top, height=30, corner_radius=6, text='Save', font=('Alte Haas Grotesk', 15, 'bold'), text_color='White', width=100)
    save_button.place(x=width-10, y=height+entry_height+10, anchor=tk.NE)
    discard_button = customtkinter.CTkButton(my_top, height=30, corner_radius=6, text='Discard', font=('Alte Haas Grotesk', 15, 'bold'), text_color='White', width=100, fg_color='IndianRed2', hover_color='IndianRed4')
    discard_button.place(x=width-120, y=height+entry_height+10, anchor=tk.NE)
    my_top.canvas.create_text(12, height+entry_height+40, text="Timestamp: "+ str(datetime.now()), font=('Cascadia Code', 10), fill='Grey60', anchor=tk.SW)

def open_pdf(title, location, p_width=1000, p_height=1414):
    my_top = create_top_level(title, 1000, 900, load_captions=['Reading Document...', 1000, 'Opening in Viewer...', 400])
    pdf_frame = CTkPDFViewer(my_top, file=location, page_width=p_width, page_height=p_height)
    pdf_frame.pack(fill="both", expand=True, padx=10, pady=10)
    my_top.mainloop()

def add_parameter(parameter_map, update_fn):
    my_top = create_top_level('Add New Parameter', 400, 205, load_captions=['Please wait...', 200])
    my_top.canvas.create_text(200, 30, text='Add New Parameter', font=('Century Gothic', 17, 'bold'), fill='Grey40')
    my_top.canvas.create_line(10, 60, 390, 60, fill='#3B8ED0', width=4)
    my_top.canvas.create_text(190, 90, text='Choose Parameter :', font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey50', anchor=tk.E)
    my_top.canvas.create_text(190, 125, text='Enter Value :', font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey50', anchor=tk.E)
    my_top.canvas.create_line(10, 150, 390, 150, fill='#3B8ED0', width=4)

    combobox_1 = customtkinter.CTkComboBox(
        my_top.canvas, values=["Age", "Gender", "Height", "Weight", "BMI", "Heartrate", "SPO2", "Blood Pressure", "Temperature"],
        width=160, height=25, font=('Alte Haas Grotesk', 12), state='readonly', corner_radius=7
    )
    combobox_1.place(x=200, y=90, anchor=tk.W)
    combobox_1.set("Select...")

    val_entry = customtkinter.CTkEntry(
        master=my_top.canvas, placeholder_text="Nil", corner_radius=7, width=160, height=25,
        bg_color='White', font=('Alte Haas Grotesk', 12)
    )
    val_entry.place(x=200, y=125, anchor=tk.W)

    def save():
        p = combobox_1.get()
        v = val_entry.get()
        if p != "Select..." and p and v:
            parameter_map[p] = v
            print(parameter_map)
            update_fn() 
        else:
            my_top.attributes('-topmost', False)
            messagebox.showerror('Error!', 'Invalid or incomplete parameter/value passed!')
            my_top.attributes('-topmost', True)
            return None
        my_top.destroy()

    save_button = customtkinter.CTkButton(
        my_top, height=30, corner_radius=6, text='Save', font=('Alte Haas Grotesk', 15, 'bold'),
        text_color='White', width=100, command=save
    )
    save_button.place(x=390, y=165, anchor=tk.NE)

    discard_button = customtkinter.CTkButton(
        my_top, height=30, corner_radius=6, text='Close', font=('Alte Haas Grotesk', 15, 'bold'),
        text_color='White', width=100, fg_color='IndianRed2', hover_color='IndianRed4',
        command=my_top.destroy  # Use `command` instead of `function`
    )
    discard_button.place(x=280, y=165, anchor=tk.NE)

def check_vitals(vitals):
    action_history.append(['Checked Vitals', str(datetime.now())])
    my_top = create_top_level('Vitals Check', 600, 600, ['Please Wait...', 500, 'Checking Body Vitals...', 2000, 'Processing...', 1000])
    vitals_overlay = customtk.create_tk_image('assets\\static\\vitals_overlay.png', 600, 600)
    my_top.canvas.create_image(0, 0, anchor=tk.NW, image=vitals_overlay)
    my_top.canvas.image = vitals_overlay
    pos_dict = {"Temperature":[280, 254, ' \u00b0C'], "Heartrate":[746, 254, ' BPM'], "SPO2":[277, 545, '%'], "Blood Pressure":[746, 545, ''], "Respiratory Rate":[272, 834, ' Breaths/Min']}
    for key, (x, y, z) in pos_dict.items():
        value = vitals.get(key, "N/A")
        my_top.canvas.create_text(x*0.6, y*0.6, text=str(value)+z, font=('Alte Haas Grotesk', 12, 'bold'), fill='grey30', anchor='nw')

def show_action_history(op_procedure):
    my_top = create_top_level('Action History', 1000, 950, load_captions=['Loading...', 500])
    tabview_1 = customtkinter.CTkTabview(master=my_top.canvas, width=960, height=930, bg_color='#f0f0f0', corner_radius=7)
    tabview_1._segmented_button.configure(font=('Alte Haas Grotesk', 15, 'bold'))
    tabview_1.place(x=20, y=0)
    tabview_1.add("Your Action History"); tabview_1.add("Operational Procedure")

    tab_1_canvas = tk.Canvas(tabview_1.tab("Your Action History"), width=960, height=930, highlightthickness=0, background=tabview_1.cget('fg_color')[0])
    tab_1_canvas.place(x=0, y=0)
    scroll_bar = customtkinter.CTkScrollbar(tabview_1.tab("Your Action History"), command=tab_1_canvas.yview, height=880)
    tab_1_canvas.config(yscrollcommand=scroll_bar.set)
    scroll_bar.place(x=930, y=-4)

    # Visualization of the linked list
    y_position = 40  # Initial Y position
    x_position = 470  # X position for buttons
    node = action_history.head  # Start from the head of the linked list

    tab_1_canvas.create_line(500, 0, 500, 40, width=4, fill=tabview_1.cget('fg_color')[0])

    while node:
        values = node.data  # Extract list from linked list node
        if values:
            element = customtkinter.CTkSegmentedButton(
                master=tab_1_canvas,
                values=values,
                font=('Alte Haas Grotesk', 14, 'bold'),
                corner_radius=7,
                height=40,
                state=tk.DISABLED,
                text_color_disabled='White',
                selected_color='Indianred2'
            )
            element.set(values[0])  # Set first element as selected value
            tab_1_canvas.create_window(x_position, y_position, window=element, anchor=tk.CENTER)
            
            # Draw an arrow to the next node
            if node.next:
                tab_1_canvas.create_line(
                    x_position, y_position + 20,  # Start of the arrow (right side of the button)
                    x_position, y_position + 80,  # Middle point of the arrow
                    arrow=tk.LAST, fill="black", width=4
                )
            
            y_position += 100  # Move down for the next element
        
        node = node.next  # Move to the next node

    tab_1_canvas.create_line(500, y_position, 500, y_position+10, width=4, fill=tabview_1.cget('fg_color')[0])
    
    my_top.update()
    tab_1_canvas.configure(scrollregion=tab_1_canvas.bbox("all"))

    tab_2_canvas = tk.Canvas(tabview_1.tab("Operational Procedure"), width=960, height=930, highlightthickness=0, background=tabview_1.cget('fg_color')[0])
    tab_2_canvas.place(x=0, y=0)
    scroll_bar_2 = customtkinter.CTkScrollbar(tabview_1.tab("Operational Procedure"), command=tab_2_canvas.yview, height=880)
    tab_2_canvas.config(yscrollcommand=scroll_bar_2.set)
    scroll_bar_2.place(x=930, y=-4)

    def draw_operational_procedure(canvas):
        node_width, node_height = 180, 60

        def draw_node(text, position, color):
            x, y = position
            width, height = node_width, node_height
            canvas.create_rectangle(x - width // 2, y - height // 2, x + width // 2, y + height // 2, fill=color, outline="black")
            canvas.create_text(x, y, text=text, font=("Arial", 8, "bold"), width=width - 10)

        def draw_edge(start, end, decision_text):
            x1, y1 = start
            x2, y2 = end
            dx, dy = x2 - x1, y2 - y1

            length = (dx**2 + dy**2) ** 0.5
            if length == 0:
                return

            ux, uy = dx / length, dy / length
            start_x = x1 + ux * (node_width // 2 + 5)
            start_y = y1 + uy * (node_height // 2 + 5)
            end_x = x2 - ux * (node_width // 2 + 5)
            end_y = y2 - uy * (node_height // 2 + 5)

            canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.LAST, width=2)

            if decision_text:
                circle_x, circle_y = (start_x + end_x) / 2, (start_y + end_y) / 2
                radius = 12
                canvas.create_oval(circle_x - radius, circle_y - radius, circle_x + radius, circle_y + radius, fill="lightgrey", outline="black")
                canvas.create_text(circle_x, circle_y, text=decision_text, font=("Arial", 8, "bold"))

        graph = op_procedure

        for node, data in graph.items():
            for next_node, decision_text in data["next"]:
                draw_edge(data["pos"], graph[next_node]["pos"], decision_text)

        for node, data in graph.items():
            draw_node(data["text"], data["pos"], data["color"])

        canvas.create_line(0, 0, 0, -1, width=0)  # Top padding
        canvas.create_line(0, 1040, 0, 1041, width=0)  # Bottom padding

        canvas.configure(scrollregion=canvas.bbox("all"))

    draw_operational_procedure(tab_2_canvas)

def temp_untop(win, func):
    win.attributes('-topmost', False)
    if func() == True:
        win.attributes('-topmost', True)
        return True
    win.attributes('-topmost', True)

def run_simulation(parameter_map, drug, params, root_canvas, onnx):

    if onnx == None:
        return None
    elif  onnx[0] == None or onnx[1] == None:
        return None

    global sim_static
    my_top = create_top_level('Calibration Results', 600, 525, ["Calibrating...", 500])
    sim_static = customtk.create_tk_image('assets\\static\sim_static.png', 600, 600)
    my_top.canvas.create_image(0, 0, image=sim_static, anchor=tk.NW)
    start_x=30; start_y=60; row_spacing=13; padding=5; max_width=570
    x, y = start_x, start_y 
    button_height = 20
    found = 0
    print(f"{drug} parameters: {params}")
    my_input = [0, 0, 0, 0, 0, 0]
    for key, value in parameter_map.items():
            found = found + 1
            # Create a segmented button with key and value as options
            element = customtkinter.CTkSegmentedButton(
                master=my_top.canvas,
                values=[f' {key} ', f' {value} '],
                font=('Alte Haas Grotesk', 14, 'bold'),
                corner_radius=7,
                height=button_height
            )

            if value == 0 or value == '' or value == None:
                element.configure(values=[f' {key} ', 'Undef.'], selected_color='IndianRed3')
                found = found - 1
            else:
                try:
                    if key == 'Gender':
                        if value == 'Female':
                            my_input[0] = 1 
                        else:
                            my_input[0] = 0
                    elif key == 'Age':
                        my_input[1] = float(value)
                    elif key == 'Blood Pressure':
                        bp = value.split('/')
                        my_input[2] = float(bp[0])
                        my_input[3] = float(bp[1])
                    elif key == 'BMI':
                        my_input[4] = float(value)
                    elif key == 'Temperature':
                        my_input[5] = float(value)
                    elif key == 'SPO2':
                        my_input[6] = float(value)
                except Exception:
                    pass
                    
            element.set(f' {key} ')
            
            # Measure button width
            my_top.canvas.update_idletasks()
            button_width = element.winfo_reqwidth()
            
            # If the next button exceeds max_width, move to the next row
            if x + button_width > max_width:
                x = start_x 
                y += button_height + row_spacing
 
            element.place(x=x, y=y, anchor='nw')
            # Update x position for next button
            x += button_width + padding

    my_top.canvas.create_text(30, 20, text=f'Found {found} parameters.', fill='Grey30', font=('Alte Haas Grotesk', 15, 'bold'), anchor=tk.NW)
    my_top.canvas.create_text(30, 195, text=f"{drug}: Clearance rate, Dosing Interval & Bioavailability", fill='Grey30', font=('Alte Haas Grotesk', 12, 'bold'), anchor=tk.NW)

    x=30; y=230
    for key, value in params.items():
            found = found + 1
            # Create a segmented button with key and value as options
            element = customtkinter.CTkSegmentedButton(
                master=my_top.canvas,
                values=[f'   {key}   ', f' {value} '],
                font=('Alte Haas Grotesk', 14, 'bold'),
                corner_radius=7,
                height=button_height+20,
                selected_color='IndianRed2'
            )
            element.set(f'   {key}   ')
            my_top.canvas.update_idletasks()
            button_width = element.winfo_reqwidth()
            element.place(x=x, y=y, anchor='nw')
            # Update x position for next button
            x += button_width + padding

    #def save_results():
    predicted = 0.0
    if my_input != [0, 0, 0, 0, 0, 0, 0]:
        predicted = float(predict_dosage(my_input, onnx[0]))
    calibrated = abs( ( predicted * params['CL'] * params['tau'] ) / params['F'])
    my_top.canvas.create_text(378, 369, text=f"{predicted} {onnx[1]}", font=('Alte Haas Grotesk', 14, 'bold'), fill='Grey40', anchor=tk.CENTER)
    my_top.canvas.create_text(378, 419, text=f"{calibrated} {onnx[1]}", font=('Alte Haas Grotesk', 14, 'bold'), fill='Grey40', anchor=tk.CENTER)

    def save():
        action_history.append([drug, f"Predicted dosage: {round(predicted, 3)} mL"])
        action_history.append([drug, f"Calibrated dosage: {round(calibrated, 3)} mL"])
        root_canvas.delete('Sim_results')
        root_canvas.create_text(1643, 649, text=f'{drug}: {params}\n\nPredicted Dosage: {round(predicted, 3)} mL\nCalibrated Dosage: {round(calibrated, 3)} mL', tags='Sim_results', font=('Alte Haas Grotesk', 11, 'bold'), anchor=tk.NW, width=255, fill='Grey35')
        my_top.destroy()

    save_button = customtkinter.CTkButton(my_top, height=30, corner_radius=6, text='Save', font=('Alte Haas Grotesk', 15, 'bold'), text_color='White', width=100, command=save)
    save_button.place(x=575, y=480, anchor=tk.NE)
    discard_button = customtkinter.CTkButton(my_top, height=30, corner_radius=6, text='Discard', font=('Alte Haas Grotesk', 15, 'bold'), text_color='White', width=100, fg_color='IndianRed2', hover_color='IndianRed4', command = lambda: my_top.destroy() if temp_untop(my_top, lambda: messagebox.askyesno("Discard changes?", "Are you sure you want to discard your changes?")) else None)
    discard_button.place(x=465, y=480, anchor=tk.NE)

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def check_and_save_cpr(my_top, comp_rate, depth):
    global cpr_yet
    my_top.destroy()
    if comp_rate == 'Select...' or depth.strip() == '' or not isfloat(depth):
        messagebox.showerror("Error!", "Invalid or empty parameters passed!")
    else:
        action_history.append([f'Administered CPR', f'{depth} inches | Compression rate: {comp_rate}'])
        messagebox.showinfo("CPR started", "CPR has been initiated.\n\nProcess will continue until ROSC.")
        cpr_yet = True

cpr_yet = False
def CPR():
    
    if cpr_yet:
        messagebox.showinfo("CPR Controls", "CPR is already being administered!")
        return None
    
    my_top = create_top_level(f'CPR Controls', 400, 205, load_captions=['Please wait...', 200])
    my_top.canvas.create_text(200, 30, text=f'Cardio-Pulmonary Resuscitation', font=("Century Gothic", 15, 'bold'), fill='Grey20')
    my_top.canvas.create_line(10, 60, 390, 60, fill='#3B8ED0', width=4)
    my_top.canvas.create_text(190, 90, text='Compression Rate :', font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey50', anchor=tk.E)
    my_top.canvas.create_text(190, 125, text='Depth (in.) :', font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey50', anchor=tk.E)
    my_top.canvas.create_line(10, 150, 390, 150, fill='#3B8ED0', width=4)

    combobox_1 = customtkinter.CTkComboBox(
        my_top.canvas, values=[
                                "60/min",
                                "80/min",
                                "100/min",
                                "120/min",
                                "140/min"
                            ],
        width=160, height=25, font=('Alte Haas Grotesk', 12), state='readonly', corner_radius=7
    )
    combobox_1.place(x=200, y=90, anchor=tk.W)
    combobox_1.set("Select...")

    val_entry = customtkinter.CTkEntry(
        master=my_top.canvas, placeholder_text="Nil", corner_radius=7, width=160, height=25,
        bg_color='White', font=('Alte Haas Grotesk', 12)
    )
    val_entry.place(x=200, y=125, anchor=tk.W)

    save_button = customtkinter.CTkButton(
        my_top, height=30, corner_radius=6, text='Start CPR', font=('Alte Haas Grotesk', 15, 'bold'),
        text_color='White', width=100, command=lambda: check_and_save_cpr(my_top, combobox_1.get(), val_entry.get())
    )
    save_button.place(x=390, y=165, anchor=tk.NE)

    discard_button = customtkinter.CTkButton(
        my_top, height=30, corner_radius=6, text='Cancel', font=('Alte Haas Grotesk', 15, 'bold'),
        text_color='White', width=100, fg_color='IndianRed2', hover_color='IndianRed4',
        command = lambda: my_top.destroy() if temp_untop(my_top, lambda: messagebox.askyesno("Discard changes?", "Are you sure you want to discard your changes?")) else None  # Use `command` instead of `function`
    )
    discard_button.place(x=280, y=165, anchor=tk.NE)

attached_defib_yet = False
def shock(my_top, num, energy):
    global attached_defib_yet
    my_top.destroy()
    if num == 'Select...' or energy.strip() == '' or not energy.isnumeric():
        messagebox.showerror("Error!", "Invalid or empty parameters passed!")
    else:
        if not attached_defib_yet:
            action_history.append(['Attached Defibrillator', str(datetime.now())])
        if num == '1':
            num = 'once'
        elif num == '2':
            num = 'twice'
        elif num == '3':
            num = 'thrice'
        elif num == '4':
            num = '4 times'
        action_history.append([f'Shocked Patient', f'{num.title()} | Energy: {energy}J'])
        messagebox.showinfo("Defibrillator", f"Successfully shocked the patient {num} with {energy}J of energy.")
        attached_defib_yet = True

def administer_fn(my_top, dose, dose_int, drug, method):
    my_top.destroy()
    if dose_int == 'Select...' or dose.strip() == '':
        messagebox.showerror("Error!", "Invalid or empty parameters passed!")
    else:
        action_history.append([f'Administered {drug} | {method}', f'{dose}, {dose_int.lower()}'])
        messagebox.showinfo("Administration", f"{drug} - {dose} will be administered {dose_int.lower()}.")

def administer(drug, method):    
    if drug == ''or drug == None or drug == 'None' or method == '' or method == None or method == 'Select Method...':
        return None
    my_top = create_top_level(f'Administer {drug}', 400, 205, load_captions=['Please wait...', 200])
    my_top.canvas.create_text(200, 30, text=f'{drug} | {method}', font=("Century Gothic", 13, 'bold'), fill='Grey20')
    my_top.canvas.create_line(10, 60, 390, 60, fill='#3B8ED0', width=4)
    my_top.canvas.create_text(190, 90, text='Dosing interval :', font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey50', anchor=tk.E)
    my_top.canvas.create_text(190, 125, text='Dose:', font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey50', anchor=tk.E)
    my_top.canvas.create_line(10, 150, 390, 150, fill='#3B8ED0', width=4)

    combobox_1 = customtkinter.CTkComboBox(
        my_top.canvas, values=[
                                "Just once",
                                "Every 3-5 minutes",
                                "Every 10 minutes"
                            ],
        width=160, height=25, font=('Alte Haas Grotesk', 12), state='readonly', corner_radius=7
    )
    combobox_1.place(x=200, y=90, anchor=tk.W)
    combobox_1.set("Select...")

    val_entry = customtkinter.CTkEntry(
        master=my_top.canvas, placeholder_text="Nil", corner_radius=7, width=160, height=25,
        bg_color='White', font=('Alte Haas Grotesk', 12)
    )
    val_entry.place(x=200, y=125, anchor=tk.W)

    save_button = customtkinter.CTkButton(
        my_top, height=30, corner_radius=6, text='Administer', font=('Alte Haas Grotesk', 15, 'bold'),
        text_color='White', width=100, command=lambda: administer_fn(my_top, val_entry.get(), combobox_1.get(), drug, method)
    )
    save_button.place(x=390, y=165, anchor=tk.NE)

    discard_button = customtkinter.CTkButton(
        my_top, height=30, corner_radius=6, text='Cancel', font=('Alte Haas Grotesk', 15, 'bold'),
        text_color='White', width=100, fg_color='IndianRed2', hover_color='IndianRed4',
        command = lambda: my_top.destroy() if temp_untop(my_top, lambda: messagebox.askyesno("Discard changes?", "Are you sure you want to discard your changes?")) else None  # Use `command` instead of `function`
    )
    discard_button.place(x=280, y=165, anchor=tk.NE)

def defib():    
    my_top = create_top_level(f'Defibrillator Controls', 400, 205, load_captions=['Please wait...', 200])
    my_top.canvas.create_text(200, 30, text=f'Attach Defibrillator', font=("Century Gothic", 15, 'bold'), fill='Grey20')
    my_top.canvas.create_line(10, 60, 390, 60, fill='#3B8ED0', width=4)
    my_top.canvas.create_text(190, 90, text='Number of Shocks :', font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey50', anchor=tk.E)
    my_top.canvas.create_text(190, 125, text='Shock Energy (J) :', font=('Alte Haas Grotesk', 12, 'bold'), fill='Grey50', anchor=tk.E)
    my_top.canvas.create_line(10, 150, 390, 150, fill='#3B8ED0', width=4)

    combobox_1 = customtkinter.CTkComboBox(
        my_top.canvas, values=[
                                "1",
                                "2",
                                "3",
                                "4"
                            ],
        width=160, height=25, font=('Alte Haas Grotesk', 12), state='readonly', corner_radius=7
    )
    combobox_1.place(x=200, y=90, anchor=tk.W)
    combobox_1.set("Select...")

    val_entry = customtkinter.CTkEntry(
        master=my_top.canvas, placeholder_text="Nil", corner_radius=7, width=160, height=25,
        bg_color='White', font=('Alte Haas Grotesk', 12)
    )
    val_entry.place(x=200, y=125, anchor=tk.W)

    save_button = customtkinter.CTkButton(
        my_top, height=30, corner_radius=6, text='Shock', font=('Alte Haas Grotesk', 15, 'bold'),
        text_color='White', width=100, command=lambda: shock(my_top, combobox_1.get(), val_entry.get())
    )
    save_button.place(x=390, y=165, anchor=tk.NE)

    discard_button = customtkinter.CTkButton(
        my_top, height=30, corner_radius=6, text='Cancel', font=('Alte Haas Grotesk', 15, 'bold'),
        text_color='White', width=100, fg_color='IndianRed2', hover_color='IndianRed4',
        command = lambda: my_top.destroy() if temp_untop(my_top, lambda: messagebox.askyesno("Discard changes?", "Are you sure you want to discard your changes?")) else None  # Use `command` instead of `function`
    )
    discard_button.place(x=280, y=165, anchor=tk.NE)