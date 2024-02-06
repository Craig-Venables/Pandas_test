import matplotlib.pyplot as plt
import numpy as np
import file as f
import scipy as sp
import pathlib as pl
import os


class plot():
    '''
    pass through data frame
    '''

    def __init__(self, data,file_info,save_loc,filepath) -> None:
        self.data = data

        self._unpack_dataframe()



        # gets file info
        self.type = file_info.get('type')
        self.polymer = file_info.get('polymer')
        self.sample_name = file_info.get('sample_name')
        self.section = file_info.get('section')
        self.device_number = file_info.get('device_number')
        self.filename = file_info.get('file_name')
        self.save_loc = save_loc
        self.short_filename = os.path.splitext(self.filename)[0]

        file_info = f.extract_folder_names(filepath)
        short_name = f.short_name(filepath)
        long_name = f.long_name(filepath)

        # looped data
        self.looped_info = False
        self.normalized_areas = ""
        self.ps_areas = ""
        self.ng_areas = ""

        self.fig = None


    def _unpack_dataframe(self):
        """ Unpacks dataframe with the names given """
        for column in self.data.columns:
            setattr(self, column.lower(), self.data.get(column))

    def _unpack_dataframe_file_info(self):
        """ Unpacks dataframe with the names given """
        for column in self.file_info.columns:
            setattr(self, column.lower(), self.file_info.get(column))

    def main_plot(self,crossing_points,re_save):
        '''
            plots iv and log iv graphs as subplots and saves it
        '''

        file_path = os.path.join(self.save_loc, f"{self.short_filename}.png")

        if not os.path.exists(file_path) or re_save:
            plt.close('all')
            self.fig = plt.figure(figsize=(12, 8))

            plt.suptitle(
                f'{self.polymer} -' + f'{self.sample_name} -' + ' ' + f'{self.section} -' + ' '
                + f'{self.device_number} -' + ' ' + self.filename)

            # using the functions main_plot the graphs
            plt.subplot(2, 2, 1)
            self.plot_iv(self.voltage, self.current)

            plt.subplot(2, 2, 2)
            self.plot_logiv(self.voltage, self.abs_current)

            plt.subplot(2, 2, 3)
            self.plot_iv_avg(self.voltage, self.current)

            plt.subplot(2, 2, 4)
            text = (crossing_points)
            plt.text(0.5, 0.5, text, ha='center', va='center', fontsize=12)
            #self.plot_graph_other()
            # self.information()
            # self.plot_array_changes()

            # add label underneath plots for on-off ratio
            # self.fig.text(0.5, 0.01, " ON/OFF Ratio @0.2v - " + f'{round(self.on_off_ratio, 4)}', ha='center', fontsize=10)
            #plt.show()
            # add subplot title

            # Turn off interactive mode
            plt.ioff()


            file_path = os.path.join(self.save_loc, f"{self.short_filename}.png")


            plt.savefig(file_path, bbox_inches='tight', dpi=200)

            print(f"File saved successfully at {file_path}")
            return self.fig
        else:

            print(f"File {file_path} already exists. Skipping save.")
            return None


    def main_plot_loop(self,voltage,current,abs_current,sweep_num):
        '''
            plots iv and log iv graphs as subplots and saves it
        '''

        save_name = f"{self.short_filename}" + "- #" + f"{sweep_num}"+ ".png"
        file_path = os.path.join(self.save_loc, "Extracted sweeps",f"{self.filename}",save_name)


        if not os.path.exists(file_path):
            plt.close('all')
            self.fig = plt.figure(figsize=(12, 8))

            plt.suptitle(
                f'{self.polymer} -' + f'{self.sample_name} -' + ' ' + f'{self.section} -' + ' '
                + f'{self.device_number} -' + ' ' + self.filename)

            # using the functions main_plot the graphs
            plt.subplot(2, 2, 1)
            self.plot_iv(voltage, current)

            plt.subplot(2, 2, 2)
            self.plot_logiv(voltage, abs_current)

            plt.subplot(2, 2, 3)
            self.plot_iv_avg(voltage, current)

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

            return self.fig

    def plot_iv(self, voltage,current):
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
        # plt.yscale("log")
        plt.xlabel('Voltage')
        plt.title('Voltage vs. Current Graph')


    def plot_logiv(self, voltage,abs_current):
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


    def plot_iv_avg(self, voltage,current, num_points=20, ax=None):
        # plt.figure(figsize=(8, 6))

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



    def plot_array_changes(self,vall):
        # Create a range for the x-axis (indices of the array)
        x = range(len(vall))

        # Plot the array values
        plt.plot(x, vall, marker='o', linestyle='-')

        # Set labels and title
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.title('Change of Values in the Array')

        # Show the plot
        plt.show()

    # def information(self):
    #     '''
    #     Add text information to the final section of the subplot.
    #
    #     '''
    #
    #     text = f' ON/OFF ratio = {self.on_off_ratio} \n' \
    #            f'{self.section_name, self.device_number, self.filename} \n' \
    #            'add more information about device here,\n' \
    #            ' or new graph'
    #     # Create a subplot for information
    #     plt.subplot(2, 2, 4)
    #
    #     # Clear any existing content in the subplot
    #     plt.cla()
    #
    #     # # Add the text to the subplot
    #     # plt.text(0.5, 0.5, text, ha='center', va='center', fontsize=12)
    #
    #     # Add the text to the subplot without a frame
    #     # plt.text(0.5, 0.5, text, ha='center', va='center', fontsize=12, bbox=dict(facecolor='none', edgecolor='none'))
    #     plt.text(0.5, 0.5, text, ha='center', va='center', fontsize=12, bbox=None)
    #
    #     # Remove axis ticks and labels
    #     plt.xticks([])
    #     plt.yticks([])
    #
    #     # Adjust the subplot layout
    #     plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)


    # def save_plot(self, figure_path):
    #     """
    #     Save the current figure to the specified file path.
    #
    #     Parameters:
    #         figure_path (str): The file path where the figure should be saved.
    #     """
    #     if hasattr(self, 'fig') and self.fig is not None:
    #         self.fig.savefig(figure_path)
    #         print(f"Figure saved to {figure_path}")
    #     else:
    #         print("No figure to save. Please generate a figure using main_plot() first.")
    #
    #     # # Plot some data (optional)
    #     # # x = [1, 2, 3, 4, 5]
    #     # # y = [10, 8, 6, 4, 2]
    #     # #plt.figure()
    #     # #plt.plot(x,y)
    #     #
    #     # # Add text directly to the plot
    #     # text_x = 2  # X-coordinate for the text
    #     # text_y = 8  # Y-coordinate for the text
    #     #
    #     # text = "This is some additional information."
    #     #
    #     # plt.text(text_x, text_y, text, fontsize=12, color='blue')
    #     #
    #     # # Customize labels and title (optional)
    #     # plt.xlabel('X-axis')
    #     # plt.ylabel('Y-axis')
    #     # plt.title('Plot with Additional Text')
    #
    #     # Show the plot
    #     # plt.grid(True)


    # def make_hist(self, data_in, x_label, ax):
    #     ax.hist(data_in)
    #     ax.set_xlabel(x_label)
    #     ax.set_ylabel('yes_and_no_sort')
    #     ax.grid()


    # def plot_histograms(self):
    #     fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
    #
    #     self.make_hist(self.resistance_on_values, 'Ron', axes[0, 0])
    #     self.make_hist(self.resistance_off_values, 'Roff', axes[0, 1])
    #     self.make_hist(self.voltage_off_values, 'Voff', axes[1, 0])
    #     self.make_hist(self.voltage_on_values, 'Von', axes[1, 1])
    #
    #     plt.tight_layout()
    #     plt.show()


