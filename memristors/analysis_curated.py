import os
import memristors.Files_ as Files_
import Graph.Origin.Origin as Origin

""" for working on the currated data"""
""" Curated data Analysis"""

# mike_smith
# https://github.com/MikeSmithLabTeam/filehandling/tree/master?tab=readme-ov-file
# using glob

#if */*/file*.png
def currated_data(path):
    global file_stats
    print("working on currated data")
    for type in os.listdir(path):
        type_path = os.path.join(path, type)
        if os.path.isdir(type_path):  # Check if material_path is a directory
            # Navigate through sub-folders (e.g., polymer)
            polymer_stats_dict = {}
            polymer_sweeps_dict = {}
            polymer_data = {}
            polymer_names_dict = {}

            total_samples = sum(1 for _ in os.listdir(path) if os.path.isdir(os.path.join(path, _)))
            total_files = sum(len(files) for _, _, files in os.walk(path))
            processed_samples = 0
            processed_files = 0

            print("type - ",type)

            for material in os.listdir(type_path):
                material_path = os.path.join(type_path, material)
                if os.path.isdir(material_path):  # Check if polymer_path is a directory
                # ie ws2, zn-ci-in-s , polymer
                    print("material - ",material)


                    for sample in os.listdir(material_path):
                        sample_path = os.path.join(material_path, sample)
                        if os.path.isdir(sample_path):  # Check if polymer_path is a directory
                        # ie D-23
                            processed_samples += 1  # Add one to the number of samples measured
                            percentage_completed = (processed_samples / total_samples) * 100
                            #print("sample - ",sample)
                            on_values = []
                            off_values = []
                            file_names = []
                            file_data = {}
                            list_of_file_stats = []
                            sample_data = {}

                            for file_name in (os.listdir(sample_path)):
                                file_path = os.path.join(sample_path, file_name)
                                """ For each file """
                                #print(file_name)
                                if file_name.endswith('.txt'):
                                    # for all files that end in txt

                                    short_name = sample + " - " + file_name
                                    long_name = type + " - " + material + " - " + sample + " - " + file_name

                                    result = Files_.txt_file(file_name, file_path, sample_path, total_files, list_of_file_stats, file_data, processed_files, short_name, long_name)

                                    if result is not None:
                                        percentage_completed_files, processed_files, num_of_sweeps, num_sweeps, short_name, long_name, file_data, file_stats = result
                                    else:
                                        print(
                                            f'Warning: mem_txt.txt_file returned None for file {file_name, file_path}')
                                        # Handle the None case appropriately, perhaps by setting default values

                                    resistance_on_value = file_stats.get('resistance_on_value')
                                    resistance_off_value = file_stats.get('resistance_off_value')

                                    #print(resistance_on_value[0],resistance_off_value[0])
                                    file_names.append(file_name)

                                    # resistance on/off values
                                    if resistance_on_value is not None:
                                        on_values.append(resistance_on_value.iloc[0])  # Append the first value to the on_values list
                                        #print("on value", resistance_on_value.iloc[0])
                                    else:
                                        print("on value not found")

                                    if resistance_off_value is not None:
                                        off_values.append(resistance_off_value.iloc[0])  # Append the first value to the off_values list
                                        #print("off value", resistance_off_value.iloc[0])
                                    else:
                                        print("off value not found")

                                    sample_data[f'{sample}'] = file_data
                            #print(on_values)
                            # plot
                            # plotting.plot_histograms(on_values,off_values)
                            # plotting.plot_index_vs_values(on_values,off_values)
                            # plotting.plot_filenames_vs_values(file_names, on_values, off_values)
                            #
                            # plot in origin here
                            Origin.plot_in_origin(sample_data, sample_path, 'transport')
                            Origin.plot_in_origin(sample_data, sample_path, 'iv_log')

                                    # calculate the stuff for the whole device
                                    # histogram the resistance Von and Voff and graph
                                    # histogram the resistance Ron and Roff and graph
                                    # Plot all graphs in origin
                                    # add gifs of all devices for later


                                    #

    #         # More dictionary stuff
    #         material_stats_dict[f'{material}'] = polymer_stats_dict
    #         material_sweeps_dict[f'{material}'] = polymer_sweeps_dict
    #         material_data[f'{material}'] = polymer_data
    #
    # return material_stats_dict, material_sweeps_dict, material_data, file_info_dict