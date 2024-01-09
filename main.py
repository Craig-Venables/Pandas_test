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
                for sample_name in os.listdir(polymer_path):
                    sample_path = os.path.join(polymer_path, sample_name)
                    if os.path.isdir(sample_path):
                        print("working on ", sample_name)
                        print("Path = ", sample_path)
                        # Anything to device that doesn't require information on individual sweeps
                        # Sample name = ie D14-Stock-Gold-PVA(2%)-Gold-s7

                        # Pulls information from device sweep excell sheet
                        sample_sweep_dict = exc.save_info_from_device_info_excell(sample_name, sample_path)
                        print(sample_sweep_dict['G'])

                        # Pulls information on fabrication from excell file
                        info_dict = exc.save_info_from_solution_devices_excell(sample_name, f.excel_path, sample_path)

                        # empty list for storing all measured devices
                        list_of_measured_files_devices_sections = []
                        device_dict = {}
                        section_dict = {}
                        final_dict = {}
                        # Navigate through section folders
                        for section_folder in os.listdir(sample_path):
                            # Anything to section that doesn't require information on individual sweeps
                            section_path = os.path.join(sample_path, section_folder)
                            if os.path.isdir(section_path):
                                # Navigate through device_number folders
                                print("working on ", sample_name, section_folder)
                                list_of_measured_files_devices = []

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

                                                analysis_result = eq.file_analysis(file_path, plot_graph, save_df, device_path)

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

                                                list_of_df.append(df)
                                                list_of_measured_files.append(long_name)
                                                list_of_graphs.append(graph)
                                                list_of_file_stats.append(file_stats)

                                        # for the device level

                                        concatdf = pd.concat(list_of_file_stats,ignore_index=True)
                                        print(concatdf)
                                        device_dict[f'{device_folder}'] = concatdf



                                        # After processing all files in the device_number folder

                                        print("")
                                        print("####################################")
                                        print("information on device", device_folder )
                                        # print("list of measured devices" ,list_of_measured_files)
                                        print("total number of sweeps = ", num_of_sweeps)
                                        # print("final list of measured files")
                                        #print(list_of_file_stats)
                                        # print(list_of_measured_files)
                                        # print(list_of_file_stats)
                                        list_of_measured_files_devices.append(list_of_measured_files)
                                        print("Moving onto next device folder")
                                        print("####################################")
                                        print("")


                                # for the section level
                                # this already does all sections correctly
                                section_dict[f'{section_folder}'] = device_dict

                                # calculation for ech section and the statistics of each
                                # pdf.create_pdf_with_graphs_and_data_for_section()
                                # section name
                                list_of_measured_files_devices_sections.append(list_of_measured_files_devices)

                        # Names the final dictionary the sample name for storage later if necessary
                        final_dict[f'{sample_name}'] = section_dict

                        print("----------------------------------------")
                        print("----------------------------------------")
                        print("----------------------------------------")

                        # access the dataframe for specific bits
                        print(final_dict[f'{sample_name}']['G 200µm'])


                        for sample_name,section_name in final_dict.items():
                            print("------------------------")
                            print(f"sample Name:{sample_name}")
                            print("------------------------")
                            for section_name, device_number in section_name.items():
                                print(f"section Name:{section_name}")
                                print("------------------------")
                                for device_number, info in device_number.items():
                                    print(f"device number:{device_number}")
                                    print(info)
                                    print("------------------------")




                        # graphs = some_function_comparing_all_files
                        pdf.create_pdf_with_graphs_and_data_for_sample(sample_path,
                                                                       f"{file_info.get('sample_name')}.pdf", graph,
                                                                       info_dict)

                        with open(sample_path + '/list of devices measured', 'wb') as file:
                            pickle.dump(list_of_measured_files, file)

                # Information on the polymer

