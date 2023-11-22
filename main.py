import pandas as pd
import numpy
import os
import Equations as eq
import matplotlib.pyplot as plt

filepath = r"C:\Users\ppxcv1\OneDrive - The University of Nottingham\Desktop\Origin Test Folder\top directory\sub directory 1\testfile.txt"

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
set_pandas_display_options()

# For dealing with the file

def filereader(filepath):
    with open(filepath, "r") as f:  # open the file as read only
        fread = f.readlines()
        fread.pop(0)
        return fread


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


v_data, c_data = split_iv_sweep(filepath)
v_data_ps, c_data_ps = eq.filter_positive_values(v_data, c_data)
v_data_ng, c_data_ng = eq.filter_negative_values(v_data, c_data)

# # check arrays printing
# for i in range(len(v_data)):
#     print(v_data[i],c_data[i])


# # plot graph
# plt.plot(v_data, c_data, color='blue')
# # Add labels and a title
# plt.ylabel('Current')
# # plt.yscale("log")
# plt.xlabel('Voltage')
# plt.title('Voltage vs. Current Graph')
# plt.show()

# print(eq.current_density_eq(v_data,c_data))


#todo find a way to call the dataframe the name of the file and then save it appropratly

# data frame
data = {'Voltage': v_data,
        'Current': c_data,
        'Abs_Current': eq.absolute_val(c_data),
        'Resistance': eq.resistance(v_data, c_data),
        'Voltage_ps': v_data_ps,
        'Current_ps': c_data_ps,
        'Voltage_ng': v_data_ng,
        'Current_ng': c_data_ng,
        'log_Resistance': eq.log_value(eq.resistance(v_data, c_data)),
        'Abs_Current_Ps': eq.absolute_val(c_data_ps),
        'Abs_Current_ng': eq.absolute_val(c_data_ng),
        'Current_Density_Ps': eq.current_density_eq(v_data_ps, c_data_ps),
        'Current_Density_Ng': eq.current_density_eq(v_data_ng, c_data_ng),
        'Electric_field_Ps': eq.electric_field_eq(v_data_ps),
        'Electric_field_Ng': eq.electric_field_eq(v_data_ng),
        'Inverse_resistance_ps': eq.inverse_resistance_eq(v_data_ps, c_data_ps),
        'Inverse_resistance_ng': eq.inverse_resistance_eq(v_data_ng, c_data_ng),
        'Sqrt_Voltage': eq.sqrt_array(v_data),
        'on_off_ratio': eq.statistics}




df = pd.DataFrame(data)
#display(df)
print(df)

