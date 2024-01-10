import pandas as pd
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

from file import excel_path
import excell as ex

# pip install reportlab matplotlib

# to add
# Todo Statistics- pull data from the statisitcs sheet i fill out when measuring the devices
#  create a file that saves all the data collected from each device an sweeps within the data
# - histogram all the data
# - reorganise the functions
#

# Add a try except when file reading, so if the first way doesn't work, it tries something else.
# i.e tries csv or a different method of extracting data from a text file
# add something about working out what kind of data I am taking, and it should react accordingly
# have it create the origin graphs for all files towards the end, however only do this if there isn't already an origin
# file created for each

# loop through all the multiple sweeps and save images if each sweep for use later, for each of the looped data with all the individual
# images in, with a full overview of each create a final overview pdf of each device with all the sweeps information
# ie average enclosed area, avaerage switching

# check for number of sweeps completed for each device so far

# find a way to incorporate the file created that keeps track of all the info from each sweep from past resuts where
# i give the endurance nuber of sweeps etc celled _____

save_df = False
plot_graph = False
re_analyse = True
#eq.set_pandas_display_options()

# Main for loop for parsing through folders
# empty dictionary's
material_stats_dict = {}
material_sweeps_dict = {}
material_data = {}

for type_folder in os.listdir(f.main_dir):
    type_path = os.path.join(f.main_dir, type_folder)
    if os.path.isdir(type_path):
        # Navigate through sub-folders (e.g., polymer)
        polymer_stats_dict = {}
        polymer_sweeps_dict = {}
        polymer_data = {}
        for polymer_folder in os.listdir(type_path):
            polymer_path = os.path.join(type_path, polymer_folder)

            if os.path.isdir(polymer_path):
                # Navigate through sample_name folders
                sample_stats_dict = {}
                sample_sweeps_dict = {}
                sample_data = {}

                for sample_name in os.listdir(polymer_path):
                    sample_path = os.path.join(polymer_path, sample_name)
                    if os.path.isdir(sample_path):
                        print("working on ", sample_name)
                        print("Path = ", sample_path)
                        # Anything to device that doesn't require information on individual sweeps
                        # Sample name = ie D14-Stock-Gold-PVA(2%)-Gold-s7

                        # Pulls information from device sweep excell sheet
                        sample_sweep_excell_dict = exc.save_info_from_device_info_excell(sample_name, sample_path)
                        print(sample_sweep_excell_dict['G'])

                        # Pulls information on fabrication from excell file
                        info_dict = exc.save_info_from_solution_devices_excell(sample_name, f.excel_path, sample_path)

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
                                print("working on ", sample_name, section_folder)

                                list_of_measured_files_devices = []
                                device_sweeps_dict = {}
                                device_stats_dict = {}
                                device_data = {}

                                for device_folder in os.listdir(section_path):
                                    device_path = os.path.join(section_path, device_folder)
                                    if os.path.isdir(device_path):
                                        # Working on individual devices
                                        print("")
                                        print("working in folder ", sample_name, section_folder, device_folder)
                                        print("")

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

                                                file_path = os.path.join(device_path, file_name)

                                                # Performs analysis on the file given returning the dataframe after
                                                # analysis
                                                analysis_result = eq.file_analysis(file_path, plot_graph, save_df,
                                                                                   device_path)

                                                if analysis_result is None:
                                                    # if there is an error in reading the file it will jst continue
                                                    # skipping
                                                    continue

                                                file_info, num_sweeps, short_name, long_name, data, file_stats, graph = analysis_result

                                                # keeps count of the number of sweeps by each device
                                                num_of_sweeps += num_sweeps

                                                # storing information from analysis
                                                list_of_measured_files.append(long_name)
                                                list_of_graphs.append(graph)
                                                list_of_file_stats.append(file_stats)
                                                file_data[f'{file_name}'] = data



                                        # for the device level, After processing all files in the device_number folder:


                                        device_stats_dict[f'{device_folder}'] = pd.concat(list_of_file_stats, ignore_index=True)
                                        device_data[f'{device_folder}'] = file_data
                                        device_sweeps_dict[f'{device_folder}'] = num_of_sweeps
                                        print('section_sweeps_dict for device', (device_sweeps_dict))
                                        list_of_measured_files_devices.append(list_of_measured_files)

                                        #plt.hist(device_stats_dict[f'{device_folder}']['ON_OFF_Ratio'], bins=30, edgecolor='black')
                                        print("")
                                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                                        print("information on device", section_folder, device_folder)
                                        print("largest ON OFF Ratio = ", "value", "for", "value")
                                        print("total number of sweeps = ", num_of_sweeps)
                                        print("Moving onto next device folder")
                                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                                        print("")

                                # for the section level
                                # this already does all sections correctly
                                section_stats_dict[f'{section_folder}'] = device_stats_dict
                                section_sweeps_dict[f'{section_folder}'] = device_sweeps_dict
                                section_data[f'{section_folder}']=device_data
                                print('section_sweeps_dict for section', section_sweeps_dict)

                                print("")
                                print("########################################")
                                print("information on section", section_folder)
                                print("largest ON OFF Ratio = ", "value", "for", "value")
                                print("other information here")
                                print("Moving onto next section folder")
                                print("########################################")
                                print("")

                                # calculation for ech section and the statistics of each
                                # pdf.create_pdf_with_graphs_and_data_for_section()
                                # section name
                                list_of_measured_files_devices_sections.append(list_of_measured_files_devices)

                        # Names the final dictionary the sample name for storage later if necessary
                        sample_stats_dict[f'{sample_name}'] = section_stats_dict
                        sample_sweeps_dict[f'{sample_name}'] = section_sweeps_dict
                        sample_data[f'{sample_name}'] = section_data
                        print(sample_sweeps_dict)

                        print("")
                        print("\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/")
                        print("information on sample", sample_name)
                        print("largest ON OFF Ratio = ", "value", "for", "value")
                        print("other information here")
                        print("Moving onto next section folder")
                        print("\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/")
                        print("")

                        # access the dataframe for specific bits
                        #print(sample_stats_dict[f'{sample_name}']['G 200µm'])

                        # graphs = some_function_comparing_all_files
                        pdf.create_pdf_with_graphs_and_data_for_sample(sample_path,
                                                                       f"{file_info.get('sample_name')}.pdf", graph,
                                                                       info_dict)

                        # Saves information for later use
                        with open(sample_path + '/statistic_device_pkl', 'wb') as file:
                            pickle.dump(sample_stats_dict, file)

                        with open(sample_path + '/list of devices & files measured', 'wb') as file:
                            pickle.dump(list_of_measured_files, file)

                        # save the dataframe for stats within the sample folder in txt format
                        eq.save_df_off_stats(sample_path, sample_stats_dict, sample_sweeps_dict)

                        #print(sample_data[f'{sample_name}']['G 200µm']['1']['1-Fs_0.5v_0.01s.txt'])
                        # these dictionrys need to be all the way back to "1) memristor"

                # More dictionary stuff
                polymer_stats_dict[f'{polymer_folder}'] = sample_stats_dict
                polymer_sweeps_dict[f'{polymer_folder}'] = sample_sweeps_dict
                polymer_data[f'{polymer_folder}'] = sample_data

        # More dictionary stuff
        material_stats_dict[f'{type_folder}'] = polymer_stats_dict
        material_sweeps_dict[f'{type_folder}'] = polymer_sweeps_dict
        material_data[f'{type_folder}'] = polymer_data

        print("")
        print("-----------------------")
        print("access files using the following")
        print("material_data['Stock'][f'{polymer_folder}'][f'{sample_name}']['G 200µm']['1']['1-Fs_0.5v_0.01s.txt']")
        #print(material_data['Stock'][f'{polymer_folder}'][f'{sample_name}']['G 200µm']['1']['1-Fs_0.5v_0.01s.txt'])
        print("-----------------------")





# For printing these
#################################
# for sample_name, section_name in sample_data.items():
#     print("------------------------")
#     print(f"sample Name:{sample_name}")
#     print("------------------------")
#     for section_name, device_number in section_name.items():
#         print(f"section Name:{section_name}")
#         print("------------------------")
#         for device_number, info in device_number.items():
#             print(f"device number:{device_number}")
#             print("------------------------")
#             print(info)
#             print("------------------------")
# print("###########################")
# for sample_name, section_info_stats in sample_stats_dict.items():
#     print("------------------------")
#     print(f"Sample Name: {sample_name}")
#     print("------------------------")
#     for section_name, device_number in section_info_stats.items():
#         print(f"Section Name: {section_name}")
#         print("------------------------")
#
#         # Access corresponding information from sample_sweeps_dict
#         section_info_sweeps = sample_sweeps_dict.get(sample_name, {}).get(section_name, {})
#
#         for device_number, info in device_number.items():
#             print(f"Device Number: {device_number}")
#             # Print corresponding info from sample_sweeps_dict if available
#             sweeps_info = section_info_sweeps.get(device_number, "No sweeps info available")
#             print(f"Number of sweeps: {sweeps_info}")
#             print(info)
#             print("------------------------")
#

# if __name__ == '__main__':
#     #This is a piece of boilerplate code which you should write routinely when you create a script.
#     print('Since this is inside the if statement it will only run if you run this file and not it you import it')
#     #example_function()