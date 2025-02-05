if __name__ == '__main__':
    import tkinter as tk
    from RealtimeSTT import AudioToTextRecorder
    from PIL import Image, ImageTk, ImageColor
    import tkinter.messagebox as messagebox
    from shared.transforms import RGBTransform
    import shared.customtk as customtk
    from shared.tkgif import GifLabel
    from ollama import chat
    from ollama import ChatResponse
    import tkinter.scrolledtext as st 
    
    root = tk.Tk()
    root.title("CliniSim")
    root.attributes('-fullscreen', True)
    # icon = tk.PhotoImage(file='images\\icon.png')
    # root.iconphoto(True, icon)

    screen_height = root.winfo_screenheight()
    screen_width = root.winfo_screenwidth()

    background_image = Image.open('assets\\backgrounds\\sample.jpg')
    background_image = background_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    background_image = ImageTk.PhotoImage(background_image)

    canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
    canvas.pack()

    canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

    def show_info(text, color):
        canvas.delete('drawerinfo')
        canvas.create_text(screen_width-5, 34, text=text, font=('Helvetica', '10', 'bold'), fill=color, anchor=tk.NE, tags='drawerinfo')

    drawer_icon = Image.open("assets\\icons\\drawer.png")
    drawer_icon = drawer_icon.resize((169, 38), Image.Resampling.LANCZOS)
    alpha = drawer_icon.split()[-1]
    drawer_icon = drawer_icon.convert("RGB")
    drawer_icon = RGBTransform().mix_with(ImageColor.getcolor('#232323', "RGB"),factor=1).applied_to(drawer_icon)
    drawer_icon.putalpha(alpha)
    drawer_icon = ImageTk.PhotoImage(drawer_icon)
    canvas.create_image(screen_width+55, -6 ,anchor=tk.NE, image=drawer_icon)

    close = customtk.create_tk_image('assets\\icons\\close_small.jpg', 19, 19)
    minimize = customtk.create_tk_image('assets\\icons\\minimize_small.jpg', 19, 19)
    test = customtk.create_tk_image('assets\\icons\\test_small.jpg', 19, 19)

    close_button = tk.Button(canvas, image=close, bd=0, highlightthickness= 0, bg="#232323", relief=tk.SUNKEN, highlightcolor='#232323', activebackground='#232323', command=lambda: customtk.quit_confirm(root))
    close_button.image = close; close_button.place(x=screen_width-5, y=5, width=20, height=20, anchor=tk.NE)

    minimize_button = tk.Button(canvas, image=minimize, bd=0, highlightthickness= 0, bg="#232323", relief=tk.SUNKEN, highlightcolor='#232323', activebackground='#232323', command=root.iconify)
    minimize_button.image = minimize; minimize_button.place(x=screen_width-35, y=5, width=20, height=20, anchor=tk.NE)

    test_button = tk.Button(canvas, image=test, bd=0, highlightthickness= 0, bg="#232323", relief=tk.SUNKEN, highlightcolor='#232323', activebackground='#232323')
    test_button.image = test; test_button.place(x=screen_width-65, y=5, width=20, height=20, anchor=tk.NE)

    close_button.bind('<Enter>', lambda x: show_info('Close', 'IndianRed2')); close_button.bind('<Leave>', lambda x: show_info('', 'IndianRed2'))
    minimize_button.bind('<Enter>', lambda x: show_info('Minimize', 'Gold')); minimize_button.bind('<Leave>', lambda x: show_info('', 'Gold'))
    test_button.bind('<Enter>', lambda x: show_info('Configure/Launcher', 'Pale Green')); test_button.bind('<Leave>', lambda x: show_info('', 'Pale Green'))

    static_img = customtk.create_tk_image('assets\\static\\static_v1.png', 1920, 1080)
    canvas.create_image(0, 0, anchor=tk.NW, image=static_img)

    # previous = ["Patient's age seems to be 20. Patient is female. Patient's weight is 60 kilograms. State is unconscious. Heartrate is eighty beats per minute. Blood pressure is low."]
    previous = []
    recorder = AudioToTextRecorder()

    ini_prompt = '''Can you extract the essential information from this text and return it in a JSON format. Take key features and return like:
                {'age': 20,
                'gender': 'female'
                'weight': ...}
                If there are no key features in the text at all, just say 'No features detected in input'. Make sure also include text featires like the current state of the patient
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
        canvas.create_text(520, 915, text="Speak now...", tags='stt', anchor=tk.NW, font=('Alte Haas Grotesk', 14, 'bold'), fill='Grey25')

    def print_to_output():
        global previous
        canvas.delete('stt')
        canvas.create_text(520, 915, text="Transcribing...", tags='stt', anchor=tk.NW, font=('HAlte Haas Grotesk', 14, 'bold'), fill='Grey25')
        transcription = recorder.text()
        previous.append(transcription)
        canvas.delete('stt')
        canvas.create_text(520, 915, text=transcription, tags='stt', width=810, anchor=tk.NW, font=('Alte Haas Grotesk', 14, 'bold'), fill='Grey20')

    send_message_button = customtk.create_image_button(root, 'assets\\icons\\start_recording.jpg', 1390, 908, 30, 30, bg='#3e3e3e', active_bg='#3e3e3e', disable_btn_press_anim=True, command=start_recording)
    send_message_button_2 = customtk.create_image_button(root, 'assets\\icons\\stop_recording.jpg', 1390, 960, 30, 30, bg='#3e3e3e', active_bg='#3e3e3e', disable_btn_press_anim=True, command=print_to_output)
    send_message_button_3 = customtk.create_image_button(root, 'assets\\icons\\transcript.jpg', 1390, 1014, 30, 30, bg='#3e3e3e', active_bg='#3e3e3e', disable_btn_press_anim=True, command=ollama_chat)

    root.mainloop()