import file as f
import pickle
import sys
from memristors import print_mem as p, currat_data as m
from file import Tee
import memristors.analysis as mem
import memristors.statistics_mem as stat_mem
import memristors.analysis_curated as curr
import memristors.Files_ as Files
import configparser

# to add
# - histogram all the data
# - reorganise the functions
# - keeo track of which files have been measured and wonr remeaure them
# set mem_print to just print instead of specifying for memristors


# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Set the environment (HOME_PC or LAPTOP)
environment = 'HOME_PC'  # Change to 'LAPTOP' or 'NOTTS_PC' as needed

# Get the paths from the config file
excel_path = config[environment]['excel_path']
main_dir = config[environment]['main_dir']
curr_data_path = config[environment]['curr_data_path']
template_for_device_xls_path = config[environment]['template_for_device_xls_path']

# Get the ignore files list and convert it to a tuple
ignore_files_str = config['IGNORE_FILES']['files']
ignore_files = tuple(ignore_files_str.split(', '))


# Print paths to verify (optional)
print(f"Excel Path: {excel_path}")
print(f"Main Directory: {main_dir}")
print(f"Current Data Path: {curr_data_path}")
print(f"Template for Device XLS Path: {template_for_device_xls_path}")

# Initial Params
memristors_data = True  # analysis all raw data
currated = False   # analyses curated data

plot_graph = True
plot_gif = False
sort_graphs = False
# Plot all the data into origin?
origin_graphs = False
pull_fabrication_info_excell = True
save_df = False
re_save_graph = False
re_analyse = True

# Params Dictionary
params = f.create_params_dict(plot_graph, plot_gif, sort_graphs, origin_graphs,
                              pull_fabrication_info_excell, save_df, re_save_graph, re_analyse)

# Open a file for writing with utf-8 encoding
output_file = open(main_dir + 'printlog.txt', 'w', encoding='utf-8')
# Redirect print output to both the file and the console
sys.stdout = Tee(file=output_file, stdout=sys.stdout)
# set Pandas display options to display all data in dataframe?
mem.set_pandas_display_options()

# This is for Memristors, create a new one for other device measurements
if memristors_data:
    material_stats_dict, material_sweeps_dict, material_data, file_info_dict = mem.memristor_devices(main_dir, params,excel_path)
else:
    print("not analysing")


# Load in the material_stats_dict data
with open(main_dir + '/material_stats_dict_all.pkl', 'rb') as file:
    material_stats_dict = pickle.load(file)

# Load material_sweeps_dict
with open(main_dir + '/material_sweeps_dict_all.pkl', 'rb') as file:
    material_sweeps_dict = pickle.load(file)

# Load material_data
with open(main_dir + '/material_data_all.pkl', 'rb') as file:
    material_data = pickle.load(file)

with open(main_dir + '/file_info_dict.pkl', 'rb') as file:
    file_info_dict = pickle.load(file)

print('-' * 25)
print("")
print('-' * 25)
print("access files using the following")
print("material_sweeps_dict(['stock'][[f'{polymer}'][f'{sample_name}'][['section']['device_number'])")
print("material_data['Stock'][f'{polymer}'][f'{sample_name}']['G 200µm']['1']['1-Fs_0.5v_0.01s.txt']")
print('-' * 25)
print("")
print("Finished sample analysis below is information about the samples")
print("")

# needs to sort the data here, taking the data_dict and file_info_dict but full (see above) parsing through and
# material_sweeps_dict = Contains all the sweeps per device along with the classification
# material_data = Contains all the data extracted from the sweep (Voltage,current,abs_current etc....)


# For sorting the graphs and copying the data
if sort_graphs:
    print("Sorting graphs")
    m.data_copy(material_data,main_dir)
    #origin.plot_in_origin(device_data, device_path, 'transport')

if currated:
    #curr_data_path = r"C:\Users\Craig-Desktop\OneDrive - The University of Nottingham\Documents\Phd\1) Projects\1) Memristors\1) Curated Data"
    curr.currated_data(curr_data_path)

############################################################################
# All sweeps analysed at this point stats are done below
# A Breakpoint below does all the stats on the device
# VERY CRUDE JUST PRINTS EVERYTHING DOS-NT SAVE ANYTHING YET
############################################################################

# Calculate yield for each sample
p.yield_calc(material_sweeps_dict)  # prints yield on each sample

# Sample with the most sweeps, corresponding sample and its sweeps in high to low and prints
sample_sweeps = stat_mem.get_num_sweeps_ordered(file_info_dict, material_sweeps_dict)
p.top_10_measured(sample_sweeps)  # prints top 10 measured samples

# Call the function to process 'ON_OFF_Ratio'
on_off_ratio_info = Files.process_property(material_stats_dict, 'ON_OFF_Ratio')
# Call the function to process 'normalised_area'
normalised_area_info = Files.process_property(material_stats_dict, 'normalised_area')

# print the values from above
p.print_on_off_ratio_info(on_off_ratio_info)
p.print_normalised_area_info(normalised_area_info)

# Call the function to find the top 10 samples based on ON-OFF ratio
on_off_ratio_info, top_samples_with_repetition_on_off, top_samples_without_repetition_on_off = stat_mem.find_top_samples(
    material_stats_dict, property_name='ON_OFF_Ratio')

# Call the function to find the top 10 samples based on normalized area
normalized_area_info, top_samples_with_repetition_normalized, top_samples_without_repetition_normalized = stat_mem.find_top_samples(
    material_stats_dict, property_name='normalised_area')

# Print the results for ON-OFF ratio
print("Top Samples (With Repetition) - ON-OFF Ratio:")
for idx, sample_info in enumerate(on_off_ratio_info[:10], start=1):
    print(
        f"#{idx}: Sample: {sample_info['sample_key']}, Section: {sample_info['section_key']}, Device: {sample_info['device_key']}, File Name: {sample_info['file_name']}, ON-OFF Ratio: {sample_info['property_value']}")

print("\nTop Samples (Without Repetition) - ON-OFF Ratio:")
for idx, sample_key in enumerate(top_samples_without_repetition_on_off[:10], start=1):
    # Find the corresponding sample info for samples without repetition
    sample_info = next(info for info in on_off_ratio_info if info['sample_key'] == sample_key)
    print(
        f"#{idx}: Sample: {sample_info['sample_key']}, Section: {sample_info['section_key']}, Device: {sample_info['device_key']}, File Name: {sample_info['file_name']}, ON-OFF Ratio: {sample_info['property_value']}")

# Print the results for normalized area
print("\nTop Samples (With Repetition) - Normalized Area:")
for idx, sample_info in enumerate(normalized_area_info[:10], start=1):
    print(
        f"#{idx}: Sample: {sample_info['sample_key']}, Section: {sample_info['section_key']}, Device: {sample_info['device_key']}, File Name: {sample_info['file_name']}, Normalized Area: {sample_info['property_value']}")

print("\nTop Samples (Without Repetition) - Normalized Area:")
for idx, sample_key in enumerate(top_samples_without_repetition_normalized[:10], start=1):
    # Find the corresponding sample info for samples without repetition
    sample_info = next(info for info in normalized_area_info if info['sample_key'] == sample_key)
    print(
        f"#{idx}: Sample: {sample_info['sample_key']}, Section: {sample_info['section_key']}, Device: {sample_info['device_key']}, File Name: {sample_info['file_name']}, Normalized Area: {sample_info['property_value']}")


"""

Dictionary's;


material_sweeps_dict = Contains all the sweeps per device along with the classification
material_data = Contains all the data extracted from the sweep (voltage,current,abs_current etc....)
material_stats_dict = Contains stats for each sweep including Area,Ron/roff,Von/off
yield_dict = Contains the yield for each Sample
yield_dict_sect = Contains the yield for each Section of a device
on_off_ratio_info = Contains the ON-OFF ratio for each Sample organised for each section device and sweep
normalized_area_info = Contains the normalized area for each sample organised for each section device and sweep
sample_sweeps = Contains the sweeps per sample organised into descending order


Per sample:  
(these are only applicable to current working sample and are not saved elsewhere.)
sample_sweep_excell_dict = PD dataframe Contains information for each device in sections i.e. Memristive 
fabrication_info_dict = information from the solutions and devices excell file - Per sample only 

As they sound:
top_samples_with_repetition_on_off = 
top_samples_without_repetition_on_off = 
top_samples_with_repetition_normalized = 
top_samples_without_repetition_normalized = 




# Pulls information on fabrication from excell file
fabrication_information_dict = exc.save_info_from_solution_devices_excell(sample_name, f.excel_path, sample_path)

"""
# fabrication_info_dict

# ##################################################################

# ignore below this line

##################################################################

# Close the file to ensure that everything is written
# output_file.close()


# if __name__ == '__main__':
#     #This is a piece of boilerplate code which you should write routinely when you create a script.
#     print('Since this is inside the if statement it will only run if you run this file and not it you import it')
#     #example_function()
# Close the file to ensure that everything is written
