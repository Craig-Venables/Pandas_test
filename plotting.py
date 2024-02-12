import matplotlib.pyplot as plt
import numpy as np
import file as f
import scipy as sp
import pathlib as pl
import os
import imageio
import os
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFile
import re
import matplotlib.gridspec as gridspec

ImageFile.LOAD_TRUNCATED_IMAGES = True


def main_plot(voltage, current, abs_current, save_loc, crossing_points, re_save, file_info):
    '''
        plots iv and log iv graphs as subplots and saves it
    '''

    type = file_info.get('type')
    polymer = file_info.get('polymer')
    sample_name = file_info.get('sample_name')
    section = file_info.get('section')
    device_number = file_info.get('device_number')
    filename = file_info.get('file_name')
    save_loc = save_loc
    short_filename = os.path.splitext(filename)[0]

    file_path = os.path.join(save_loc, f"{short_filename}.png")

    if not os.path.exists(file_path) or re_save:
        plt.close('all')
        fig = plt.figure(figsize=(12, 8))

        plt.suptitle(
            f'{polymer} -' + f'{sample_name} -' + ' ' + f'{section} -' + ' '
            + f'{device_number} -' + ' ' + filename)

        # using the functions main_plot the graphs
        plt.subplot(2, 2, 1)
        plot_iv(voltage, current)

        plt.subplot(2, 2, 2)
        plot_logiv(voltage, abs_current)

        plt.subplot(2, 2, 3)
        plot_iv_avg(voltage, current)

        # Create subplot for the final plot with two graphs
        plt.subplot(2, 2, 4)
        plot_iv_subplots(voltage, current)

        # text = (crossing_points)
        # plt.text(0.5, 0.5, text, ha='center', va='center', fontsize=12)

        plt.show()

        # Turn off interactive mode
        plt.ioff()

        file_path = os.path.join(save_loc, f"{short_filename}.png")

        plt.savefig(file_path, bbox_inches='tight', dpi=200)

        print(f"File saved successfully at {file_path}")
        return fig
    else:

        print(f"File {file_path} already exists. Skipping save.")
        return None

def plot_iv_subplots(voltage,current):
    '''
        plots iv and log iv graphs as subplots and saves it
    '''
    # Generate some data
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)

    # Create subplots
    fig, axs = plt.subplots(2)  # 2 rows of subplots

    # Plot data on the subplots
    axs[0].plot(x, y1, color='blue')
    axs[0].set_title('Sin(x)')
    axs[1].plot(x, y2, color='red')
    axs[1].set_title('Cos(x)')

def main_plot_loop(voltage, current, abs_current, sweep_num, save_loc, crossing_points, re_save, file_info):
    '''
        plots iv and log iv graphs as subplots and saves it
    '''
    type = file_info.get('type')
    polymer = file_info.get('polymer')
    sample_name = file_info.get('sample_name')
    section = file_info.get('section')
    device_number = file_info.get('device_number')
    filename = file_info.get('file_name')
    save_loc = save_loc
    short_filename = os.path.splitext(filename)[0]
    save_name = f"{short_filename}" + "- #" + f"{sweep_num}" + ".png"
    file_path = os.path.join(save_loc, "Extracted sweeps", f"{filename}", save_name)

    if not os.path.exists(file_path):
        plt.close('all')
        fig = plt.figure(figsize=(12, 8))

        plt.suptitle(
            f'{polymer} -' + f'{sample_name} -' + ' ' + f'{section} -' + ' '
            + f'{device_number} -' + ' ' + filename)

        # using the functions main_plot the graphs
        plt.subplot(2, 2, 1)
        plot_iv(voltage, current)

        plt.subplot(2, 2, 2)
        plot_logiv(voltage, abs_current)

        plt.subplot(2, 2, 3)
        plot_iv_avg(voltage, current)

        plt.subplot(2, 2, 4)
        # self.plot_graph_other()
        # self.information()
        # self.plot_array_changes()

        # add label underneath plots for on-off ratio
        # self.fig.text(0.5, 0.01, " ON/OFF Ratio @0.2v - " + f'{round(self.on_off_ratio, 4)}', ha='center', fontsize=10)
        # plt.show()
        # add subplot title

        # Turn off interactive mode
        plt.ioff()

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        plt.savefig(file_path, bbox_inches='tight', dpi=200)

        # print(f"File saved successfully at {file_path}")
    else:
        return None
        # print(f"File {file_path} already exists. Skipping save.")

        # uncomment to show for 0.01 sec
        # plt.pause(0.01)

        # uncomment to keep on screen
        # plt.show()

        return fig


def plot_iv(voltage, current):
    """
     Plots voltage against abs current using Matplotlib.

      Parameters:
      - voltage_data (list): List of voltage data points.
      - abs_current_data (list): List of current data points.
      """
    # Create a scatter main_plot of voltage against current
    plt.plot(voltage, current, color='blue')
    # Add labels and a title
    plt.ylabel('Current')
    plt.xlabel('Voltage')
    plt.title('Voltage vs. Current Graph')


def plot_logiv(voltage, abs_current):
    """
        Plots voltage against abs current using Matplotlib.

        Parameters:
        - voltage_data (list): List of voltage data points.
        - abs_current_data (list): List of current data points.
        """
    # Create a scatter main_plot of voltage against current
    plt.plot(voltage, abs_current, color='blue')

    # Add labels and a title
    plt.ylabel('abs Current')
    plt.yscale("log")
    plt.xlabel('Voltage')
    plt.title('Voltage vs. abs_Current Graph')
    # plt.title('Voltage vs. abs_Current Graph' + \
    #           '\n' + f'{self.device_name}' + ' ' + f'{self.section_name}' + ' ' + f'{self.filename}')

    # Show the main_plot
    # plt.show()


def plot_iv_avg(voltage, current, num_points=20, ax=None):
    # Calculate the length of the data
    data_len = len(voltage)

    # Determine the step size for averaging
    step_size = data_len // num_points

    # Initialize lists to store averaged data
    avg_v_data = []
    avg_c_data = []

    # Calculate the averages
    for i in range(0, data_len, step_size):
        avg_v = np.mean(voltage[i:i + step_size])
        avg_c = np.mean(current[i:i + step_size])
        avg_v_data.append(avg_v)
        avg_c_data.append(avg_c)

    # Plot the IV curve with smaller, colored points for averaged data
    plt.scatter(avg_v_data, avg_c_data, c='b', marker='o', label='Averaged Data', s=10)

    # Add arrows between data points
    for i in range(1, len(avg_v_data)):
        plt.annotate('', xy=(avg_v_data[i], avg_c_data[i]), xytext=(avg_v_data[i - 1], avg_c_data[i - 1]),
                     arrowprops=dict(arrowstyle='->', color='red'))

    # Customize labels and title
    plt.xlabel('Voltage (V)')
    plt.ylabel('Current (A)')
    plt.title(f'Averaged Data Showing {num_points} Data points with Arrows indicating direction')
    plt.legend()
    plt.grid(True)


def plot_graph_other(self):
    """ code got from raven"""
    data = {"t": [], "V": [], "I": [], "dIdt": []}

    # print(self.data["voltage"].to_numpy()) #dataframe

    data["V"] = (self.data["voltage"].to_numpy())
    data["I"] = (self.data["current"].to_numpy())

    data["V"] = np.array(data["V"])  # volts
    data["I"] = np.array(data["I"]) * 10 ** 6  # mAmps

    src_delay = 1  # msec
    meas_delay = 20  # msec
    total_delay = src_delay + meas_delay

    v_step = 0.1  # volts
    v_range = [(-4, 4), (-5, 5)]
    step_num = len(data["V"])

    data["t"] = np.arange(start=0, stop=step_num * total_delay, step=total_delay)

    print(step_num, total_delay)
    print(data)

    data["dIdt"] = np.gradient(data["I"], total_delay)

    # just need to plot graphs now

    fig, axs = plt.subplots(3, 1, tight_layout=True, figsize=(8, 12))

    '''axs[0].plot(data[0]["t"], data[0]["V"], color = "r")
    axs[1].plot(data[0]["t"], data[0]["I"], color = "r")
    axs[2].plot(data[0]["t"], data[0]["dIdt"], color = "r")'''

    axs[0].plot(data["t"][0:82], data["V"][0:82], color="b")
    axs[0].plot(data["t"][0:82], data["I"][0:82], color="r")
    # axs[1].plot(data[1]["t"][0:82], data[1]["dIdt"][0:82], color="b")
    # axs[2].plot(data[1]["V"][0:82], data[1]["dIdt"][0:82], color="b")

def sclc_ps(voltage,current_density):
    # create scatter
    plt.plot(voltage, current_density, color='black')
    # Add labels and a title
    plt.ylabel('current density positive (A/cm^2) ')
    plt.xlabel('Voltage (V)')
    plt.title('SCLC')

def sclc_ng(voltage, abs_current_density):
    # create scatter
    plt.plot(voltage, abs_current_density, color='black')
    # Add labels and a title
    plt.ylabel('Current density negative (A/cm^2)')
    plt.xlabel('abs(Voltage) (V)')
    plt.title('SCLC')

def schottky_emission_ps(voltage_half,current):
    # create scatter
    plt.plot(voltage_half, current, color='black')
    # Add labels and a title
    plt.ylabel('Current (A) ')
    plt.xlabel('Voltage (V^1/2)')
    plt.title('Schottky Emission (positive)')

def schottky_emission_ng(voltage_half, abs_current):
    # create scatter
    plt.plot(voltage_half, abs_current, color='black')
    # Add labels and a title
    plt.ylabel('abs(Current) (A) ')
    plt.xlabel('Voltage (V^1/2)')
    plt.title('Schottky Emission (Negative)')

def poole_frenkel_ps(current_voltage, voltage_half):
    # create scatter
    plt.plot(current_voltage, voltage_half, color='black')
    # Add labels and a title
    plt.ylabel('Current/Voltage (A/V) ')
    plt.xlabel('Voltage (V^1/2)')
    plt.title('Poole-Frenkel (Positive')

def poole_frenkel_ng(abs_current_voltage, voltage_half):
    # create scatter
    plt.plot(abs_current_voltage, voltage_half, color='black')
    # Add labels and a title
    plt.ylabel('abs(Current/Voltage) (A/V) ')
    plt.xlabel('Voltage (V^1/2)')
    plt.title('Poole-Frenkel (negative')


def grid_spec():

    gs = gridspec.GridSpec(4, 4)
    ax1 = plt.subplot(gs[0, :2])
    ax2 = plt.subplot(gs[2, :])
    ax3 = plt.subplot(gs[2, :])


    ax2 = plt.subplot(gs[1, :-1])
    ax3 = plt.subplot(gs[1:, -1])
    ax4 = plt.subplot(gs[-1, 0])
    ax5 = plt.subplot(gs[-1, -2])


def polar_subplot(x,y):
    fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw=dict(projection='polar'))
    ax1.plot(x, y)
    ax2.plot(x, y ** 2)

plt.show()

def information(on_off_ratio, section_name, device_number, filename):
    '''
    Add text information to the final section of the subplot.

    '''

    text = f' ON/OFF ratio = {on_off_ratio} \n' \
           f'{section_name, device_number, filename} \n' \
           'add more information about device here,\n' \
           ' or new graph'
    # Create a subplot for information
    plt.subplot(2, 2, 4)

    # Clear any existing content in the subplot
    plt.cla()

    # # Add the text to the subplot
    # plt.text(0.5, 0.5, text, ha='center', va='center', fontsize=12)

    # Add the text to the subplot without a frame
    # plt.text(0.5, 0.5, text, ha='center', va='center', fontsize=12, bbox=dict(facecolor='none', edgecolor='none'))
    plt.text(0.5, 0.5, text, ha='center', va='center', fontsize=12, bbox=None)

    # Remove axis ticks and labels
    plt.xticks([])
    plt.yticks([])

    # Adjust the subplot layout
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)


# good one dont delete
# def create_gif_from_folder(folder_path, output_gif, duration=5, restart_duration=2):
#     """
#     Create a GIF from a folder full of images, with a black screen added at the end.
#
#     Parameters:
#         folder_path (str): Path to the folder containing the images.
#         output_gif (str): Path for the output GIF file.
#         duration (float): Duration (in seconds) between each frame.
#         restart_duration (float): Duration (in seconds) of the black screen at the end to indicate restart.
#     """
#     try:
#         # List all files in the folder and sort them numerically
#         image_files = sorted(
#             [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.png')],
#             key=lambda x: int(re.search(r'\d+', os.path.basename(x)).group()))  # Custom sorting key
#
#         # Check if there are no image files
#         if not image_files:
#             pass
#             #raise FileNotFoundError("No image files found in the folder.")
#
#         # # Load all images
#         # images = [imageio.imread(image_file) for image_file in image_files]
#
#         # Load all images
#         images = []
#         for image_file in image_files:
#             image = imageio.imread(image_file)
#             #print(f"Image file: {image_file}, shape: {image.shape}")  # Print the shape of each loaded image
#             images.append(image)
#
#         # # Add a black screen at the end to indicate restart
#         # black_image = np.zeros_like(images[0])
#         # images.append(black_image)
#
#         # Calculate the number of frames needed for restart duration
#         restart_frames = int(restart_duration * 2)  # Assuming the default frame rate is 2 frames per second
#
#         # # Add additional black screens for restart indication
#         # for _ in range(restart_frames):
#         #     images.append(black_image)
#
#         # Save the images as a GIF using imageio
#         imageio.mimsave(output_gif, images, format='GIF', fps=2)
#
#         #print(f"GIF created successfully at {output_gif}")
#
#     except FileNotFoundError as e:
#         #pass
#         print(f"Error: {e}")
#         print("Continuing without creating the GIF.")
#
#     except Exception as e:
#         #pass
#         print(f"An error occurred: {e}")
# #


def create_gif_from_folder(folder_path, output_gif, duration=5, restart_duration=2):
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

        # Load all images
        images = []
        for image_file in image_files:
            # Read the image using PIL
            image = Image.open(image_file)
            # Resize the image to a common shape
            image = image.resize((width, height))  # Specify the desired width and height
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
        imageio.mimsave(output_gif, images, format='GIF', fps=2)

        print(f"GIF created successfully at {output_gif}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Continuing without creating the GIF.")

    except Exception as e:
        print("check create gif fom folder final")
        print(folder_path)
        print(f"An error occurred: {e}")

# def create_gif_from_folder(folder_path, output_gif, duration=5, restart_duration=2):
#     """
#     Create a GIF from a folder full of images, with a black screen added at the end.
#
#     Parameters:
#         folder_path (str): Path to the folder containing the images.
#         output_gif (str): Path for the output GIF file.
#         duration (float): Duration (in seconds) between each frame.
#         restart_duration (float): Duration (in seconds) of the black screen at the end to indicate restart.
#     """
#     try:
#         # List all files in the folder and sort them numerically
#         image_files = sorted(
#             [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.png')],
#             key=lambda x: int(re.search(r'\d+', os.path.basename(x)).group()))  # Custom sorting key
#
#         # Check if there are no image files
#         if not image_files:
#             pass
#             #raise FileNotFoundError("No image files found in the folder.")
#
#         # Set a common canvas size
#         canvas_width = 2500
#         canvas_height = 2000
#         canvas_channels = 3  # Assuming RGB images
#
#         # Create a blank canvas
#         canvas = np.zeros((canvas_height, canvas_width, canvas_channels), dtype=np.uint8)
#
#         # Set the starting position to paste the images onto the canvas
#         start_x = 0
#         start_y = 0
#
#         # Iterate through each image and paste it onto the canvas
#         for image_file in image_files:
#             image = imageio.imread(image_file)
#             if len(image.shape) == 3 and image.shape[2] == 4:  # Check if image has alpha channel
#                 image = image[:, :, :3]  # Remove alpha channel
#             # Get the dimensions of the image
#             height, width, _ = image.shape
#             # Paste the image onto the canvas
#             canvas[start_y:start_y + height, start_x:start_x + width, :] = image
#             # Update the starting position for the next image
#             start_x += width
#
#         # Save the canvas as a single GIF
#         imageio.mimsave(output_gif, [canvas], format='GIF', fps=2)
#
#         #print(f"GIF created successfully at {output_gif}")
#
#     except FileNotFoundError as e:
#         #pass
#         print(f"Error: {e}")
#         print("Continuing without creating the GIF.")
#
#     except Exception as e:
#         #pass
#         print(f"An error occurred: {e}")
#
