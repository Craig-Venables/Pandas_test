import numpy as np
import pandas as pd
import math
from file import filepath
import matplotlib.pyplot as plt
from itertools import zip_longest
debugging = False


''' all the data manipulation goes here including any dataframe manipulation 
 '''

def split_loops(v_data,c_data,num_loops):
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
    print("\n" + "-" * 40 + "\n")

    # Print each split array in split_c_data
    print("Split Arrays for c_data:")
    for idx, array in enumerate(split_c_data):
        print(f"Split Array {idx + 1}: {array}")

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

    return percent_change, avg_change,avg_relative_change, std_relative_change

def calculate_metrics_for_loops(split_v_data, split_c_data):
    '''
    Calculate various metrics for each split array of voltage and current data.

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
    print("List of Normalized Areas:", normalized_areas)

    # Return the calculated metrics
    return ps_areas, ng_areas, areas, normalized_areas

def area_under_curves(v_data,c_data):
    """
    only run this for an individual sweep
    :return: ps_area_enclosed,ng_area_enclosed,total_area_enclosed
    """
    # finds v max and min
    v_max,v_min = bounds(v_data)
    print("Voltage max and min", v_max,v_min)
    # creates dataframe of the sweep in sections
    df_sections = split_data_in_sect(v_data,c_data,v_max,v_min)



    #calculate the area under the curve for each section
    sect1_area = abs(area_under_curve(df_sections.get('voltage_ps_sect1'),df_sections.get('current_ps_sect1')))
    sect2_area = abs(area_under_curve(df_sections.get('voltage_ps_sect2'), df_sections.get('current_ps_sect2')))
    sect3_area = abs(area_under_curve(df_sections.get('voltage_ng_sect1'), df_sections.get('current_ng_sect1')))
    sect4_area = abs(area_under_curve(df_sections.get('voltage_ng_sect2'), df_sections.get('current_ng_sect2')))

    #plot to show where each section is on the hysteresis
    # plt.plot(df_sections.get('voltage_ps_sect1'), df_sections.get('current_ps_sect1'),color="blue" )
    # plt.plot(df_sections.get('voltage_ps_sect2'), df_sections.get('current_ps_sect2'),color="green")
    # plt.plot(df_sections.get('voltage_ng_sect1'), df_sections.get('current_ng_sect1'),color="red")
    # plt.plot(df_sections.get('voltage_ng_sect2'), df_sections.get('current_ng_sect2'),color="yellow")
    # #plt.legend()
    # plt.show()
    # plt.pause(0.1)

    #blue - green
    #red - yellow

    ps_area_enclosed = abs(sect1_area) - abs(sect2_area)
    ng_area_enclosed = abs(sect4_area) - abs(sect3_area)
    area_enclosed = ps_area_enclosed + ng_area_enclosed
    print("total voltage",(abs(v_max) + abs(v_min)))
    print(ng_area_enclosed,ps_area_enclosed)
    norm_area_enclosed = area_enclosed / (abs(v_max) + abs(v_min))
    return ps_area_enclosed,ng_area_enclosed,area_enclosed,norm_area_enclosed

def split_data_in_sect(voltage, current, v_max, v_min):
    # splits the data into sections and clculates the area under the curve for how "memeristive" a device is.
    zipped_data = list(zip(voltage, current))

    positive = [(v, c) for v, c in zipped_data if 0 <= v <= v_max]
    negative = [(v, c) for v, c in zipped_data if v_min <= v <= 0]

    print("Length of positive and negative arrays:", len(positive), len(negative))

    # Find the maximum length among the four sections
    max_len = max(len(positive), len(negative))
    # Check if max_len is odd and adjust
    # if max_len % 2 != 0:
    #     max_len += 1
    # max_len//= 2

    print(max_len, type(max_len))


    # Split positive section into two equal parts
    positive1 = positive[:max_len // 2]
    positive2 = positive[max_len // 2:]

    # Split negative section into two equal parts
    negative3 = negative[:max_len // 2]
    negative4 = negative[max_len // 2:]
    #
    # Pad shorter sections to ensure equal lengths
    last_positive = positive[-1] if positive else (0, 0)
    last_negative = negative[-1] if negative else (0, 0)

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

    # print("----")
    # print("this is all the sections of the hysteresis")
    # print(positive1)
    # print(len(positive1))
    # print(positive2)
    # print(len(positive2))
    #
    # print(negative3)
    # print(len(negative3))
    # print(negative4)
    # print(len(negative4))
    # print("----")
    # df_sections = pd.DataFrame(sections)
    # print(df_sections)

    df_sections = pd.DataFrame(sections)
    #print(df_sections)
    return df_sections


def area_under_curve (voltage,current):
    """
    Calculate the area under the curve given voltage and current data.
    """

    #print(voltage,current)
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
    return max,min

def check_for_loops(v_data):
    """
    :param v_data:
    :return: number of loops for given data set
    """
    # looks at max voltage and min voltage if they are seen more than twice
    # it classes it as a loop
    num = 0
    max_v, min_v = bounds(v_data)
    for value in v_data:
        if value == max_v:
            num += 1
    if num <= 2:
        print("Single sweep")
        return 1

    else:
        loops = num/2
        return loops


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

def filter_positive_values(v_data,c_data):
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

def filter_negative_values(v_data,c_data):
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

def resistance(v_data,c_data):
    ''' takes voltage data and current data arrays returns resistance array'''
    resistance = []
    for i in range(len(v_data)):
        resistance.append(zero_devision_check(v_data[i],c_data[i]))
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

def current_density_eq(v_data, c_data,distance=100E-9,area=100E-6):
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

#todo change this from class too other 
def statistics(self):
    """
    calculates r on off and v on off values for an individual device
    """
    resistance_on_value = []
    resistance_off_value = []
    voltage_on_value = []
    voltage_off_value = []
    # if this breaks maybe add max v / x number
    #this will need changing later dependent on the max voltage used
    thresh = 0.2

    # voltage and current magnitude
    voltage_mag = []
    current_mag = []
    if not len(self.v_data) < 10:
        for value in range(len(self.v_data)):
            if -thresh < self.v_data[value] < thresh:
                voltage_mag.append(self.v_data[value])
                current_mag.append(self.c_data[value])

        res_mag = []  # same here but for the resistances
        for j in range(len(voltage_mag)):
            if voltage_mag[j] != 0:
                res_mag.append(voltage_mag[j] / current_mag[j])


        if not len(self.v_data) < 10:
            roff = min(res_mag)
            ron = max(res_mag)
        else:
            roff = 0
            ron = 0


        resistance_off_value = roff
        resistance_on_value = ron

        grads = []
        for j in range(len(self.v_data)):
            if j != len(self.v_data) - 1:
                if self.v_data[j + 1] - self.v_data[j] != 0:
                    grads.append((self.c_data[j + 1] - self.c_data[j]) / (self.v_data[
                                                                              j + 1] - self.v_data[j]))

        max_grad = max(grads[:(int(len(grads) / 2))])
        min_grad = min(grads)

        for j in range(len(grads)):
            if grads[j] == max_grad:
                voltage_off = self.v_data[j]
            if grads[j] == min_grad:
                voltage_on = self.v_data[j]

        voltage_on_value = voltage_on
        voltage_off_value = voltage_off
    else:
        return 0, 0, 0, 0

    # print (resistance_on_value, resistance_off_value, voltage_on_value , voltage_off_value)
    return resistance_on_value, resistance_off_value, voltage_on_value, voltage_off_value


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
