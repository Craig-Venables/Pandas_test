import pandas as pd
import statistics
import numpy
import os
import Data as eq
import pdf as pdf
import matplotlib.pyplot as plt
import excell as exc
import plot as plot
import file as f
import pickle
import pprint
import math
import sys



class Tee:
    def __init__(self, file, stdout):
        self.file = file
        self.stdout = stdout
        self.closed = False

    def write(self, data):
        if not self.closed:
            self.file.write(data)
        self.stdout.write(data)

    def flush(self):
        if not self.closed:
            self.file.flush()
        self.stdout.flush()

    def close(self):
        if not self.closed:
            self.file.close()
            self.closed = True

from file import excel_path
import excell as ex

# pip install reportlab matplotlib

# to add
# Todo Statistics- pull data from the statisitcs sheet i fill out when measuring the devices
#  create a file that saves all the data collected from each device an sweeps within the data
# - histogram all the data
# - reorganise the functions
#

# have it created the origin graphs for all files towards the end, however only do this if there isn't already an origin
# file created for each

# images in, with a full overview of each create a final overview pdf of each device with all the sweeps information
# ie average enclosed area, average switching

# Open a file for writing with utf-8 encoding
output_file = open(f.main_dir + 'printlog.txt', 'w',encoding='utf-8')

# Redirect print output to both the file and the console
sys.stdout = Tee(file=output_file, stdout=sys.stdout)

# add check for nan values and



save_df = False
plot_graph = False
re_analyse = True
eq.set_pandas_display_options()

# Main for loop for parsing through folders
# empty dictionary's
material_stats_dict = {}
material_sweeps_dict = {}
material_data = {}
material_names_dict = {}
file_info_dict = {}
sample_name_arr = []

print("Starting...")

for material in os.listdir(f.main_dir):
    material_path = os.path.join(f.main_dir, material)
    if os.path.isdir(material_path):
        # Navigate through sub-folders (e.g., polymer)
        polymer_stats_dict = {}
        polymer_sweeps_dict = {}
        polymer_data = {}
        polymer_names_dict = {}
        for polymer in os.listdir(material_path):
            polymer_path = os.path.join(material_path, polymer)

            if os.path.isdir(polymer_path):
                # Navigate through sample_name folders
                sample_stats_dict = {}
                sample_sweeps_dict = {}
                sample_data = {}
                sample_names_dict = {}

                for sample_name in os.listdir(polymer_path):
                    sample_path = os.path.join(polymer_path, sample_name)
                    if os.path.isdir(sample_path):
                        # print("working on ", sample_name)
                        # print("Path = ", sample_path)

                        # Anything to device that doesn't require information on individual sweeps
                        # Sample name = ie D14-Stock-Gold-PVA(2%)-Gold-s7

                        # Pulls information from device sweep excell sheet
                        #sample_sweep_excell_dict = exc.save_info_from_device_info_excell(sample_name, sample_path)

                        # Pulls information on fabrication from excell file
                        #info_dict = exc.save_info_from_solution_devices_excell(sample_name, f.excel_path, sample_path)

                        # empty list for storing all measured devices
                        list_of_measured_files_devices_sections = []
                        section_stats_dict = {}
                        section_sweeps_dict = {}
                        section_data = {}

                        # Navigate through section folders
                        for section_folder in os.listdir(sample_path):
                            # Anything to section that doesn't require information on individual sweeps
                            section_path = os.path.join(sample_path, section_folder)
                            if os.path.isdir(section_path):
                                # Navigate through device_number folders
                                #print("working on ", sample_name, section_folder)

                                list_of_measured_files_devices = []
                                device_sweeps_dict = {}
                                device_stats_dict = {}
                                device_data = {}

                                for device_folder in os.listdir(section_path):
                                    device_path = os.path.join(section_path, device_folder)
                                    if os.path.isdir(device_path):
                                        # Working on individual devices
                                        # print("")
                                        #print("working in folder ", sample_name, section_folder, device_folder)
                                        # print("")


                                        # keeps a list of all files processed for each device
                                        list_of_measured_files = []
                                        list_of_file_stats = []
                                        list_of_areas_loops = []
                                        list_of_looped_array_info = []
                                        list_of_data_dfs = []
                                        list_of_graphs = []
                                        num_of_sweeps = 0
                                        file_data = {}

                                        # add more here into how each array changes over each array
                                        # Process each file in the device_number folder
                                        for file_name in os.listdir(device_path):
                                            if file_name.endswith('.txt'):
                                                # Does work on the file here
                                                # checks If in excell sheet on file its capacitive or not if
                                                # capacitive does something else
                                                #print(file_name)

                                                file_path = os.path.join(device_path, file_name)
                                                sweep_type = eq.check_sweep_type(file_path)
                                                #print(sweep_type)
                                                if sweep_type == 'Iv_sweep':

                                                    # Performs analysis on the file given returning the dataframe after
                                                    # analysis
                                                    analysis_result = eq.file_analysis(file_path, plot_graph, save_df,
                                                                                       device_path)

                                                    if analysis_result is None:
                                                        # if there is an error in reading the file it will jst continue
                                                        # skipping
                                                        continue

                                                    num_sweeps, short_name, long_name, data, file_stats, graph = analysis_result

                                                    # keeps count of the number of sweeps by each device
                                                    num_of_sweeps += num_sweeps

                                                    # storing information from analysis
                                                    list_of_measured_files.append(long_name)
                                                    list_of_graphs.append(graph)
                                                    list_of_file_stats.append(file_stats)
                                                    file_data[f'{file_name}'] = data

                                                    file_key = f'{material}_{polymer}_{sample_name}_{section_folder}_{device_folder}_{file_name}'

                                                    # Store the file information in the dictionary
                                                    file_info_dict[file_key] = {
                                                        'material': material,
                                                        'polymer': polymer,
                                                        'sample_name': sample_name,
                                                        'section_folder': section_folder,
                                                        'device_folder': device_folder,
                                                        'file_name': file_name,
                                                        'file_path': os.path.join(device_path, file_name)
                                                    }
                                                else:
                                                    print("This file isn't a simple IV_Sweep Skipping ")
                                                    continue


                                        # for the device level, After processing all files in the device_number folder:

                                        if len(list_of_file_stats) >=2:
                                            device_stats_dict[f'{device_folder}'] = pd.concat(list_of_file_stats, ignore_index=True)
                                        device_data[f'{device_folder}'] = file_data
                                        device_sweeps_dict[f'{device_folder}'] = num_of_sweeps
                                        list_of_measured_files_devices.append(list_of_measured_files)

                                        #plt.hist(device_stats_dict[f'{device_folder}']['ON_OFF_Ratio'], bins=30, edgecolor='black')


                                # for the section level
                                # this already does all sections correctly
                                section_stats_dict[f'{section_folder}'] = device_stats_dict
                                section_sweeps_dict[f'{section_folder}'] = device_sweeps_dict
                                section_data[f'{section_folder}']=device_data


                                # calculation for each section and the statistics of each
                                # pdf.create_pdf_with_graphs_and_data_for_section()
                                # section name
                                list_of_measured_files_devices_sections.append(list_of_measured_files_devices)

                        # Names the final dictionary the sample name for storage later if necessary
                        sample_stats_dict[f'{sample_name}'] = section_stats_dict
                        sample_sweeps_dict[f'{sample_name}'] = section_sweeps_dict
                        sample_data[f'{sample_name}'] = section_data


                        print("")
                        print("################################")
                        print("Sample finished processing - ", sample_name)
                        print("################################")

                        # access the dataframe for specific bits
                        #print(sample_stats_dict[f'{sample_name}']['G 200µm'])

                        # graphs = some_function_comparing_all_files
                        #pdf.create_pdf_with_graphs_and_data_for_sample(sample_path,f"{sample_name}.pdf",info_dict,sample_stats_dict)

                        # Saves information for later use
                        with open(sample_path + '/' + sample_name + '_Stats', 'wb') as file:
                            pickle.dump(sample_stats_dict, file)

                        with open(sample_path + '/material_stats_dict.pkl', 'wb') as file:
                            pickle.dump(material_stats_dict, file)

                        with open(sample_path + '/'+sample_name+'_data', 'wb') as file:
                            # all the data for the given sample
                            pickle.dump(sample_data, file)

                        # save the dataframe for stats within the sample folder in txt format
                        eq.save_df_off_stats(sample_path, sample_stats_dict, sample_sweeps_dict)
                        # saves df in text format for each sample
                        #eq.save_df_off_data(sample_path, sample_data, sample_sweeps_dict)

                        #print(sample_data[f'{sample_name}']['G 200µm']['1']['1-Fs_0.5v_0.01s.txt'])


                # More dictionary stuff
                polymer_stats_dict[f'{polymer}'] = sample_stats_dict
                polymer_sweeps_dict[f'{polymer}'] = sample_sweeps_dict
                polymer_data[f'{polymer}'] = sample_data

        # More dictionary stuff
        material_stats_dict[f'{material}'] = polymer_stats_dict
        material_sweeps_dict[f'{material}'] = polymer_sweeps_dict
        material_data[f'{material}'] = polymer_data

# material data = all the data extracted forom the sweep (voltage,current,abs_current etc....
# materials_stats_dict = all the stats like area, resistance on and off etc...
# materials_sweeps_dicts = all the sweeps per device in dictionary

print("")
print("-----------------------")
print("access files using the following")
print("material_data['Stock'][f'{polymer}'][f'{sample_name}']['G 200µm']['1']['1-Fs_0.5v_0.01s.txt']")
print("material_sweeps_dict(['stock'][[f'{polymer}'][f'{sample_name}'][['G 200µm']['1'])")
print("-----------------------")

############################################################################

# A Breakpoint below does all the stats on the device
# VERY CRUDE JUST PRINTS EVERYTHING DOSNT SAVE ANYTHING YET

############################################################################

print("\nSample with the most sweeps, corresponding sample and its sweeps in high to low")

# Sample with the most sweeps, corresponding sample and its sweeps in high to low
sample_sweeps = eq.get_num_sweeps_ordered(file_info_dict,material_sweeps_dict)

# Counter variable to keep track of the number of items printed
print("Top 10 measured samples = ")
print('-' * 50)
printed_count = 0
for file_key, file_info in sample_sweeps.items():
    # Print only the top 10 items
    if printed_count < 10:
        print(f'File Key: {file_key}')
        print(f'Sample Name: {file_info["sample_name"]}')
        print(f'Total Sum: {file_info["total_sum"]}')
        print('-' * 25)

        # Increment the counter
        printed_count += 1

#####################################
print('')
#####################################


# Call the function to process 'ON_OFF_Ratio'
on_off_ratio_info = eq.process_property(material_stats_dict, 'ON_OFF_Ratio')

# Call the function to process 'normalised_area'
normalised_area_info = eq.process_property(material_stats_dict, 'normalised_area')

# Print the comprehensive information outside the function
for sample_key, sample_info in on_off_ratio_info.items():
    print(f"Comprehensive Information for {sample_key}:")
    print(f"Best Device: #{sample_info['best_device']['device_key']}, Mean ON_OFF_Ratio: {sample_info['mean_ON_OFF_Ratio']}")
    print(f"Top 3 Devices:")
    for idx, device_info in enumerate(sample_info['top3_devices'], start=1):
        print(f"#{idx}: Device: #{device_info['device_key']}, ON_OFF_Ratio: {device_info['ON_OFF_Ratio']}, File Name: {device_info['file_name']}")
    print(f"Mean ON_OFF_Ratio: {sample_info['mean_ON_OFF_Ratio']}")
    print(f"Median ON_OFF_Ratio: {sample_info['median_ON_OFF_Ratio']}")
    print(f"Mode ON_OFF_Ratio: {sample_info['mode_ON_OFF_Ratio']}")
    print("\n")

# Use the returned information as needed...
# print("ON_OFF_Ratio Information:")
# print(on_off_ratio_info)
#
# print("\nNormalised Area Information:")
# print(normalised_area_info)


# Function to find the top samples based on a given property (ON-OFF ratio or normalized area)


# Call the function to find the top 10 samples based on ON-OFF ratio
on_off_ratio_info, top_samples_with_repetition_on_off, top_samples_without_repetition_on_off = eq.find_top_samples(material_stats_dict, property_name='ON_OFF_Ratio')

# Call the function to find the top 10 samples based on normalized area
normalized_area_info, top_samples_with_repetition_normalized, top_samples_without_repetition_normalized = eq.find_top_samples(material_stats_dict, property_name='normalised_area')


# Print the results for ON-OFF ratio
print("Top Samples (With Repetition) - ON-OFF Ratio:")
for idx, sample_info in enumerate(on_off_ratio_info[:10], start=1):
    print(f"#{idx}: Sample: {sample_info['sample_key']}, Section: {sample_info['section_key']}, Device: {sample_info['device_key']}, File Name: {sample_info['file_name']}, ON-OFF Ratio: {sample_info['property_value']}")

print("\nTop Samples (Without Repetition) - ON-OFF Ratio:")
for idx, sample_key in enumerate(top_samples_without_repetition_on_off[:10], start=1):
    # Find the corresponding sample info for samples without repetition
    sample_info = next(info for info in on_off_ratio_info if info['sample_key'] == sample_key)
    print(f"#{idx}: Sample: {sample_info['sample_key']}, Section: {sample_info['section_key']}, Device: {sample_info['device_key']}, File Name: {sample_info['file_name']}, ON-OFF Ratio: {sample_info['property_value']}")

# Print the results for normalized area
print("\nTop Samples (With Repetition) - Normalized Area:")
for idx, sample_info in enumerate(normalized_area_info[:10], start=1):
    print(f"#{idx}: Sample: {sample_info['sample_key']}, Section: {sample_info['section_key']}, Device: {sample_info['device_key']}, File Name: {sample_info['file_name']}, Normalized Area: {sample_info['property_value']}")

print("\nTop Samples (Without Repetition) - Normalized Area:")
for idx, sample_key in enumerate(top_samples_without_repetition_normalized[:10], start=1):
    # Find the corresponding sample info for samples without repetition
    sample_info = next(info for info in normalized_area_info if info['sample_key'] == sample_key)
    print(f"#{idx}: Sample: {sample_info['sample_key']}, Section: {sample_info['section_key']}, Device: {sample_info['device_key']}, File Name: {sample_info['file_name']}, Normalized Area: {sample_info['property_value']}")


##################################################################

# ignore below this line

##################################################################
# # Iterate through the material, polymer, and sample dictionaries finsing the largest ON-OFF ratio for each material, polymer, and sample.
# for material_key, polymer_dict in material_stats_dict.items():
#     for polymer_key, sample_dict in polymer_dict.items():
#         for sample_key, section_dict in sample_dict.items():
#             for section_key, device_dict in section_dict.items():
#                 for device_key, stats_df in device_dict.items():
#                     # Extract the row with the largest ON-OFF ratio
#                     max_on_off_row = stats_df.loc[stats_df['ON_OFF_Ratio'].idxmax()]
#
#                     # Extract relevant information
#                     largest_on_off_ratio = max_on_off_row['ON_OFF_Ratio']
#                     file_name = max_on_off_row['file_name']
#
#                     # Print or store the information as needed
#                     print(f"Largest ON-OFF Ratio for {material_key}_{polymer_key}_{sample_key}_{section_key}_{device_key}: {largest_on_off_ratio}")
#                     print(f"Corresponding File Name: {file_name}")

# ... (continue with your existing code)

#
# Close the file to ensure that everything is written
#output_file.close()


# if __name__ == '__main__':
#     #This is a piece of boilerplate code which you should write routinely when you create a script.
#     print('Since this is inside the if statement it will only run if you run this file and not it you import it')
#     #example_function()
# Close the file to ensure that everything is written
