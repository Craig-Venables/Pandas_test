# anything gifs here

import numpy as np
import imageio
import os
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFile
import re


ImageFile.LOAD_TRUNCATED_IMAGES = True



def create_gif_from_folder(folder_path, output_gif, fps=2, restart_duration=2):
    """
    Create a GIF from a folder full of images, with a black screen added at the end.

    Parameters:
        folder_path (str): Path to the folder containing the images.
        output_gif (str): Path for the output GIF file.
        duration (float): Duration (in seconds) between each frame.
        restart_duration (float): Duration (in seconds) of the black screen at the end to indicate restart.
    """
    # Specify the desired width and height for resizing the images
    width = 1046  # Adjust as needed
    height = 759  # Adjust as needed
    try:
        # List all files in the folder and sort them numerically
        image_files = sorted(
            [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.png')],
            key=lambda x: int(re.search(r'\d+', os.path.basename(x)).group()))  # Custom sorting key

        # Check if there are no image files
        if not image_files:
            pass
            # raise FileNotFoundError("No image files found in the folder.")

        font_size = 40
        # old s
        # Load all images
        images = []
        for idx, image_file in enumerate(image_files):
            # Read the image using PIL
            image = Image.open(image_file)
            # Resize the image to a common shape
            image = image.resize((width, height))  # Specify the desired width and height

            # Draw index of the image_file to the left-hand corner
            draw = ImageDraw.Draw(image)
            font = ImageFont.load_default()  # You can adjust the font and size here if needed
            font = ImageFont.truetype("arial.ttf", font_size)  # Change the font size here
            text_color = "red"
            draw.text((30, 30), str(idx + 1), fill=text_color, font=font)  # Adjust position as needed

            # Convert the image to numpy array
            image = np.array(image)
            images.append(image)

        # Add a black screen at the end to indicate restart
        black_image = np.zeros_like(images[0])
        images.append(black_image)

        # Calculate the number of frames needed for restart duration
        restart_frames = int(restart_duration * 2)  # Assuming the default frame rate is 2 frames per second

        # Add additional black screens for restart indication
        for _ in range(restart_frames):
            images.append(black_image)

        # Save the images as a GIF using imageio
        imageio.mimsave(output_gif, images, format='GIF', fps=fps)

        print(f"GIF created successfully at {output_gif}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Continuing without creating the GIF.")

    except Exception as e:
        print("check create_gif_from_folder either error or no files")
        print(folder_path)
        print(f"An error occurred: {e}")