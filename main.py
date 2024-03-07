import pandas as pd
import statistics
import numpy
import os
import Data as eq
import pdf as pdf
import matplotlib.pyplot as plt
import excell as exc
import file as f
import pickle
import pprint
import math
import sys
import print_info as p
from file import Tee
import shutil
import excell as ex
from file import excel_path
import plotting
import Origin as origin
import re
import copy_graph_class as cg

###### Important ######
# Make sure that all files are text files you can easily do this using power rename and
# "NOT *.txt" within the search bar to find all the files in the directory that arnt texts and then rename them
# using power rename, add the last letter into the top search bar and the extension .txt in the one below
# then set to extension only.

# pip install reportlab matplotlib

# to add
# - histogram all the data
# - reorganise the functions


# Open a file for writing with utf-8 encoding
output_file = open(f.main_dir + 'printlog.txt', 'w', encoding='utf-8')

# Redirect print output to both the file and the console
sys.stdout = Tee(file=output_file, stdout=sys.stdout)

sort_graphs = False
origin_graphs = False
pull_fabrication_info_excell = False
save_df = False
plot_graph = True
plot_gif = True
re_save_graph = True
re_analyse = True

# set Pandas display options to display all data in dataframe?
#eq.set_pandas_display_options()

# Main for loop for parsing through folders

# empty dictionary's for later use
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
                        """ working on a sample folders, here do anything for work on the device that dosnt 
                        involve analysis of data:
                        Sample name = ie D14-Stock-Gold-PVA(2%)-Gold-s7 """

                        # print("working on ", sample_name)
                        # print("Path = ", sample_path)
                        if pull_fabrication_info_excell:
                            # Pulls information on fabrication from excell file
                            fabrication_info_dict = exc.save_info_from_solution_devices_excell(sample_name,
                                                                                               f.excel_path,
                                                                                               sample_path)
                        # Pulls information from device sweep excell sheet
                        sample_sweep_excell_dict = exc.save_info_from_device_info_excell(sample_name, sample_path)

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
                                """ working on section folder"""
                                print("working on ", sample_name, section_folder)

                                # More empty arrays for storing all measured devices
                                list_of_measured_files_devices = []
                                device_sweeps_dict = {}
                                device_stats_dict = {}
                                device_data = {}
                                #print(section_path)


                                def extract_numeric_part(filename):
                                    match = re.search(r'\d+', filename)
                                    return int(match.group()) if match else float('inf')


                                # Sort the list of filenames based on the numeric part
                                sorted_files = sorted(os.listdir(section_path), key=extract_numeric_part)

                                for device_folder in sorted_files:
                                    device_path = os.path.join(section_path, device_folder)
                                    if os.path.isdir(device_path):
                                        print(device_folder)
                                        """ Working on individual devices"""
                                        # print("working in folder ", sample_name, section_folder, device_folder)

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
                                        #print(os.listdir(device_path))
                                        # sorted(os.listdir(device_path), key=lambda x: int(re.split(r'[-_]', x)[0]) if re.match(r'^\d+', re.split(r'[-_]', x)[0]) else float('inf')):
                                        for file_name in (os.listdir(device_path)):
                                            file_path = os.path.join(device_path, file_name)
                                            if file_name.endswith('.txt'):
                                                #print(file_name)
                                                """Loops through each file in the folder and analyses them using the 
                                                functions here"""

                                                # Checks and returns the sweep type of the file also checks for nan
                                                # values if nan values are present returns None

                                                sweep_type = eq.check_sweep_type(file_path)
                                                #print(sweep_type)

                                                if sweep_type == 'Iv_sweep':
                                                    """ for simple iv sweeps"""

                                                    # Performs analysis on the file given returning the dataframe
                                                    analysis_result = eq.file_analysis(file_path, plot_graph, save_df,
                                                                                       device_path, re_save_graph)

                                                    if analysis_result is None:
                                                        # if there is an error in reading the file it will just continue
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
                                                    #print(file_info_dict[f'{file_key}'])
                                                    if sort_graphs:
                                                        cg.yes_no(file_data[f'{file_name}'], file_info_dict[file_key])

                                                else:
                                                    #print("This file isn't a simple IV_Sweep Skipping ")
                                                    continue

                                        ###############################################################################
                                        """ For the device level only place in here any information that needs to be 
                                        done on an individual device """

                                        save_name = "_Device" + f"{device_folder}" + ".gif"
                                        folder_path = device_path + '\\' + "python_images"
                                        output_gif_loc = os.path.join(folder_path, save_name)

                                        if plot_gif:
                                            # Creates Gifs of any sample with multiple sweeps
                                            plotting.create_gif_from_folder(folder_path, output_gif_loc, duration=0,restart_duration=10)

                                        if len(list_of_file_stats) >= 2:
                                            device_stats_dict[f'{device_folder}'] = pd.concat(list_of_file_stats,ignore_index=True)

                                        # determines the classification of a device from the excell sheet
                                        classification = eq.device_clasification(sample_sweep_excell_dict, device_folder, section_folder,device_path)

                                        device_data[f'{device_folder}'] = file_data

                                        device_sweeps_dict[f'{device_folder}'] = {'num_of_sweeps': num_of_sweeps,'classification': classification}

                                        if origin_graphs:
                                            # plot the data in origin for use later
                                            origin.plot_in_origin(device_data, device_path, 'transport')

                                        # plt.hist(device_stats_dict[f'{device_folder}']['ON_OFF_Ratio'], bins=30, edgecolor='black')

                                ###############################################################################
                                """ For the Section level only place in here any information that needs to be 
                                done on an individual section """

                                # Creating Dictionary's for device stats as a section
                                section_stats_dict[f'{section_folder}'] = device_stats_dict
                                section_sweeps_dict[f'{section_folder}'] = device_sweeps_dict
                                section_data[f'{section_folder}'] = device_data

                        ###############################################################################
                        """ For the Sample level only place in here any information that needs to be 
                        done on an individual Sample level """

                        # Names the final dictionary the sample name for storage later if necessary
                        sample_stats_dict[f'{sample_name}'] = section_stats_dict
                        sample_sweeps_dict[f'{sample_name}'] = section_sweeps_dict
                        sample_data[f'{sample_name}'] = section_data



                        ######################################
                        # this is for auto adding sweeps into the excell file pls keep
                        # for section_name, section_data in sample_sweep_excell_dict.items():
                        #     section_letter = section_name[0]  # Take the first letter of the section name
                        #     print(section_letter)
                        #     # Check if the section letter exists
                        #     #print(section_letter)
                        #     #print(section_data)
                        #     # Find the first key containing the letter 'A'
                        #     matching_key = next((key for key in sample_sweeps_dict if section_letter in key), None)
                        #     print(matching_key , "matching key")
                        #     if matching_key is not None:
                        #         data_s = sample_sweeps_dict[matching_key]
                        #         print(data_s)
                        #         #not sure if this works but give it a try
                        #         #exc.update_and_save_to_excel(sample_name, sample_path, matching_key, data_s)
                        #     else:
                        #         print("No key containing", section_letter , " found in sample_sweeps_dict.")
                        ######################################

                        # try:
                        #     # Get the folder name without the path
                        #     folder_name = os.path.basename(subfolder)
                        #     subfolder = os.path.abspath(subfolder)
                        #     print("foldername", folder_name)
                        #     print(subfolder)
                        #
                        #
                        #     # Check if the folder still exists
                        #     if not os.path.exists(subfolder):
                        #         print(f"Folder {subfolder} does not exist. Skipping...")
                        #         continue
                        #
                        #     # Check if a file with the same name as the folder already exists
                        #     dest_file_path = os.path.join(subfolder, folder_name + os.path.splitext(dest_file)[1])
                        #     if os.path.exists(dest_file_path):
                        #         print(f"File already exists in {subfolder}. Skipping...")
                        #         processed_folders.append(subfolder)  # Add the skipped folder to processed_folders
                        #         continue
                        #
                        #     # Copy the file to the destination and rename it
                        #     shutil.copy(dest_file, dest_file_path)
                        #     print(f"File copied to {subfolder} and renamed to {folder_name}")

                        print("")
                        print("################################")
                        print("Sample finished processing - ", sample_name)
                        print("################################")

                        # access the dataframe for specific bits
                        # print(sample_stats_dict[f'{sample_name}']['G 200µm'])

                        # graphs = some_function_comparing_all_files
                        # pdf.create_pdf_with_graphs_and_data_for_sample(sample_path,f"{sample_name}.pdf",info_dict,sample_stats_dict)

                        # Saves information for later use
                        with open(sample_path + '/' + sample_name + '_Stats', 'wb') as file:
                            pickle.dump(sample_stats_dict, file)

                        with open(sample_path + '/material_stats_dict.pkl', 'wb') as file:
                            pickle.dump(material_stats_dict, file)

                        with open(sample_path + '/' + sample_name + '_data', 'wb') as file:
                            # all the data for the given sample
                            pickle.dump(sample_data, file)

                        # save the dataframe for stats within the sample folder in txt format
                        eq.save_df_off_stats(sample_path, sample_stats_dict, sample_sweeps_dict)

                        # saves df in text format for each sample
                        # eq.save_df_off_data(sample_path, sample_data, sample_sweeps_dict)

                # More dictionary stuff
                polymer_stats_dict[f'{polymer}'] = sample_stats_dict
                polymer_sweeps_dict[f'{polymer}'] = sample_sweeps_dict
                polymer_data[f'{polymer}'] = sample_data

        # More dictionary stuff
        material_stats_dict[f'{material}'] = polymer_stats_dict
        material_sweeps_dict[f'{material}'] = polymer_sweeps_dict
        material_data[f'{material}'] = polymer_data

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

############################################################################
# All sweeps analysed at this point stats are done below
# A Breakpoint below does all the stats on the device
# VERY CRUDE JUST PRINTS EVERYTHING DOS-NT SAVE ANYTHING YET

############################################################################



# Calculate yield for each sample
yield_dict, yield_dict_sect = eq.calculate_yield(material_sweeps_dict)
print("Yield for each sample, descending order")
print('-' * 25)
for key, value in yield_dict.items():
    print(f'{key}: {value}')
print('-' * 25)

#####################################
print('')
#####################################

# Sample with the most sweeps, corresponding sample and its sweeps in high to low
sample_sweeps = eq.get_num_sweeps_ordered(file_info_dict, material_sweeps_dict)

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

# print the values from above
p.print_on_off_ratio_info(on_off_ratio_info)
p.print_normalised_area_info(normalised_area_info)

# Call the function to find the top 10 samples based on ON-OFF ratio
on_off_ratio_info, top_samples_with_repetition_on_off, top_samples_without_repetition_on_off = eq.find_top_samples(
    material_stats_dict, property_name='ON_OFF_Ratio')

# Call the function to find the top 10 samples based on normalized area
normalized_area_info, top_samples_with_repetition_normalized, top_samples_without_repetition_normalized = eq.find_top_samples(
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

#####################################
print('')
#####################################

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
