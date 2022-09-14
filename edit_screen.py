# TODO 0: IMPORT REQUIRED LIBRARIES AND MODULES
from tkinter import *
from tkinter import font
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter.colorchooser import askcolor
from marking import Marking
import matplotlib.font_manager as fm


# TODO 1: CREATE A CLASS
class EditScreen:
    def __init__(self, file_directory_list):
        self.color_choice = "#FFA701"
        self.watermark_start_position_x = 40
        self.watermark_start_position_y = 40
        self.file_directory_list = list(file_directory_list)
        self.image_temporary_memory = []
        self.image_ind_list = []
        self.edit_window_init()
        self.display_selected_images()
        self.edit_window.mainloop()

    # TODO 2: CREATE A NEW EDIT SCREEN
    def edit_window_init(self):
        self.edit_window = Toplevel()
        self.edit_window.title("Edit & Save")
        self.edit_window.geometry('1200x800')
        self.edit_window.resizable(False, False)
        self.background_color = "#F8F1F1"
        self.my_font_color = "#0A065D"
        self.my_font = 'Poppins'
        self.edit_window.grid_columnconfigure(0, weight=1)
        self.edit_window.grid_columnconfigure(1, weight=550)
        self.edit_window.grid_columnconfigure(2, weight=550)
        self.edit_window.grid_columnconfigure(3, weight=550)

    # TODO 3: DISPLAY SELECTED IMAGES IN THIS SCREEN
    def display_selected_images(self):
        # CREATE A MAIN FRAME
        thumbnail_main_frame = Frame(self.edit_window, height=770, width=300)
        thumbnail_main_frame.grid(column=0, padx=0, pady=0, sticky="ns")
        thumbnail_main_frame.grid_columnconfigure(0, weight=3)
        thumbnail_main_frame.grid_columnconfigure(1, weight=1)
        # CREATE A CANVAS
        thumbnail_canvas = Canvas(thumbnail_main_frame, height=770, width=300)
        thumbnail_canvas.grid(column=0, sticky="ns", padx=0, pady=10)
        # ADD SCROLL BAR TO THE CANVAS
        myscrollbar = Scrollbar(thumbnail_main_frame, orient="vertical", command=thumbnail_canvas.yview)
        myscrollbar.grid(row=0, column=1, sticky="ns")
        # CONFIGURE THE CANVAS
        thumbnail_canvas.configure(yscrollcommand=myscrollbar.set)
        thumbnail_canvas.bind("<Configure>",
                              lambda e: thumbnail_canvas.configure(scrollregion=thumbnail_canvas.bbox("all")))

        # TODO 3.1: PUT ALL SELECTED IMAGES THUMBNAIL TO LEFT HAND SIDE OF THE EDIT SCREEN
        # CREATE ANOTHER FRAME INSIDE OF THE CANVAS
        thumbnail_subframe = Frame(thumbnail_canvas)
        # ADD THIS NEW FRAME TO A WINDOW IN THE CANVAS
        thumbnail_canvas.create_window((0, 0), width=300, window=thumbnail_subframe, anchor="nw")
        for selected_image_directory in self.file_directory_list:
            selected_image = Image.open(selected_image_directory).resize((240, 140))
            self.image_temporary_memory.append(ImageTk.PhotoImage(selected_image))
            self.image_ind_list = Button(thumbnail_subframe, image=self.image_temporary_memory[-1],
                                         command=lambda arg=selected_image_directory: self.show_image_on_edit_screen(
                                             arg))
            self.image_ind_list.pack(fill=Y, expand=True)
        self.water_marking_user_choices()
        # TODO 3.2: WHEN ONE CLICKS ON THUMBNAIL, DISPLAY THE IMAGE

    def show_image_on_edit_screen(self, image_to_display):
        self.selected_image_transfer = image_to_display
        self.image_select = Image.open(fp=image_to_display).convert("RGBA").resize((800,600))
        self.original_trans_image=Image.open(fp=image_to_display, mode="r").convert("RGBA")
        #self.original_trans_image_object = ImageTk.PhotoImage(image=self.original_trans_image)
        display_frame = Frame(self.edit_window, height=600, width=800)
        display_frame.grid(row=0, column=1, sticky=N, pady=10, padx=30)
        self.display_canvas = Canvas(display_frame, height=600, width=800)
        self.display_canvas.pack()

        self.display_canvas.image_transfer = ImageTk.PhotoImage(image=self.image_select)
        self.x = self.display_canvas.create_image(0, 0, image=self.display_canvas.image_transfer, anchor="nw")

        # # TODO 3.3: PRINT THE DEFAULT WATERMARK ON THE SCREEN
        self.update_display_canvas(self.image_select,self.original_trans_image)

# ETIKETI DOGRU YERE KONUMLANDIRMAYA CALISACAGIM!!!!!
    def update_display_canvas(self, show_image,real_image):
        def hex_to_rgb(hex_num):
            rgb_list = []
            for ind in (0, 2, 4):
                decimal = int(hex_num[ind:ind + 2], 16)
                rgb_list.append(decimal)
            return tuple(rgb_list)
        worker_image = show_image.copy()
        self.resize_convert_ratio_width = int(real_image.width) / 800
        self.resize_convert_ratio_height = int(real_image.height) / 600
        rgb_default = hex_to_rgb(self.color_choice[1:])
        font_default = ImageFont.truetype(font=fm.findfont(fm.FontProperties(family=self.fonttype.get())),
                                          size=self.fontsize.get())
        txt = Image.new("RGBA", worker_image.size, (255, 255, 255, 0))
        draw_text = ImageDraw.Draw(txt, "RGBA")
        draw_text.text(xy=(0, 0),
                       text=self.watermark_textbox.get(),
                       font=font_default,
                       fill=((rgb_default[0], rgb_default[1], rgb_default[2], self.opacity_value.get())))
        x_axis_location = int(self.watermark_start_position_x)
        y_axis_location = int(self.watermark_start_position_y)
        worker_image.paste(txt, (x_axis_location, y_axis_location), mask=txt)
        self.photo = ImageTk.PhotoImage(worker_image)
        self.display_canvas.itemconfig(self.x, image=self.photo)

    # TODO 4: MAKE CONFIGURATIONS MENU

    def water_marking_user_choices(self):
        edit_properties_frame = Frame(self.edit_window, height=160, width=800)
        edit_properties_frame.grid(row=0, column=1, sticky=S)
        self.edit_properties_canvas = Canvas(edit_properties_frame, height=160, width=800)
        self.edit_properties_canvas.pack(fill=Y, expand=True)

        # TODO 4.1: CREATE THE WATERMARK TEXT ENTRY BOX
        self.user_watermark_entry = StringVar()
        self.watermark_textbox = Entry(edit_properties_frame, textvariable=self.user_watermark_entry,
                                       font=("Helvetica", 12), width=40)
        self.watermark_textbox.insert(0, "Plese write your watermark!")
        self.watermark_textbox.bind("<Button-1>", self.delete_watermark_text)
        self.edit_properties_canvas.create_window(10, 10, anchor=NW, window=self.watermark_textbox)

        # TODO 4.2: FONT SIZE
        self.fontsize = IntVar()
        self.fontsize.set(14)
        fontsize_list = [fs + 2 for fs in range(6, 80, 2)]
        fontsize_dropdown_menu = OptionMenu(edit_properties_frame, self.fontsize, *fontsize_list,
                                            command=self.update_watermark_display)
        self.edit_properties_canvas.create_text(43, 85, text="Font Size:", font=("Helvetica", 12))
        self.edit_properties_canvas.create_window(80, 70, anchor=NW, window=fontsize_dropdown_menu)

        # TODO 4.3: FONT TYPE
        self.fonttype = StringVar()
        self.fonttype.set("Arial")
        fonttype_dropdown_menu = OptionMenu(edit_properties_frame, self.fonttype,
                                            command=self.update_watermark_display, *list(font.families()))
        self.edit_properties_canvas.create_text(43, 55, text="Font Type:", font=("Helvetica", 12))
        self.edit_properties_canvas.create_window(80, 40, anchor=NW, window=fonttype_dropdown_menu)

        # TODO 4.4: COLOR
        self.color_picking_button = Button(edit_properties_frame, command=self.color_picking, width=2)
        self.color_picking_button.configure(bg=self.color_choice)
        self.edit_properties_canvas.create_text(59, 117, text="Color:", font=("Helvetica", 12))
        self.edit_properties_canvas.create_window(81, 105, anchor=NW, window=self.color_picking_button)
        # TODO 4.5: OPACITY
        self.opacity_value = IntVar()
        self.opacity_value.set(255)
        opacity_slider = Scale(edit_properties_frame, variable=self.opacity_value, from_=255, to=0, orient=HORIZONTAL,
                                            command=self.update_watermark_display)
        self.edit_properties_canvas.create_text(190, 100, text="Opacity:", font=("Helvetica", 12))
        self.edit_properties_canvas.create_window(230, 70, anchor=NW, window=opacity_slider)

        # TODO 4.6: WATERMARK POSITIONING
        # TODO 4.6.1: CREATE POSITION BUTTONS
        right_position_button = Button(edit_properties_frame, text="🡲", command=self.position_increase_xaxis, width=2)
        left_position_button = Button(edit_properties_frame, text="🡰", command=self.position_decrease_xaxis, width=2)
        up_position_button = Button(edit_properties_frame, text="🡱", command=self.position_decrease_yaxis, width=2)
        down_position_button = Button(edit_properties_frame, text="🡳", command=self.position_increase_yaxis, width=2)
        self.edit_properties_canvas.create_window(430, 10, anchor=NW, window=up_position_button)
        self.edit_properties_canvas.create_window(430, 90, anchor=NW, window=down_position_button)
        self.edit_properties_canvas.create_window(400, 50, anchor=NW, window=left_position_button)
        self.edit_properties_canvas.create_window(460, 50, anchor=NW, window=right_position_button)

        # TODO 5: CREATE SAVE BUTTON
        self.save_button = Button(edit_properties_frame, text="💾", font=("Helvetica", 40),
                                  command=self.save_edited_image, width=4)
        self.edit_properties_canvas.create_window(530, 30, anchor=NW, window=self.save_button)
        self.image_displayed = False

    # TODO 5.1: SAVE THE EDITED IMAGES
    def save_edited_image(self):
        user_inputs = [self.watermark_textbox.get(), self.fontsize.get(), self.fonttype.get(),
                       self.color_choice, self.watermark_start_position_x,
                       self.watermark_start_position_y, self.opacity_value.get(),self.resize_convert_ratio_width,self.resize_convert_ratio_height]
        Marking(user_inputs, self.selected_image_transfer)

    def position_decrease_xaxis(self):
        if self.watermark_start_position_x > 14:
            self.watermark_start_position_x -= 15
            self.update_display_canvas(self.image_select,self.original_trans_image)
        else:
            pass

    def position_increase_xaxis(self):
        if self.watermark_start_position_x < 786:
            self.watermark_start_position_x += 15
            self.update_display_canvas(self.image_select,self.original_trans_image)
        else:
            pass

    def position_decrease_yaxis(self):
        if self.watermark_start_position_y > 14:
            self.watermark_start_position_y -= 15
            self.update_display_canvas(self.image_select,self.original_trans_image)
        else:
            pass

    def position_increase_yaxis(self):
        if self.watermark_start_position_y < 786:
            self.watermark_start_position_y += 15
            self.update_display_canvas(self.image_select,self.original_trans_image)
        else:
            pass

    def color_picking(self):
        colors = askcolor(title="Please select your watermark color!")
        self.color_choice = colors[1]
        self.color_picking_button.configure(bg=f'{self.color_choice}')
        self.update_display_canvas(self.image_select,self.original_trans_image)

    def delete_watermark_text(self, event):
        if self.watermark_textbox.get() == "Plese write your watermark!":
            self.watermark_textbox.delete(0, END)
            self.update_watermark_display(self.image_select,self.original_trans_image)

    def update_watermark_display(self,event,*args):
        self.update_display_canvas(self.image_select,self.original_trans_image)
