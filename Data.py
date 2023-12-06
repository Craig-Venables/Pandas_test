import numpy as np
import pandas as pd
from file import filepath
import matplotlib.pyplot as plt
from itertools import zip_longest
debugging = False


''' all the data manipulation goes here including any dataframe manipulation 
 '''



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

    # plot to show where each section is on the hysteresis
    # plt.plot(df_sections.get('voltage_ps_sect1'), df_sections.get('current_ps_sect1'),color="blue" )
    # plt.plot(df_sections.get('voltage_ps_sect2'), df_sections.get('current_ps_sect2'),color="green")
    # plt.plot(df_sections.get('voltage_ng_sect1'), df_sections.get('current_ng_sect1'),color="red")
    # plt.plot(df_sections.get('voltage_ng_sect2'), df_sections.get('current_ng_sect2'),color="yellow")
    # plt.legend()
    # plt.show()
    # plt.pause(0.1)

    #blue - green
    #red - yellow

    ps_area_enclosed = sect1_area - sect2_area
    ng_area_enclosed = sect3_area - sect4_area
    total_area_enclosed = (sect1_area - sect2_area) + (sect3_area - sect4_area)
    return ps_area_enclosed,ng_area_enclosed,total_area_enclosed

def split_data_in_sect(voltage, current,v_max,v_min):
    positive = [(v, c) for v, c in zip(voltage, current) if 0 <= v <= v_max]
    negative = [(v, c) for v, c in zip(voltage, current) if v_min <= v <= 0]

    # this makes sure that the arrays positive and negative are of the same length if not
    # it repeats the last value , this shouldn't have too much of an effect on the result
    len_positive, len_negative = len(positive), len(negative)
    if len_positive < len_negative:
        final_positive_value = positive[-1]
        positive += [final_positive_value] * (len_negative - len_positive)
    elif len_negative < len_positive:
        final_negative_value = negative[-1]
        negative += [final_negative_value] * (len_positive - len_negative)

    positive1 = list(zip(*positive[:len(positive)//2]))
    positive2 = list(zip(*positive[len(positive)//2:]))

    negative1 = list(zip(*negative[:len(negative)//2]))
    negative2 = list(zip(*negative[len(negative)//2:]))

    # create dataframe for device
    sections = {'voltage_ps_sect1': positive1[0],
                'current_ps_sect1': positive1[1],
                'voltage_ps_sect2': positive2[0],
                'current_ps_sect2': positive2[1],
                'voltage_ng_sect1': negative1[0],
                'current_ng_sect1': negative1[1],
                'voltage_ng_sect2': negative2[0],
                'current_ng_sect2': negative2[1]}

    df_sections = pd.DataFrame(sections)
    return df_sections

def area_under_curve (voltage,current):
    """
    Calculate the area under the curve given voltage and current data.
    """
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
        print ("There are ", loops , " loops within this data")
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
