import numpy as np


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