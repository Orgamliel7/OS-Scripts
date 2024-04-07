import re
import os
from PIL import Image, ImageDraw, ImageFont
import sys
sys.path.append(r".")
from PyRingIt import RingIT  # noqa
from utils.record import Record  # noqa
from utils.config_manager import DEFAULT_CONFIG_FILE_LOCATION  # noqa


def add_text_to_image(input_image_path, output_image_path, above_text, below_text, below_text_size=12):
    img = Image.open(input_image_path)
    width, height = img.size

    # Create a new image with additional space for text
    new_width, new_height = width + 80, height + 80 + 2 * below_text_size
    new_img = Image.new("RGB", (new_width, new_height), color=(255, 255, 255))

    # Paste the original image in the center of the new image
    new_img.paste(img, ((new_width - width) // 2, (new_height - height) // 2))

    draw = ImageDraw.Draw(new_img)
    font_above = ImageFont.truetype("arial.ttf", 16, encoding="unic")
    font_below = ImageFont.truetype("arial.ttf", below_text_size, encoding="unic")

    # Add above text to the image
    above_text_width, above_text_height = draw.textsize(above_text, font=font_above)
    draw.text(((new_width - above_text_width) // 2, 10), above_text, font=font_above, fill='black')

    # Add below text to the image
    below_text_width, below_text_height = draw.textsize(below_text, font=font_below)
    draw.text(((new_width - below_text_width) // 2, new_height - below_text_height - 10), below_text, font=font_below, fill='black')

    # Save the edited image
    new_img.save(output_image_path)

    # Open the saved image with the default image viewer on Windows
    try:
        os.startfile(output_image_path)
    except Exception as e:
        print(f"Error opening image: {e}")

    return output_image_path


def main():
    rit = RingIT("video")
    input_path = input("Enter the input image path: ")

    match = re.match(r'^"(.*)"$', input_path)
    input_image_path = match.group(1) if match else input_path
    output_image_path = input_image_path[:-4] + "_text.png"

    above_text = "SCAN TO DISPLAY HOLOGRAM"
    below_text = "Having issues? Visit Summitov.com/portal."

    saved_image_path = add_text_to_image(input_image_path, output_image_path, above_text, below_text)
    print("Image saved at:", saved_image_path)
    rit.print_qr(saved_image_path)


if __name__ == "__main__":
    main()
