import numpy as np

# All the Equations for manipulating data

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


def log_value(array):
    """
    Takes an array and returns an array of the logged values.
    If a value is zero, the function returns zero instead of taking the natural logarithm.
    """
    log_value = []
    for i in range(len(array)):
        if array[i] != 0:
            result = np.log(abs(array[i]))
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
