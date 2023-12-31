import numpy as np
import pandas as pd
import file as f
import plot as plot
import os
import math

import matplotlib.pyplot as plt
from itertools import zip_longest

debugging = False

''' all the data manipulation goes here including any dataframe manipulation 
 '''


def file_analysis(filepath, plot_graph, save_df, device_path):
    """ for all info from a single file this determines if it is a s """

    file_info = f.extract_folder_names(filepath)
    short_name = f.short_name(filepath)
    long_name = f.long_name(filepath)

    print("-----")
    print("Currently working on -", file_info.get('file_name'))
    # print('Information on file below:')
    # for variable_name, folder_name in file_info.items():
    #     print(f"{variable_name} = '{folder_name}'")
    # print ("-----")

    # what type of data is this?
    # check how many columns it has and match it against something that tells you what data
    # ie Iv sweeps = 2 columns named voltage and current
    try:
        # Pull voltage and current data from file
        v_data, c_data = split_iv_sweep(filepath)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("probably due too the file not being what it expects please check")

    # get positive and negative values of voltage and current data for equations later
    v_data_ps, c_data_ps = filter_positive_values(v_data, c_data)
    v_data_ng, c_data_ng = filter_negative_values(v_data, c_data)
    # checks for looped data and calculates the number of loops
    num_sweeps = check_for_loops(v_data)

    # create a dataframe for the device of all the data
    data = {'voltage': v_data,
            'current': c_data,
            'abs_current': absolute_val(c_data),
            'resistance': resistance(v_data, c_data),
            'voltage_ps': v_data_ps,
            'current_ps': c_data_ps,
            'voltage_ng': v_data_ng,
            'current_ng': c_data_ng,
            'log_Resistance': log_value(resistance(v_data, c_data)),
            'abs_Current_ps': absolute_val(c_data_ps),
            'abs_Current_ng': absolute_val(c_data_ng),
            'current_Density_ps': current_density_eq(v_data_ps, c_data_ps),
            'current_Density_ng': current_density_eq(v_data_ng, c_data_ng),
            'electric_field_ps': electric_field_eq(v_data_ps),
            'electric_field_ng': electric_field_eq(v_data_ng),
            'inverse_resistance_ps': inverse_resistance_eq(v_data_ps, c_data_ps),
            'inverse_resistance_ng': inverse_resistance_eq(v_data_ng, c_data_ng),
            'sqrt_Voltage': sqrt_array(v_data),
            }

    df = pd.DataFrame(data)

    # if there is more than one loop adds
    if num_sweeps > 1:
        # Data processing for multiple sweeps
        print("Running through looped data")
        print("There are ", num_sweeps, " loops within this data")

        # splits the loops depending on the number of sweeps
        split_v_data, split_c_data = split_loops(v_data, c_data, num_sweeps)
        # Calculates the metrics for each array returning the areas
        ps_areas, ng_areas, areas, normalized_areas, ron, roff, von, voff = calculate_metrics_for_loops(split_v_data, split_c_data)
        # have it plot each sweep individually for each loop number 1 to n
        # create a folder named as the file name with the images of each saved inside.


        # create dataframe for a device of all the data
        areas_loops = {'ps_area': ps_areas,
                       'ng_area': ng_areas,
                       'areas': areas,
                       'normalised_areas': normalized_areas,
                       }
        # areas_loops = pd.DataFrame(areas_loops)

        # Calculate the average values for each array
        ps_area_avg = sum(ps_areas) / len(ps_areas)
        ng_area_avg = sum(ng_areas) / len(ng_areas)
        areas_avg = sum(areas) / len(areas)
        normalized_areas_avg = sum(normalized_areas) / len(normalized_areas)
        ron_avg = sum(ron) / len(ron)
        roff_avg = sum(roff) / len(roff)
        von_avg = sum(von) / len(von)
        voff_avg = sum(voff) / len(voff)

        # Create a dictionary for the new DataFrame
        info = {
            'ps_area_avg': [ps_area_avg],
            'ng_area_avg': [ng_area_avg],
            'areas_avg': [areas_avg],
            'normalized_areas_avg': [normalized_areas_avg],
            'resistance_on_value': ron_avg,
            'resistance_off_value': roff_avg,
            'voltage_on_value': von_avg,
            'voltage_off_value': voff_avg,
        }

        # Create a new DataFrame
        # info = pd.DataFrame(info)

        # Analyze the array changes
        percent_change, avg_change, avg_relative_change, std_relative_change = analyze_array_changes(normalized_areas)

        # create dataframe for device of all the data
        looped_array_info = {'percentage_change': percent_change,
                             'avg_change': avg_change,
                             'avg_relative_change': avg_relative_change,
                             'stf_relative_change': std_relative_change}
        # looped_array_info = pd.DataFrame(looped_array_info)

        # print(f"Percentage change over the length: {percent_change:.5f}%")
        # print(f"Average change over time: {avg_change:.2e}")
        # print(f"Average relative change: {avg_relative_change:.5e}")
        # print(f"Standard deviation of relative change: {std_relative_change:.5e}")


        # print variable names dd too dataframe
        for variable_name, folder_name in file_info.items():
            df[variable_name] = folder_name

        f.check_if_folder_exists(device_path, "python_images")

        save_loc = device_path + '\\' + "python_images"

        graph_dict = {}
        if plot_graph:
            p = plot.plot(df, file_info, save_loc, filepath)
            graph = p.main_plot()
            # p.fig.savefig(f"{file_info.get('file_name')}.png")
            # print("saved graph too" , "###insert file path###")
            # this will plot graphs specific too looped data
        else:
            graph = None

        # for loops save file within a folder then  the next bit acan access it and open it
        if save_df:
            # save the sada frame
            print(long_name)
            df.to_csv(long_name, index=False)

        # plots the changes over time for each array and the loops.
        # plot_array_changes(normalized_areas)
        # info = None

    # this is for later
    if num_sweeps == 0.5:
        print("skipping as half sweep")
        return None
    else:
        # Data Processing for a single sweep
        print("data contains only one sweep")
        # if the xcell document states capacitive return
        ps_area, ng_area, area, normalized_area = area_under_curves(v_data, c_data)
        print("total info enclosed within the hysteresis normalised to voltage = ", normalized_area)
        # this info will need passing back to another array for comparision across all devices in the section
        # create dataframe for the device of all the data
        resistance_on_value, resistance_off_value, voltage_on_value, voltage_off_value = statistics(v_data, c_data)
        info = {'ps_area': ps_area,
                'ng_area': ng_area,
                'area': area,
                'normalised_areas': normalized_area,
                'resistance_on_value': resistance_on_value,
                'resistance_off_value': resistance_off_value,
                'voltage_on_value': voltage_on_value,
                'voltage_off_value': voltage_off_value,
                }
        # info = pd.DataFrame(info)

        f.check_if_folder_exists(device_path, "python_images")
        save_loc = os.path.join(device_path, "python_images")

        graph_dict = {}
        if plot_graph:
            p = plot.plot(df, file_info, save_loc, filepath)
            graph = p.main_plot()
        else:
            graph = None

        if save_df:
            # save the sada frame
            print(long_name)
            df.to_csv(long_name, index=False)
        areas_loops = None
        looped_array_info = None
    return file_info, num_sweeps, short_name, long_name, df, info, graph


def split_loops(v_data, c_data, num_loops):
    """ splits the looped data and outputs each sweep as another array"""
    total_length = len(v_data)  # Assuming both v_data and c_data have the same length
    size = total_length // num_loops  # Calculate the size based on the number of loops

    # Convert size to integer
    size = int(size)

    # Handle the case when the division leaves a remainder
    if total_length % num_loops != 0:
        size += 1

    split_v_data = [v_data[i:i + size] for i in range(0, total_length, size)]
    split_c_data = [c_data[i:i + size] for i in range(0, total_length, size)]

    # Print the number of arrays and their lengths
    # for idx, (sub_v_array, sub_c_array) in enumerate(zip(split_v_data, split_c_data)):
    #     print(f"Split Array {idx + 1}:")
    #     print(f"v_data Length: {len(sub_v_array)}")
    #     print(f"c_data Length: {len(sub_c_array)}")
    #     print("------")

    # # Print each split array in split_v_data
    # print("Split Arrays for v_data:")
    # for idx, array in enumerate(split_v_data):
    #     print(f"Split Array {idx + 1}: {array}")

    # Print a separator
    # print("\n" + "-" * 40 + "\n")
    #
    # # Print each split array in split_c_data
    # print("Split Arrays for c_data:")
    # for idx, array in enumerate(split_c_data):
    #     print(f"Split Array {idx + 1}: {array}")

    return split_v_data, split_c_data


def analyze_array_changes(arr):
    ''' calculate the array changes for each of the values of enclosed area'''

    # Calculate the percentage change over the length
    percent_change = ((arr[-1] - arr[0]) / arr[0]) * 100

    # Calculate the average change over time
    avg_change = (arr[-1] - arr[0]) / (len(arr) - 1)

    # Compute relative changes between consecutive elements
    relative_changes = np.diff(arr) / arr[:-1]

    # Calculate statistics
    avg_relative_change = np.mean(relative_changes)
    std_relative_change = np.std(relative_changes)

    return percent_change, avg_change, avg_relative_change, std_relative_change


def calculate_metrics_for_loops(split_v_data, split_c_data):
    '''
    Calculate various metrics for each split array of voltage and current data.
    anything that needs completing on loops added in here

    Parameters:
    - split_v_data (list of lists): List containing split voltage arrays
    - split_c_data (list of lists): List containing split current arrays

    Returns:
    - ps_areas (list): List of PS areas for each split array
    - ng_areas (list): List of NG areas for each split array
    - areas (list): List of total areas for each split array
    - normalized_areas (list): List of normalized areas for each split array
    '''

    # Initialize lists to store the values for each metric
    ps_areas = []
    ng_areas = []
    areas = []
    normalized_areas = []
    ron = []
    roff = []
    von = []
    voff = []

    # Loop through each split array
    for idx in range(len(split_v_data)):
        sub_v_array = split_v_data[idx]
        sub_c_array = split_c_data[idx]

        # Call the area_under_curves function for the current split arrays
        ps_area, ng_area, area, norm_area = area_under_curves(sub_v_array, sub_c_array)

        # Append the values to their respective lists
        ps_areas.append(ps_area)
        ng_areas.append(ng_area)
        areas.append(area)
        normalized_areas.append(norm_area)

        r_on, r_off, v_on, v_off = statistics(sub_v_array, sub_c_array)

        ron.append(r_on)
        roff.append(r_off)
        von.append(v_on)
        voff.append(v_off)

        # Print the values for the current split array
        # print(f"Metrics for split array {idx + 1}:")
        # print(f"PS Area Enclosed: {ps_area}")
        # print(f"NG Area Enclosed: {ng_area}")
        # print(f"Total Area Enclosed: {area}")
        # print(f"Normalized Area Enclosed: {norm_area}")
        # print("------")

    # Print the lists of values
    # print("\nList of PS Areas:", ps_areas)
    # print("List of NG Areas:", ng_areas)
    # print("List of Total Areas:", areas)
    #print("List of Normalized Areas:", normalized_areas)

    # Return the calculated metrics
    return ps_areas, ng_areas, areas, normalized_areas, ron, roff, von, voff


def area_under_curves(v_data, c_data):
    """
    only run this for an individual sweep
    :return: ps_area_enclosed,ng_area_enclosed,total_area_enclosed
    """
    # finds v max and min
    v_max, v_min = bounds(v_data)

    # creates dataframe of the sweep in sections
    df_sections = split_data_in_sect(v_data, c_data, v_max, v_min)

    # calculate the area under the curve for each section
    sect1_area = abs(area_under_curve(df_sections.get('voltage_ps_sect1'), df_sections.get('current_ps_sect1')))
    sect2_area = abs(area_under_curve(df_sections.get('voltage_ps_sect2'), df_sections.get('current_ps_sect2')))
    sect3_area = abs(area_under_curve(df_sections.get('voltage_ng_sect1'), df_sections.get('current_ng_sect1')))
    sect4_area = abs(area_under_curve(df_sections.get('voltage_ng_sect2'), df_sections.get('current_ng_sect2')))

    # plot to show where each section is on the hysteresis
    # plt.plot(df_sections.get('voltage_ps_sect1'), df_sections.get('current_ps_sect1'),color="blue" )
    # plt.plot(df_sections.get('voltage_ps_sect2'), df_sections.get('current_ps_sect2'),color="green")
    # plt.plot(df_sections.get('voltage_ng_sect1'), df_sections.get('current_ng_sect1'),color="red")
    # plt.plot(df_sections.get('voltage_ng_sect2'), df_sections.get('current_ng_sect2'),color="yellow")
    # #plt.legend()
    # plt.show()
    # plt.pause(0.1)

    # blue - green
    # red - yellow

    ps_area_enclosed = abs(sect1_area) - abs(sect2_area)
    ng_area_enclosed = abs(sect4_area) - abs(sect3_area)
    area_enclosed = ps_area_enclosed + ng_area_enclosed
    norm_area_enclosed = area_enclosed / (abs(v_max) + abs(v_min))
    return ps_area_enclosed, ng_area_enclosed, area_enclosed, norm_area_enclosed


def split_data_in_sect(voltage, current, v_max, v_min):
    # splits the data into sections and clculates the area under the curve for how "memeristive" a device is.
    zipped_data = list(zip(voltage, current))

    positive = [(v, c) for v, c in zipped_data if 0 <= v <= v_max]
    negative = [(v, c) for v, c in zipped_data if v_min <= v <= 0]

    # Find the maximum length among the four sections
    max_len = max(len(positive), len(negative))

    # Split positive section into two equal parts
    positive1 = positive[:max_len // 2]
    positive2 = positive[max_len // 2:]

    # Split negative section into two equal parts
    negative3 = negative[:max_len // 2]
    negative4 = negative[max_len // 2:]

    # Find the maximum length among the four sections
    max_len = max(len(positive1), len(positive2), len(negative3), len(negative4))

    # Calculate the required padding for each section
    pad_positive1 = max_len - len(positive1)
    pad_positive2 = max_len - len(positive2)
    pad_negative3 = max_len - len(negative3)
    pad_negative4 = max_len - len(negative4)

    # Limit the padding to the length of the last value for each section
    last_positive1 = positive1[-1] if positive1 else (0, 0)
    last_positive2 = positive2[-1] if positive2 else (0, 0)
    last_negative3 = negative3[-1] if negative3 else (0, 0)
    last_negative4 = negative4[-1] if negative4 else (0, 0)

    positive1 += [last_positive1] * pad_positive1
    positive2 += [last_positive2] * pad_positive2
    negative3 += [last_negative3] * pad_negative3
    negative4 += [last_negative4] * pad_negative4

    # Create DataFrame for device
    sections = {
        'voltage_ps_sect1': [v for v, _ in positive1],
        'current_ps_sect1': [c for _, c in positive1],
        'voltage_ps_sect2': [v for v, _ in positive2],
        'current_ps_sect2': [c for _, c in positive2],
        'voltage_ng_sect1': [v for v, _ in negative3],
        'current_ng_sect1': [c for _, c in negative3],
        'voltage_ng_sect2': [v for v, _ in negative4],
        'current_ng_sect2': [c for _, c in negative4],
    }

    df_sections = pd.DataFrame(sections)
    return df_sections


def area_under_curve(voltage, current):
    """
    Calculate the area under the curve given voltage and current data.
    """

    # print(voltage,current)
    voltage = np.array(voltage)
    current = np.array(current)
    # Calculate the area under the curve using the trapezoidal rule
    area = np.trapz(current, voltage)
    # which ever is in np.trapz(y,x), Using a decreasing x corresponds to integrating in reverse: ie negative value?
    return area


def bounds(data):
    """
    :param data:
    :return: max and min values of given array max,min
    """
    max = np.max(data)
    min = np.min(data)
    return max, min


def check_for_loops(v_data):
    """
    :param v_data:
    :return: number of loops for given data set
    """
    # looks at max voltage and min voltage if they are seen more than twice it classes it as a loop
    # checks for the number of zeros 3 = single loop
    num_max = 0
    num_min = 0
    num_zero = 0
    max_v, min_v = bounds(v_data)
    max_v_2 = max_v / 2
    min_v_2 = min_v / 2

    # 4 per sweep
    for value in v_data:
        if value == max_v_2:
            num_max += 1
        if value == min_v_2:
            num_min += 1
        if value == 0:
            num_zero += 1
    #print(num_min)

    # print("num zero", num_zero)
    if num_max + num_min == 4:
        #print("single sweep")
        return 1
    if num_max + num_min == 2:
        #print("half_sweep", num_max, num_min)
        return 0.5
    else:
        #print("multiloop", (num_max + num_min) / 4)
        loops = (num_max + num_min) / 4
        return loops
    # used for checking with just positive and negative vlaues
    # if num_max <= 2:
    #     print("Single sweep", num_max)
    #     return 1
    # if num_max <= 1:
    #     print("half sweep", num_max)
    #     return 0.5
    # else:
    #     loops = num_max / 2


def split_iv_sweep(filepath):
    # print(f"{filepath_for_single_sweep}")
    with open(filepath, "r") as f:  # open the file as read only
        fread = f.readlines()
        fread.pop(0)
    # B = self.filereader()
    # B = fm.directory(self.filepath_for_single_sweep).filereader()
    Data = []
    for i, line in enumerate(fread):
        C = (line.split('\t'))
        D = []
        for value in C:
            if value != '':
                D.append(float(value))
        Data.append(D)
    v_data_array = []
    c_data_array = []
    for value in Data:
        if value:
            v_data_array.append(value[0])
            c_data_array.append(value[1])
    if len(v_data_array) == 0 or len(v_data_array) < 10:
        print('not enough data', filepath)
        return None
    return v_data_array, c_data_array


## ------------------------------------------------------------------------------------##

# Equations for manipulating data
def absolute_val(col):
    '''Returns the absolute value of inputted value'''
    return [abs(x) for x in col]


def filter_positive_values(v_data, c_data):
    ''' Takes the data given too it within the class (current and voltage arrays)
    and returns only the positive values in place of zeros if they are negative '''
    result_voltage_ps = []
    result_current_ps = []

    for v, c in zip(v_data, c_data):
        if v >= 0:
            result_voltage_ps.append(v)
            result_current_ps.append(c)
        else:
            result_voltage_ps.append(0)
            result_current_ps.append(0)

    return result_voltage_ps, result_current_ps


def filter_negative_values(v_data, c_data):
    ''' Takes the data given too it within the class (current and voltage arrays)
    and returns only the negative values in place of zeros if they are positive
    takes arrays '''
    result_voltage_ng = []
    result_current_ng = []
    for v, c in zip(v_data, c_data):
        if v <= 0:
            result_voltage_ng.append(v)
            result_current_ng.append(c)
        else:
            result_voltage_ng.append(0)
            result_current_ng.append(0)

    return absolute_val(result_voltage_ng), absolute_val(result_current_ng)


def zero_devision_check(x, y):
    try:
        return x / y
    except ZeroDivisionError:
        return 0


# equations for all data within this class

def resistance(v_data, c_data):
    ''' takes voltage data and current data arrays returns resistance array'''
    resistance = []
    for i in range(len(v_data)):
        resistance.append(zero_devision_check(v_data[i], c_data[i]))
    return resistance


# there is an error ocurring here C:\Users\Craig-Desktop\PycharmProjects\new yes_and_no_sort\Class_single_sweep.py:157: RuntimeWarning: invalid value encountered in log
# result = np.log(self.resistance[i]) im unsure why

def log_value(array):
    ''' takes an array returns an array of logged values'''
    log_value = []
    for i in range(len(array)):
        # checks for 0 value and if there is a zero value it returns 0 instead of loging it
        if array[i] != 0:
            result = np.log(array[i])
            log_value.append(result)
        else:
            result = 0  # or any other suitable value
            log_value.append(result)
    return log_value


def current_density_eq(v_data, c_data, distance=100E-9, area=100E-6):
    ''' Returns current density array using the current and voltage data arrays'''
    current_density = []
    for voltage, current in zip(v_data, c_data):
        if voltage == 0 or current == 0:
            current_density.append(0)
            # for checking for divide by zero error
            continue
        new_num = (distance / ((voltage / current) * area ** 2)) * (voltage / distance)
        current_density.append(new_num)
    return current_density


def electric_field_eq(v_data, distance=100E-9):
    """Returns electric field array data given the voltage array"""
    electric_field = []
    for voltage in v_data:
        if voltage == 0:
            electric_field.append(0)
            continue
        new_num = voltage / distance
        electric_field.append(new_num)
    return electric_field


def inverse_resistance_eq(v_data, c_data):
    '''Take the array of voltage and current and Divides current and voltage together'''
    # v_data & c_data cant be refered to as self as this needs
    # positive or negative values only
    inverse_resistance = []
    for voltage, current in zip(v_data, c_data):
        if voltage == 0 or current == 0:
            inverse_resistance.append(0)
            # for checking for divide by zero error
            continue
        new_num = current / voltage
        inverse_resistance.append(new_num)
    return inverse_resistance


def sqrt_array(value_array):
    """sqr roots the Value given"""
    sqrt_array = []
    for voltage in value_array:
        new_num = voltage ** 1 / 2
        sqrt_array.append(new_num)
    return sqrt_array


# todo change this from class too other
def statistics(v_data, c_data):
    """
    calculates r on off and v on off values for an individual device
    """
    resistance_on_value = []
    resistance_off_value = []
    voltage_on_value = []
    voltage_off_value = []
    # if this breaks maybe add max v / x number
    # this will need changing later dependent on the max voltage used
    thresh = 0.2

    # voltage and current magnitude
    voltage_mag = []
    current_mag = []
    if not len(v_data) < 10:
        for value in range(len(v_data)):
            if -thresh < v_data[value] < thresh:
                voltage_mag.append(v_data[value])
                current_mag.append(c_data[value])

        res_mag = []  # same here but for the resistances
        for j in range(len(voltage_mag)):
            if voltage_mag[j] != 0:
                res_mag.append(voltage_mag[j] / current_mag[j])

        if not len(v_data) < 10:
            roff = min(res_mag)
            ron = max(res_mag)
        else:
            roff = 0
            ron = 0

        resistance_off_value = roff
        resistance_on_value = ron

        grads = []
        for j in range(len(v_data)):
            if j != len(v_data) - 1:
                if v_data[j + 1] - v_data[j] != 0:
                    grads.append((c_data[j + 1] - c_data[j]) / (v_data[j + 1] - v_data[j]))

        max_grad = max(grads[:(int(len(grads) / 2))])
        min_grad = min(grads)

        for j in range(len(grads)):
            if grads[j] == max_grad:
                voltage_off = v_data[j]
            if grads[j] == min_grad:
                voltage_on = v_data[j]

        voltage_on_value = voltage_on
        voltage_off_value = voltage_off

    # print (resistance_on_value, resistance_off_value, voltage_on_value , voltage_off_value)
    return resistance_on_value, resistance_off_value, voltage_on_value, voltage_off_value
    # else:
    #     return 0, 0, 0, 0


def set_pandas_display_options() -> None:
    """Set pandas display options."""
    # Ref: https://stackoverflow.com/a/52432757/
    display = pd.options.display

    display.max_columns = 1000
    display.max_rows = 1000
    display.max_colwidth = 199
    display.width = 1000
    # display.precision = 2  # set as needed
    # display.float_format = lambda x: '{:,.2f}'.format(x)  # set as needed
