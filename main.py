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

# have it create the origin graphs for all files towards the end, however only do this if there isn't already an origin
# file created for each

# images in, with a full overview of each create a final overview pdf of each device with all the sweeps information
# ie average enclosed area, avaerage switching

# check for number of sweeps completed for each device so far

# find a way to incorporate the file created that keeps track of all the info from each sweep from past resuts where
# i give the endurance nuber of sweeps etc celled _____

save_df = False
plot_graph = True
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
                                                sweep_type = eq.check_sweep_type(file_path)
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
                        pdf.create_pdf_with_graphs_and_data_for_sample(sample_path,f"{sample_name}.pdf",info_dict,sample_stats_dict)

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
#print(material_data['Stock'][f'{polymer}'][f'{sample_name}']['G 200µm']['1']['1-Fs_0.5v_0.01s.txt'])
print("-----------------------")

# perform any analysis of the data here and below:

# Sample with the most sweeps, corresponding sample and its sweeps in high to low
sample_sweeps = eq.get_num_sweeps_ordered(file_info_dict,material_sweeps_dict)


# Counter variable to keep track of the number of items printed
print("Top 3 measured samples = ")
print('-' * 50)
printed_count = 0
for file_key, file_info in sample_sweeps.items():
    # Print only the top 3 items
    if printed_count < 3:
        print(f'File Key: {file_key}')
        print(f'Sample Name: {file_info["sample_name"]}')
        print(f'Total Sum: {file_info["total_sum"]}')
        print('-' * 25)

        # Increment the counter
        printed_count += 1



# if __name__ == '__main__':
#     #This is a piece of boilerplate code which you should write routinely when you create a script.
#     print('Since this is inside the if statement it will only run if you run this file and not it you import it')
#     #example_function()