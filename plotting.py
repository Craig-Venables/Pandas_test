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
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter
import memristors

ImageFile.LOAD_TRUNCATED_IMAGES = True


def main_plot(voltage, current, abs_current, save_loc, crossing_points, re_save, file_info, loop=False, num_sweeps=0):
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

    def create_graph():
        plt.close('all')
        fig = plt.figure(figsize=(12, 8))

        plt.suptitle(
            f'{polymer} -' + f'{sample_name} -' + ' ' + f'{section} -' + ' '
            + f'{device_number} -' + ' ' + filename)

        # using the functions main_plot the graphs
        plt.subplot(2, 2, 1)
        plt.title('Iv_Graph')
        plot_iv(voltage, current)

        plt.subplot(2, 2, 2)
        plt.title('Log_Iv')
        plot_logiv(voltage, abs_current)

        plt.subplot(2, 2, 3)
        plt.title('Iv Avg showing direction')
        if loop:
            # This dosnt save correctly it shows the correct image, but dosnt save
            split_v_data, split_c_data = split_loops(voltage, current, num_sweeps)
            plot_iv_avg(split_v_data[0], split_c_data[0])

        else:
            plot_iv_avg(voltage, current)

        # Create subplot for the final plot with two graphs
        plt.subplot(2, 2, 4)
        plt.title('Current vs Index')
        plot_current_count(current)


        # plot_iv_subplots(voltage, current)

        # text = (crossing_points)
        # plt.text(0.5, 0.5, text, ha='center', va='center', fontsize=12)

        # plt.show()

        # Turn off interactive mode
        plt.ioff()

        file_path = os.path.join(save_loc, f"{short_filename}.png")
        plt.tight_layout()
        plt.savefig(file_path, bbox_inches='tight', dpi=200)
        #plt.show()
        print(f"File saved successfully at {file_path}")

    if os.path.exists(file_path):
        # File exists
        if re_save:
            create_graph()
            # Plot the graph
            # Re-save is True, so create the file (overwriting if it exists)
        if not re_save:
            # Re-save is False wit file exists, skip plot
            pass
    # Save the graph
    else:
        # File doesn't exist
        create_graph()


def iv_and_log_iv_plot(voltage, current, abs_current, file_info, save_loc="", crossing_points="", re_save=False):
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

    def create_graph():
        plt.close('all')
        fig = plt.figure(figsize=(12, 8))

        plt.suptitle(
            f'{polymer} -' + f'{sample_name} -' + ' ' + f'{section} -' + ' '
            + f'{device_number} -' + ' ' + filename)

        # using the functions main_plot the graphs
        plt.subplot(2, 1, 1)
        plot_iv(voltage, current)

        plt.subplot(2, 1, 2)
        plot_logiv(voltage, abs_current)

        # Turn off interactive mode
        plt.ioff()

        file_path = os.path.join(save_loc, f"{short_filename}.png")

        plt.savefig(file_path, bbox_inches='tight', dpi=200)

        print(f"File saved successfully at {file_path}")
        return fig

    if os.path.exists(file_path):
        # File exists
        if re_save:
            create_graph()
            # Plot the graph
            # Re-save is True, so create the file (overwriting if it exists)
        if not re_save:
            # Re-save is False wit file exists, skip plot
            pass
    # Save the graph
    else:
        # File doesn't exist
        create_graph()



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
    folder_path = os.path.join(save_loc, "Extracted sweeps", f"{filename}")

    def create_graph():
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

    if os.path.exists(file_path):
        # File exists
        if re_save:
            create_graph()
            # Plot the graph
            # Re-save is True, so create the file (overwriting if it exists)
        if not re_save:
            # Re-save is False wit file exists, skip plot
            pass
    # Save the graph
    else:
        # File doesn't exist
        create_graph()

    return folder_path


def plot_images_in_folder(folder_path, save_loc):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)
    images = [file for file in files if file.endswith('.png') or file.endswith('.jpg')]

    num_images = len(images)
    fig, axs = plt.subplots(1, num_images, figsize=(15, 5))

    for i, image_file in enumerate(images):
        image_path = os.path.join(folder_path, image_file)
        image = Image.open(image_path)
        axs[i].imshow(image)
        axs[i].axis('off')

        # Add index number to the left of each graph
        axs[i].text(0.05, 0.95, str(i + 1), color='red', fontsize=12, ha='left', va='top', transform=axs[i].transAxes)

    plt.subplots_adjust(wspace=0.02)
    # plt.show()
    plt.savefig(save_loc, dpi=200)
    print("file saved at ,", save_loc)

def plot_iv_subplots(voltage, current):
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


def plot_iv(voltage, current, fontsize=8):
    """
     Plots voltage against abs current using Matplotlib.

      Parameters:
      - voltage_data (list): List of voltage data points.
      - abs_current_data (list): List of current data points.
      """
    # Create a scatter main_plot of voltage against current
    plt.plot(voltage, current, color='blue')
    # Add labels and a title
    plt.ylabel('Current', fontsize=fontsize)
    plt.xlabel('Voltage', fontsize=fontsize)
    # plt.title('Voltage vs. Current memristors')


def plot_logiv(voltage, abs_current, fontsize=8):
    """
        Plots voltage against abs current using Matplotlib.

        Parameters:
        - voltage_data (list): List of voltage data points.
        - abs_current_data (list): List of current data points.
        """
    # Create a scatter main_plot of voltage against current
    plt.plot(voltage, abs_current, color='blue')

    # Add labels and a title
    plt.ylabel('abs Current', fontsize=fontsize)
    plt.yscale("log")
    plt.xlabel('Voltage', fontsize=fontsize)
    # plt.title('Voltage vs. abs_Current memristors')
    # plt.title('Voltage vs. abs_Current memristors' + \
    #           '\n' + f'{self.device_name}' + ' ' + f'{self.section_name}' + ' ' + f'{self.filename}')

    # Show the main_plot
    # plt.show()

def plot_current_count(current,fontsize=8):
    """
        Plots voltage against abs current using Matplotlib.

        Parameters:
        - voltage_data (list): List of voltage data points.
        - abs_current_data (list): List of current data points.
        """
    # Create a scatter main_plot of voltage against current
    plt.plot(range(len(current)), current, 'r-')
    #plt.plot(current, 'r.', color='blue')
    # Add labels and a title
    plt.ylabel('Current', fontsize=fontsize)
    plt.xlabel('Index', fontsize=fontsize)


    # Show the main_plot
    # plt.show()


def plot_iv_avg(voltage, current, num_points=20, fontsize=8):
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
    # plt.xlabel('Voltage (V)', fontsize= fontsize)
    # plt.ylabel('Current (A)', fontsize= fontsize)
    # plt.title(f'Averaged Data Showing {num_points} Data points with Arrows indicating direction')
    # plt.legend()
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


def graph_temp(voltage, current, abs_current, type, polymer, sample_name, section, device_number, filename):
    '''
        plots iv and log iv graphs as subplots and saves it
    '''

    short_filename = os.path.splitext(filename)[0]

    def create_graph():
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
        num_sweeps = Data.check_for_loops(voltage)
        # if loop:
        #     # This dosnt save correctly it shows the correct image, but dosnt save
        #     split_v_data, split_c_data = split_loops(voltage, current, num_sweeps)
        #     plot_iv_avg(split_v_data[0], split_c_data[0])
        #
        # else:
        #
        if num_sweeps > 1:
            split_v_data, split_c_data = split_loops(voltage, current, num_sweeps)
            plot_iv_avg(split_v_data[0], split_c_data[0])
            # plot_iv_avg(voltage, current)
        else:
            plot_iv_avg(voltage, current)

        # Create subplot for the final plot with two graphs
        plt.subplot(2, 2, 4)
        # plt.show()
        # plot_iv_subplots(voltage, current)

        # text = (crossing_points)
        # plt.text(0.5, 0.5, text, ha='center', va='center', fontsize=12)

        # Turn off interactive mode
        plt.ioff()
        plt.pause(0.01)
        plt.show(block=False)
        plt.pause(0.01)
        return fig
        # file_path = os.path.join(save_loc, f"{short_filename}.png")

        # plt.savefig(file_path, bbox_inches='tight', dpi=200)

        # print(f"File saved successfully at {file_path}")

    fig = create_graph()
    return fig


def sclc_ps(voltage, current_density, fontsize=8):
    # create scatter
    plt.plot(voltage, current_density, color='black')
    # Add labels and a title
    plt.yscale("log")
    plt.xscale("log")

    # plt.tick_params(axis='both', which='major', labelsize=fontsize)
    # plt.ylabel('current density positive (A/cm^2) ', fontsize= fontsize)
    # plt.xlabel('Voltage (V)', fontsize= fontsize)
    # plt.title('SCLC')


def sclc_ng(voltage, abs_current_density, fontsize=8):
    # create scatter
    print(abs_current_density, voltage)
    plt.plot(voltage, abs_current_density, color='black')
    plt.yscale("log")
    plt.xscale("log")

    # Add labels and a title
    # plt.ylabel('Current density negative (A/cm^2)', fontsize= fontsize)
    # plt.xlabel('abs(Voltage) (V)', fontsize= fontsize)
    # plt.title('SCLC')


def schottky_emission_ps(voltage_half, current, fontsize=8):
    # create scatter
    plt.plot(voltage_half, current, color='black')
    # Add labels and a title
    plt.yscale("log")
    # plt.ylabel('Current (A) ', fontsize= fontsize)
    # plt.xlabel('Voltage (V^1/2)', fontsize= fontsize)
    # plt.title('Schottky Emission (positive)')


def schottky_emission_ng(voltage_half, abs_current, fontsize=8):
    # create scatter
    plt.plot(voltage_half, abs_current, color='black')
    # Add labels and a title
    plt.yscale("log")
    # plt.ylabel('abs(Current) (A) ', fontsize= fontsize)
    # plt.xlabel('Voltage (V^1/2)', fontsize= fontsize)
    # plt.title('Schottky Emission (Negative)')


def poole_frenkel_ps(current_voltage, voltage_half, fontsize=8):
    # create scatter
    plt.plot(current_voltage, voltage_half, color='black')
    # Add labels and a title
    plt.yscale("log")
    # plt.ylabel('Current/Voltage (A/V) ', fontsize= fontsize)
    # plt.xlabel('Voltage (V^1/2)', fontsize= fontsize)
    # plt.title('Poole-Frenkel (Positive')


def poole_frenkel_ng(abs_current_voltage, voltage_half, fontsize=8):
    # create scatter
    plt.plot(abs_current_voltage, voltage_half, color='black')
    # Add labels and a title
    plt.yscale("log")

    # plt.ylabel('abs(Current/Voltage) (A/V) ', fontsize= fontsize)
    # plt.xlabel('Voltage (V^1/2)', fontsize= fontsize)
    # plt.title('Poole-Frenkel (negative')


def resistance_time(resistance):
    plt.plot(range(len(resistance)), resistance, color='black')


def grid_spec(data):
    fontsize = 5
    gs = gridspec.GridSpec(4, 5, wspace=0.3, hspace=0.3)

    ax1 = plt.subplot(gs[0:2, 0:2])  # Rows 0 and 1 Columns 0 and 1 iv
    ax1.text(0.05, 0.95, 'Iv ', transform=ax1.transAxes, fontsize=8, va='top', ha='left', color="red")
    plot_iv(data.get('voltage'), data.get('current'), fontsize)

    ax2 = plt.subplot(gs[0:2, 2:4])  # logiv
    ax2.text(0.05, 0.95, 'Iv_log ', transform=ax2.transAxes, fontsize=8, va='top', ha='left', color="red")
    plot_logiv(data.get('voltage'), data.get('abs_current'), fontsize)

    ax3 = plt.subplot(gs[2, 0])  # sclc
    ax3.text(0.05, 0.95, 'sclc ', transform=ax3.transAxes, fontsize=8, va='top', ha='left', color="red")
    sclc_ps(data.get('voltage'), data.get('current_Density_ps'), fontsize)

    ax4 = plt.subplot(gs[2, 1])  # sclc -ve
    ax4.text(0.05, 0.95, 'sclc -ve', transform=ax4.transAxes, fontsize=8, va='top', ha='left', color="red")
    sclc_ng(data.get('voltage'), data.get('current_Density_ng'), fontsize)

    ax5 = plt.subplot(gs[2, 2])  # scxotty
    ax5.text(0.05, 0.95, 'schottky', transform=ax5.transAxes, fontsize=8, va='top', ha='left', color="red")
    schottky_emission_ps(data.get('sqrt_Voltage'), data.get('current'), fontsize)

    ax6 = plt.subplot(gs[2, 3])  # scotty
    ax6.text(0.05, 0.95, 'shottky -ve', transform=ax6.transAxes, fontsize=8, va='top', ha='left', color="red")
    schottky_emission_ng(data.get('sqrt_Voltage'), data.get('abs_current'), fontsize)

    ax7 = plt.subplot(gs[0, 4])  # pf +ve
    ax7.text(0.05, 0.95, 'pf +ve', transform=ax7.transAxes, fontsize=8, va='top', ha='left', color="red")
    poole_frenkel_ps(data.get('inverse_resistance_ps'), data.get('sqrt_Voltage'), fontsize)

    ax8 = plt.subplot(gs[1, 4])  # pf-ve
    ax8.text(0.05, 0.95, 'Poole-frenkel -ve', transform=ax8.transAxes, fontsize=8, va='top', ha='left', color="red")
    poole_frenkel_ng(data.get('inverse_resistance_ng'), data.get('sqrt_Voltage'), fontsize)

    ax9 = plt.subplot(gs[3, 0:2])  # resis coubt
    ax9.text(0.05, 0.95, 'resistance time', transform=ax9.transAxes, fontsize=8, va='top', ha='left', color="red")
    resistance_time(data.get('resistance'))

    ax10 = plt.subplot(gs[3, 2:4])  # volt count
    ax10.text(0.05, 0.95, 'voltage count', transform=ax10.transAxes, fontsize=8, va='top', ha='left', color="red")
    #
    ax11 = plt.subplot(gs[3, 4])  # direction
    ax11.text(0.05, 0.95, 'direction', transform=ax11.transAxes, fontsize=8, va='top', ha='left', color="red")
    plot_iv_avg(data.get('voltage'), data.get('current'), 20, fontsize)

    ax12 = plt.subplot(gs[2, 4])  # information
    ax12.text(0.05, 0.95, 'info', transform=ax12.transAxes, fontsize=8, va='top', ha='left', color="red")

    # Adjusting tick label font size
    for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12]:
        ax.tick_params(axis='both', which='both', labelsize=6)  # Adjust labelsize as needed

    for ax in [ax3, ax4, ax5, ax6, ax7, ax8]:
        ax.xaxis.set_major_formatter(FuncFormatter(format_tick))
        ax.yaxis.set_major_formatter(FuncFormatter(format_tick))

        # ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        # ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

    # Adjust layout to prevent overlap
    # plt.tight_layout()

    # Show plot
    plt.show()


def format_tick(value, pos):
    # Format tick label as 10^x
    return f'$10^{{{int(value)}}}$'


def polar_subplot(x, y):
    fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw=dict(projection='polar'))
    ax1.plot(x, y)
    ax2.plot(x, y ** 2)


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


def split_loops(v_data, c_data, num_loops):
    """ splits the looped data and outputs each sweep as another array coppied from data"""
    total_length = len(v_data)  # Assuming both v_data and c_data have the same length
    size = total_length // num_loops  # Calculate the size based on the number of loops

    # Convert size to integer
    size = int(size)

    # Handle the case when the division leaves a remainder
    if total_length % num_loops != 0:
        size += 1

    split_v_data = [v_data[i:i + size] for i in range(0, total_length, size)]
    split_c_data = [c_data[i:i + size] for i in range(0, total_length, size)]

    return split_v_data, split_c_data
