import pandas as pd
import numpy
import os
import Equations as eq
import matplotlib.pyplot as plt
import plot as plot
import file as f

#filepath = r"C:\Users\ppxcv1\OneDrive - The University of Nottingham\Desktop\Origin Test Folder\top directory\sub directory 1\testfile.txt"
filepath = r"C:\Users\Craig-Desktop\Desktop\test folder for py\1) Memristors\Stock\PVA\Stock-PVA-Gold-Gold-7\G 200µm\1\forthesis.txt"

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


# i will need to add into here sample number that's extracted from sample_name



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
data = {'voltage': v_data,
        'current': c_data,
        'abs_current': eq.absolute_val(c_data),
        'resistance': eq.resistance(v_data, c_data),
        'voltage_ps': v_data_ps,
        'current_ps': c_data_ps,
        'voltage_ng': v_data_ng,
        'current_ng': c_data_ng,
        'log_Resistance': eq.log_value(eq.resistance(v_data, c_data)),
        'abs_Current_ps': eq.absolute_val(c_data_ps),
        'abs_Current_ng': eq.absolute_val(c_data_ng),
        'current_Density_ps': eq.current_density_eq(v_data_ps, c_data_ps),
        'current_Density_ng': eq.current_density_eq(v_data_ng, c_data_ng),
        'electric_field_ps': eq.electric_field_eq(v_data_ps),
        'electric_field_ng': eq.electric_field_eq(v_data_ng),
        'inverse_resistance_ps': eq.inverse_resistance_eq(v_data_ps, c_data_ps),
        'inverse_resistance_ng': eq.inverse_resistance_eq(v_data_ng, c_data_ng),
        'sqrt_Voltage': eq.sqrt_array(v_data),
        'on_off_ratio': eq.statistics}

# materials = {'test':f.name}


file_info = f.extract_folder_names(filepath)
for variable_name, folder_name in file_info.items():
    print(f"{variable_name} = '{folder_name}'")
print(file_info)

df = pd.DataFrame(data)
#display(df)
#print(df)

print(df.get("Voltage"))

# plt.plot(df.get("Voltage"), df.get("Current"), color='blue')
# # Add labels and a title
# plt.ylabel('Current')
# # plt.yscale("log")
# plt.xlabel('Voltage')
# plt.title('Voltage vs. Current Graph')
# plt.show()
#

p = plot.plot(df,file_info)
p.main_plot()

