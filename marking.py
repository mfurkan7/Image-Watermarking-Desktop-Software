import random

from PIL import Image, ImageDraw, ImageFont
import matplotlib.font_manager as fm


class Marking:
    def __init__(self, user_inputs, selected_image_transfer):
        self.user_inputs = user_inputs
        self.selected_image_transfer = selected_image_transfer
        print(self.selected_image_transfer[-1:-4])
        self.user_input_marking()

    def user_input_marking(self):
        def hex_to_rgb(hex_num):
            rgb_list = []
            for ind in (0, 2, 4):
                decimal = int(hex_num[ind:ind + 2], 16)
                rgb_list.append(decimal)
            return tuple(rgb_list)

        rgb = hex_to_rgb(self.user_inputs[3][1:])
        font = ImageFont.truetype(font=fm.findfont(fm.FontProperties(family=self.user_inputs[2])),
                                  size=int(self.user_inputs[1]*self.user_inputs[7]))
        with Image.open(self.selected_image_transfer).convert("RGBA") as processing_image:
            text = Image.new("RGBA", processing_image.size)
            drawing = ImageDraw.Draw(text)
            drawing.text((int(self.user_inputs[4]*self.user_inputs[7]),int(self.user_inputs[5]*self.user_inputs[8])), text=self.user_inputs[0],
                         fill=(rgb[0], rgb[1], rgb[2], self.user_inputs[6]),font=font)
            output_image = Image.alpha_composite(processing_image, text)
            image_number=random.random()
            output_image.save(f'./Watermarked_Images/watermarked_image{str(image_number)[2:7]}.png')
