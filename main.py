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
# Todo add in the device name and polymer etc into the graphs when they get saved
# Todo Statistics- pull data from the statisitcs sheet i fill out when measuring the devices
#  - creat a file that saves all the data collected from each device an sweeps within the data
# - histogram all the data
# - reorganise the functions
#
# Add a try except when file reading, so if the first way dosnt work it tries something else.
# i.e tries csv or a different method of extracting data from a text file
# add something about working out what kind of data i am taking and it should react acodingly
# have it create the origin graphs for all files towards the end, hiwever only do this if there isnt already an origin
# file created for each

# creats a sub folder that containes all information used within python called "python info" here oit saves all the
# dataframes, the arry info and anything else ready for use later, create another folder named images where it saves
# all the images for each file and within that have another for each of the looped data with all the individual
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

for type_folder in os.listdir(f.main_dir):
    type_path = os.path.join(f.main_dir, type_folder)
    if os.path.isdir(type_path):
        # Navigate through sub-folders (e.g., polymer)
        for polymer_folder in os.listdir(type_path):
            polymer_path = os.path.join(type_path, polymer_folder)

            if os.path.isdir(polymer_path):
                # Navigate through sample_name folders
                final_stats_dict = {}
                final_sweeps_dict = {}

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
                        section_dict = {}
                        sweeps_dict = {}

                        # Navigate through section folders
                        for section_folder in os.listdir(sample_path):
                            # Anything to section that doesn't require information on individual sweeps
                            section_path = os.path.join(sample_path, section_folder)
                            if os.path.isdir(section_path):
                                # Navigate through device_number folders
                                print("working on ", sample_name, section_folder)
                                list_of_measured_files_devices = []
                                device_sweeps_dict = {}
                                device_dict = {}

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
                                        list_of_df = []
                                        list_of_graphs = []
                                        num_of_sweeps = 0

                                        # add more here into how each array changes over each array
                                        # Process each file in the device_number folder
                                        for file_name in os.listdir(device_path):
                                            if file_name.endswith('.txt'):
                                                # Does work on the file here

                                                # checks If in excell sheet on file its capacitive or not if
                                                # capacitive does something else

                                                file_path = os.path.join(device_path, file_name)

                                                # file_info,num_sweeps, short_name, long_name, df, area, areas_loops, \
                                                #     looped_array_info, graph = eq.file_analysis(
                                                #     file_path, plot_graph, save_df, device_path)

                                                analysis_result = eq.file_analysis(file_path, plot_graph, save_df,
                                                                                   device_path)

                                                if analysis_result is None:
                                                    continue
                                                file_info, num_sweeps, short_name, long_name, df, file_stats, graph = analysis_result
                                                # on off ratio

                                                num_of_sweeps += num_sweeps

                                                # add check to see if device is capacitive then ignore area maybe
                                                # check file maybe change loops into data into and averaging it check
                                                # needs to be added that does somthing if there is only  half loop ie
                                                # 0-1-0-1 etc this can be done by looking at vmax and min and if 0 is
                                                # vmin or vmax it assumes just a sweep within one region

                                                # append all the information to a master set of arrays
                                                plt.show()

                                                list_of_df.append(df)
                                                list_of_measured_files.append(long_name)
                                                list_of_graphs.append(graph)
                                                list_of_file_stats.append(file_stats)


                                        # for the device level, After processing all files in the device_number folder:
                                        # add file stats to a pd dataframe

                                        device_dict[f'{device_folder}'] = pd.concat(list_of_file_stats, ignore_index=True)

                                        list_of_measured_files_devices.append(list_of_measured_files)
                                        print(num_of_sweeps)

                                        #plt.hist(device_dict[f'{device_folder}']['ON_OFF_Ratio'], bins=30, edgecolor='black')
                                        print("")
                                        print("####################################")
                                        print("information on device",section_folder, device_folder)
                                        print("total number of sweeps = ", num_of_sweeps)
                                        print("Moving onto next device folder")
                                        print("####################################")
                                        print("")

                                        device_sweeps_dict[f'{device_folder}'] = num_of_sweeps
                                        print('sweeps_dict for device', (device_sweeps_dict))

                                # for the section level
                                # this already does all sections correctly
                                section_dict[f'{section_folder}'] = device_dict
                                sweeps_dict[f'{section_folder}'] = device_sweeps_dict
                                print('sweeps_dict for section',sweeps_dict)

                                # calculation for ech section and the statistics of each
                                # pdf.create_pdf_with_graphs_and_data_for_section()
                                # section name
                                list_of_measured_files_devices_sections.append(list_of_measured_files_devices)

                        # Names the final dictionary the sample name for storage later if necessary
                        final_stats_dict[f'{sample_name}'] = section_dict
                        final_sweeps_dict[f'{sample_name}'] = sweeps_dict
                        print(final_sweeps_dict)

                        # access the dataframe for specific bits
                        #print(final_stats_dict[f'{sample_name}']['G 200µm'])



                        # graphs = some_function_comparing_all_files
                        pdf.create_pdf_with_graphs_and_data_for_sample(sample_path,
                                                                       f"{file_info.get('sample_name')}.pdf", graph,
                                                                       info_dict)

                        # Saves information for later use
                        with open(sample_path + '/stats_dict_pkl', 'wb') as file:
                            pickle.dump(final_stats_dict, file)

                        with open(sample_path + '/list of devices measured_pkl', 'wb') as file:
                            pickle.dump(list_of_measured_files, file)

print("###########################")
for sample_name, section_info_stats in final_stats_dict.items():
    print("------------------------")
    print(f"Sample Name: {sample_name}")
    print("------------------------")
    for section_name, device_number in section_info_stats.items():
        print(f"Section Name: {section_name}")
        print("------------------------")

        # Access corresponding information from final_sweeps_dict
        section_info_sweeps = final_sweeps_dict.get(sample_name, {}).get(section_name, {})

        for device_number, info in device_number.items():
            print(f"Device Number: {device_number}")
            # Print corresponding info from final_sweeps_dict if available
            sweeps_info = section_info_sweeps.get(device_number, "No sweeps info available")
            print(f"Number of sweeps: {sweeps_info}")
            print(info)
            print("------------------------")

