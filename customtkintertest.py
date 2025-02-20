import customtkinter
import tkinter as tk
from PIL import Image, ImageTk, ImageColor
from shared.transforms import RGBTransform

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

root = customtkinter.CTk()
root.title("PreciseDose")
root.attributes('-fullscreen', True)

screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()

background_image = Image.open('assets\\backgrounds\\sample.jpg')
background_image = background_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
background_image = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
canvas.pack()

optionmenu_1 = customtkinter.CTkOptionMenu(canvas, values=["Option 1", "Option 2", "Option 42 long long long..."])
optionmenu_1.place(x=200, y=200, anchor=tk.CENTER)
optionmenu_1.set("CTkOptionMenu")

label_1 = customtkinter.CTkLabel(master=root, justify=customtkinter.CENTER, text="Age", text_color='White', font=('Century Gothic', 16, 'bold'), corner_radius=7, bg_color='White', fg_color='#00aeef')
label_1.place(x=400, y=400, anchor=tk.CENTER)

canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
root.mainloop()