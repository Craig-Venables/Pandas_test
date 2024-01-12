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
eq.set_pandas_display_options()

# Main for loop for parsing through folders
# empty dictionary's
material_stats_dict = {}
material_sweeps_dict = {}
material_data = {}
material_names_dict = {}

sample_name_arr = []

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
                        print("working on ", sample_name)
                        print("Path = ", sample_path)
                        # Anything to device that doesn't require information on individual sweeps
                        # Sample name = ie D14-Stock-Gold-PVA(2%)-Gold-s7

                        # Pulls information from device sweep excell sheet
                        sample_sweep_excell_dict = exc.save_info_from_device_info_excell(sample_name, sample_path)
                        #print(sample_sweep_excell_dict['G'])

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

                                        if len(list_of_file_stats) >=2:
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
                        #current_sample_dict = {'sample_name': sample_name}
                        sample_names_dict["sample_name"] = sample_name
                        sample_name_arr.append("sample_name")
                        print(sample_names_dict)

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
                        # pdf.create_pdf_with_graphs_and_data_for_sample(sample_path,
                        #                                                f"{file_info.get('sample_name')}.pdf", graph,
                        #                                                info_dict)

                        # Saves information for later use
                        with open(sample_path + '/Statistic_device_pkl', 'wb') as file:
                            pickle.dump(sample_stats_dict, file)

                        with open(sample_path + '/material_stats_dict.pkl', 'wb') as file:
                            pickle.dump(material_stats_dict, file)

                        with open(sample_path + '/List of devices & files measured', 'wb') as file:
                            pickle.dump(list_of_measured_files, file)

                        with open(sample_path + '/Sample_data', 'wb') as file:
                            pickle.dump(sample_data, file)

                        # save the dataframe for stats within the sample folder in txt format
                        eq.save_df_off_stats(sample_path, sample_stats_dict, sample_sweeps_dict)

                        #eq.save_df_off_data(sample_path, sample_data, sample_sweeps_dict)

                        #print(sample_data[f'{sample_name}']['G 200µm']['1']['1-Fs_0.5v_0.01s.txt'])
                        # these dictionrys need to be all the way back to "1) memristor"

                # More dictionary stuff
                polymer_stats_dict[f'{polymer}'] = sample_stats_dict
                polymer_sweeps_dict[f'{polymer}'] = sample_sweeps_dict
                polymer_data[f'{polymer}'] = sample_data
                current_polymer_dict = {polymer: sample_names_dict}
                polymer_names_dict["polymer"] = current_polymer_dict


        # More dictionary stuff
        material_stats_dict[f'{material}'] = polymer_stats_dict
        material_sweeps_dict[f'{material}'] = polymer_sweeps_dict
        material_data[f'{material}'] = polymer_data
        current_material_dict = {material: polymer_names_dict}
        material_names_dict["material"] = current_material_dict

        print("")
        print("-----------------------")
        print("access files using the following")
        print("material_data['Stock'][f'{polymer}'][f'{sample_name}']['G 200µm']['1']['1-Fs_0.5v_0.01s.txt']")
        print("material_sweeps_dict(['stock'][[f'{polymer}'][f'{sample_name}'][['G 200µm']['1'])")
        #print(material_data['Stock'][f'{polymer}'][f'{sample_name}']['G 200µm']['1']['1-Fs_0.5v_0.01s.txt'])
        print("-----------------------")

print(material_names_dict)
print("#############")

# Assuming material_names_dict is the given dictionary
for material, material_dict in material_names_dict.items():
    print("Material Name:", material)

    for polymer, polymer_dict in material_dict.items():
        print("  Polymer Name:", polymer)

        for sample_name, sample_info in polymer_dict.items():
            print("    Sample Name:", sample_name)

            # Extract additional information if needed
            for key, value in sample_info.items():
                print(f"      {key}: {value}")

# # Assuming material_names_dict is the given dictionary
# material_name = list(material_names_dict['material'].keys())[0]
# polymer_name = list(material_names_dict['material'][material_name]['polymer'].keys())[0]
# sample_name = material_names_dict['material'][material_name]['polymer'][polymer_name]['sample_name']
#
# print("Material Name:", material_name)
# print("Polymer Name:", polymer_name)
# print("Sample Name:", sample_name)


# returns total number of sweeps completed for a single sample
def find_sample_number_sweeps(material,polymer,sample_name):

    data = material_sweeps_dict[f'{material}'][f'{polymer}'][f'{sample_name}']
    #print(data)
    def recursive_sum(value):
        if isinstance(value, (int, float)):
            return value
        elif isinstance(value, dict):
            return sum(recursive_sum(v) for v in value.values())
        else:
            return 0

    total_sum = sum(recursive_sum(value) for inner_dict in data.values() for value in inner_dict.values() if isinstance(value, (int, float)))
    #print(total_sum)
    return sample_name, total_sum


for item in sample_name_arr:
    sample_name, total_sum = find_sample_number_sweeps("Stock","PVA",item)
    print("total sweeps for",sample_name, "=",total_sum)


#data = {'D14-Stock-Gold-PVA(2%)-Gold-s7': {'G 200µm': {'1': 13.0, '2': 2}, 'H 100μm': {'1': 13.0, '2': 11.0}}}

# def recursive_sum(value):
#     if isinstance(value, (int, float)):
#         return value
#     elif isinstance(value, dict):
#         return sum(recursive_sum(v) for v in value.values())
#     else:
#         return 0
#
# total_sum = sum(recursive_sum(value) for nested_dict in data.values() for inner_dict in nested_dict.values() for value in inner_dict.values() if isinstance(value, (int, float)))

# print(total_sum)
# def find_largest_sweeps(material_sweeps_dict):
#     max_sweeps = 0
#     max_sweeps_sample_name = ""
#
#     for material_type, polymer_dict in material_sweeps_dict.items():
#         for polymer_type, sample_dict in polymer_dict.items():
#             for sample_name, sweeps_dict in sample_dict.items():
#                 for section_name, num_sweeps in sweeps_dict.items():
#                     if isinstance(num_sweeps, int) and num_sweeps > max_sweeps:
#                         print(num_sweeps , "num_sweeps")
#                         max_sweeps = num_sweeps
#                         max_sweeps_sample_name = sample_name
#                     else:
#                         print("notworking")
#
#     return max_sweeps, max_sweeps_sample_name

# def find_largest_sweeps(material_sweeps_dict, target_sample_name):
#     max_sweeps = 0
#
#     for material_type, polymer_dict in material_sweeps_dict.items():
#         for polymer_type, sample_dict in polymer_dict.items():
#             for sample_name, sweeps_dict in sample_dict.items():
#                 if sample_name == target_sample_name:
#                     sample_sweeps = sum(int(num_sweeps) for num_sweeps in sweeps_dict.values() if isinstance(num_sweeps, (int, float)))
#                     max_sweeps = max(max_sweeps, sample_sweeps)
#
#     return max_sweeps
#
# # Example usage:
# target_sample_name = "D14-Stock-Gold-PVA(2%)-Gold-s7"
# max_sweeps = find_largest_sweeps(material_sweeps_dict, target_sample_name)
#
# # Print the result
# print(f"The largest number of sweeps for {target_sample_name} is {max_sweeps}")





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