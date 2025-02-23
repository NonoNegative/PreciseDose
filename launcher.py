import customtkinter
import tkinter as tk
from tkVideoPlayer import TkinterVideo
from PIL import Image, ImageTk, ImageColor

root = customtkinter.CTk()
root.title("PreciseDose")
root.attributes('-fullscreen', True)

screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()

canvas = tk.Canvas(root, width=screen_width, height=screen_height, highlightthickness=0, background='Black')
canvas.pack()

video_player = TkinterVideo(canvas, False, False, borderwidth=0, bg='Black', fg='black')
video_player.set_size((screen_width, screen_height))
video_player.place(x=0, y=0)
video_player.bind("<<Loaded>>", lambda e: e.widget.config(width=screen_width, height=screen_height))
video_player.load("test.mp4")

def start_video():
    video_player.seek(0)
    video_player.play()
    video_player.after(11200, start_video)

start_video()

calibrate_icon = customtkinter.CTkImage(light_image=Image.open("assets\\icons\\calibrate.png"),
                                  dark_image=Image.open("assets\\icons\\calibrate.png"),
                                  size=(30, 30))

calibrate_button = customtkinter.CTkButton(master=canvas, image=calibrate_icon, text='Start Simulation', compound=tk.LEFT, font=('Rage Italic', 23), width=560, height=60, corner_radius=8, bg_color='Black', border_color='Black')
calibrate_button.place(x=screen_width/2, y=screen_height/2, anchor=tk.CENTER)

root.mainloop()