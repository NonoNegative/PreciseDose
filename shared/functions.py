import customtkinter
import shared.customtk as customtk
import tkinter as tk
from shared.tkgif import GifLabel
from datetime import datetime
from shared.CTkPDFViewer import *
from tkinter import messagebox
from shared.action_history import dll as action_history

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
