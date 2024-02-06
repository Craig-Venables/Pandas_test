import matplotlib.pyplot as plt
import numpy as np
import file as f
import scipy as sp
import pathlib as pl
import os


def main_plot(voltage , current, abs_current, save_loc, crossing_points, re_save,file_info):
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

        plt.subplot(2, 2, 4)
        text = (crossing_points)
        plt.text(0.5, 0.5, text, ha='center', va='center', fontsize=12)
        # self.plot_graph_other()
        # self.information()
        # self.plot_array_changes()

        # add label underneath plots for on-off ratio
        # self.fig.text(0.5, 0.01, " ON/OFF Ratio @0.2v - " + f'{round(self.on_off_ratio, 4)}', ha='center', fontsize=10)
        # plt.show()
        # add subplot title

        # Turn off interactive mode
        plt.ioff()

        file_path = os.path.join(save_loc, f"{short_filename}.png")

        plt.savefig(file_path, bbox_inches='tight', dpi=200)

        print(f"File saved successfully at {file_path}")
        return fig
    else:

        print(f"File {file_path} already exists. Skipping save.")
        return None


def main_plot_loop(voltage,current,abs_current,sweep_num, save_loc, crossing_points, re_save,file_info):
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
    save_name = f"{short_filename}" + "- #" + f"{sweep_num}"+ ".png"
    file_path = os.path.join(save_loc, "Extracted sweeps",f"{filename}",save_name)


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

        #print(f"File saved successfully at {file_path}")
    else:
        return None
        #print(f"File {file_path} already exists. Skipping save.")

    # uncomment to show for 0.01 sec
    # plt.pause(0.01)

    # uncomment to keep on screen
    # plt.show()

        return fig

def plot_iv(voltage,current):
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


def plot_logiv(voltage,abs_current):
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


def plot_iv_avg(voltage,current, num_points=20, ax=None):

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

    #print(self.data["voltage"].to_numpy()) #dataframe

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

    print(step_num,total_delay)
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


def information(on_off_ratio,section_name,device_number,filename):
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
