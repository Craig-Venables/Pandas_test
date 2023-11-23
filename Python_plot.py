import matplotlib.pyplot as plt
import numpy as np


class plot():
    ''' for plotting graphs in python

    current_density_ps = | type: array
    current_density_ng = | type: array
    electric_field_ps = | type: array
    electric_field_ng = | type: array
    current_over_voltage_ps = | type: array
    current_over_voltage_ng = | type: array
    voltage_to_the_half_ps = | type: array
    voltage_to_the_half_ng = | type: array
    '''

    def __init__(self, v_data, c_data, abs_c_data, current_density_ps='', current_density_ng='',
                 electric_field_ps='', electric_field_ng='', current_over_voltage_ps='', current_over_voltage_ng='',
                 voltage_to_the_half_ps='', voltage_to_the_half_ng='', resistance_on_value='', resistance_off_value='',
                 voltage_on_value='', voltage_off_value='', filename='', device_number='', section_name='',
                 device_name='', polymer_name='', np_materials='', full_path='',
                 on_off_ratio='') -> None:

        # data parsed through from instance class was ran
        self.v_data = v_data
        self.c_data = c_data
        self.abs_c_data = abs_c_data
        self.current_density_ps = current_density_ps
        self.current_density_ng = current_density_ng
        self.electric_field_ps = electric_field_ps
        self.electric_field_ng = electric_field_ng
        self.current_over_voltage_ps = current_over_voltage_ps
        self.current_over_voltage_ng = current_over_voltage_ng
        self.voltage_to_the_half_ps = voltage_to_the_half_ps
        self.voltage_to_the_half_ng = voltage_to_the_half_ng
        self.resistance_on_value = resistance_on_value
        self.resistance_off_value = resistance_off_value
        self.voltage_on_value = voltage_on_value
        self.voltage_off_value = voltage_off_value
        self.on_off_ratio = on_off_ratio
        self.filename = filename
        self.section_name = section_name
        self.device_name = device_name
        self.device_number = device_number
        self.full_path = full_path
        self.polymer_name = polymer_name
        self.np_materials = np_materials
        self.fig = None
        # fix these names

    def main_plot(self):
        '''
            plots iv and log iv graphs as subplots in its own window
            '''
        plt.close('all')
        self.fig = plt.figure(figsize=(12, 8))

        # using the functions main_plot the graphs
        plt.subplot(2, 2, 1)
        self.plot_iv()

        plt.subplot(2, 2, 2)
        self.plot_logiv()

        plt.subplot(2, 2, 3)
        self.plot_iv_avg()

        plt.subplot(2, 2, 4)
        self.information()

        plt.ioff()

        # add subplot title
        plt.suptitle(
            f'{self.polymer_name} -' + f'{self.device_name} -' + ' ' + f'{self.section_name} -' + ' ' + f'{self.filename}')

        # add label underneath plots for on-off ratio
        self.fig.text(0.5, 0.01, " ON/OFF Ratio @0.2v - " + f'{round(self.on_off_ratio, 4)}', ha='center', fontsize=10)
        plt.pause(0.01)
        plt.show(block=False)
        plt.pause(0.01)

    def plot_iv(self):
        """
                    Plots voltage against abs current using Matplotlib.

                    Parameters:
                    - voltage_data (list): List of voltage data points.
                    - abs_current_data (list): List of current data points.
                    """
        # Create a scatter main_plot of voltage against current
        plt.plot(self.v_data, self.c_data, color='blue')

        # Add labels and a title
        plt.ylabel('Current')
        # plt.yscale("log")
        plt.xlabel('Voltage')
        plt.title('Voltage vs. Current Graph')

    def plot_logiv(self):
        """
            Plots voltage against abs current using Matplotlib.

            Parameters:
            - voltage_data (list): List of voltage data points.
            - abs_current_data (list): List of current data points.
            """
        # Create a scatter main_plot of voltage against current
        plt.plot(self.v_data, self.abs_c_data, color='blue')

        # Add labels and a title
        plt.ylabel('abs Current')
        plt.yscale("log")
        plt.xlabel('Voltage')
        plt.title('Voltage vs. abs_Current Graph')
        # plt.title('Voltage vs. abs_Current Graph' + \
        #           '\n' + f'{self.device_name}' + ' ' + f'{self.section_name}' + ' ' + f'{self.filename}')

        # Show the main_plot
        # plt.show()

    def plot_iv_avg(self, num_points=20, ax=None):
        # plt.figure(figsize=(8, 6))

        # Calculate the length of the data
        data_len = len(self.v_data)

        # Determine the step size for averaging
        step_size = data_len // num_points

        # Initialize lists to store averaged data
        avg_v_data = []
        avg_c_data = []

        # Calculate the averages
        for i in range(0, data_len, step_size):
            avg_v = np.mean(self.v_data[i:i + step_size])
            avg_c = np.mean(self.c_data[i:i + step_size])
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

    def information(self):
        '''
        Add text information to the final section of the subplot.

        '''

        text = f' ON/OFF ratio = {self.on_off_ratio} \n' \
               f'{self.section_name, self.device_number, self.filename} \n' \
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

    def save_plot(self, figure_path):
        """
        Save the current figure to the specified file path.

        Parameters:
            figure_path (str): The file path where the figure should be saved.
        """
        if hasattr(self, 'fig') and self.fig is not None:
            self.fig.savefig(figure_path)
            print(f"Figure saved to {figure_path}")
        else:
            print("No figure to save. Please generate a figure using main_plot() first.")

        # # Plot some data (optional)
        # # x = [1, 2, 3, 4, 5]
        # # y = [10, 8, 6, 4, 2]
        # #plt.figure()
        # #plt.plot(x,y)
        #
        # # Add text directly to the plot
        # text_x = 2  # X-coordinate for the text
        # text_y = 8  # Y-coordinate for the text
        #
        # text = "This is some additional information."
        #
        # plt.text(text_x, text_y, text, fontsize=12, color='blue')
        #
        # # Customize labels and title (optional)
        # plt.xlabel('X-axis')
        # plt.ylabel('Y-axis')
        # plt.title('Plot with Additional Text')

        # Show the plot
        # plt.grid(True)

    def make_hist(self, data_in, x_label, ax):
        ax.hist(data_in)
        ax.set_xlabel(x_label)
        ax.set_ylabel('yes_and_no_sort')
        ax.grid()

    def plot_histograms(self):
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

        self.make_hist(self.resistance_on_values, 'Ron', axes[0, 0])
        self.make_hist(self.resistance_off_values, 'Roff', axes[0, 1])
        self.make_hist(self.voltage_off_values, 'Voff', axes[1, 0])
        self.make_hist(self.voltage_on_values, 'Von', axes[1, 1])

        plt.tight_layout()
        plt.show()

    # cpp.plot_python_single_sweep(file_info.v_data, file_info.c_data, file_info.abs_current,
    #                              file_info.current_density_ps, file_info.current_density_ng,
    #                              file_info.electric_field_ps, file_info.electric_field_ng,
    #                              file_info.current_over_voltage_ps, file_info.current_over_voltage_ng,
    #                              file_info.voltage_to_the_half_ps, file_info.voltage_to_the_half_ng,
    #                              file_info.resistance_on_value, file_info.resistance_off_value,
    #                              file_info.voltage_on_value, file_info.voltage_off_value,
    #                              file_info.filename, section_name, device_name, device_number, full_path,
    #                              file_info.on_off_ratio)
