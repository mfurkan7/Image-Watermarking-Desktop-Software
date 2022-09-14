from tkinter import *
from tkinter import filedialog
from edit_screen import EditScreen


class Screen:
    def __init__(self):
        self.background_color = "#F8F1F1"
        self.my_font_color = "#0A065D"
        self.my_font = 'Poppins'
        self.window = Tk()
        self.window.title("Image Watermarking Powered By MFE")
        self.window.configure(padx=10, pady=10, bg=self.background_color)

        self.upload_screen_canvas = Canvas(self.window, width=400, height=400, bg=self.background_color, highlightthickness=0)
        upload_icon = PhotoImage(file="file_upload_image.png")
        self.upload_screen_canvas.create_image(200, 100, image=upload_icon)
        self.upload_screen_canvas.create_text(200, 225, text="Please select an image to watermark!", font=(self.my_font, '15'),
                                              fill=self.my_font_color)
        self.upload_screen_canvas.grid(column=2, row=2)

        browse_button = Button(text="Select Image(s)", fg=self.my_font_color, font=self.my_font, bg="#D2C8C8",
                               highlightthickness=0, command=self.browse_function)
        start_button = Button(text="Start", fg=self.my_font_color, font=self.my_font, bg="#D2C8C8",
                              highlightthickness=0, command=self.edit_screen_process)

        self.upload_screen_canvas.create_window(200, 280, window=browse_button)
        self.upload_screen_canvas.create_window(200, 350, window=start_button)
        self.window.mainloop()

    def edit_screen_process(self):
        edit_screen = EditScreen(self.file_directory_list)

    def browse_function(self):
        self.file_directory_list = filedialog.askopenfilenames()
