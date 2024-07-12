import memristors.analysis as eq
import statistics as stats_module
import math
import os

""" any work on the file goes here"""

def txt_file(file_name,file_path,device_path,total_files, list_of_file_stats, file_data, processed_files, short_name,long_name,num_of_sweeps=0,plot_graph=False, save_df=False,re_save_graph=False):
    # began changing this into function not sure yet
    """Loops through each file in the folder and analyses them using the
    functions here"""

    # Percentage completed
    processed_files += 1
    percentage_completed_files = (processed_files / total_files) * 100

    # Checks and returns the sweep type of the file also checks for nan
    # values if nan values are present returns None
    output_file = 'memristors\\error_files.txt'
    sweep_type = eq.check_sweep_type(file_path,output_file)

    if sweep_type == 'Iv_sweep':
        """ for simple iv sweeps"""

        # Performs analysis on the file given returning the dataframe
        analysis_result = eq.file_analysis(file_path, plot_graph, save_df,
                                           device_path, re_save_graph,short_name,long_name)

        num_sweeps, short_name, long_name, data, file_stats, graph = analysis_result

        # keeps count of the number of sweeps by each device
        num_of_sweeps += num_sweeps

        #storing information from analysis
        #list_of_measured_files.append(long_name)
        list_of_file_stats.append(file_stats)
        file_data[f'{file_name}'] = data

        return percentage_completed_files, processed_files, num_of_sweeps, num_sweeps, short_name, long_name, file_data, file_stats
    # else:
    #     # if there is an error in reading the file it will just continue
    #     # skipping
    #     print("Not iv sweep")

        # continue

def device_clasification(sample_sweep_excell_dict, device_folder, section_folder,path):
    """ extracts the classification from the device_number excel sheet for the device level """
    try:
        section_folder = section_folder[0].upper()
        # Take only the first letter from the section_folder
        # Take only the first two digits from the device_folder
        device_folder = device_folder[:2]

        # print(device_folder)
        #print(sample_sweep_excell_dict[section_folder])
        df = sample_sweep_excell_dict[section_folder]
        # Convert device_folder to the same type as in the DataFrame (assuming it's numeric)
        device_folder = int(device_folder)
        # Find the row where the "Device #" matches the specified device_folder
        result_row = df[df["Device #"] == device_folder]
        # Extract the classification value
        classification = result_row["Classification"].values[
            0] if not result_row.empty else None
        # print(classification)
        return (classification)
    except:
        print("please add xls too ", path)
        return None

def process_property(material_stats_dict: dict, property_name: str) -> dict:
    """
    This function processes the property of a material(ie, on off ratio).

    Args:
        material_stats_dict (dict): A dictionary containing the material, polymer, and sample dictionaries.
        property_name (str): The name of the property to be processed.

    Returns:
        dict: A dictionary containing the comprehensive information for each unique sample.
    """
    # Dictionary to store comprehensive information for each unique sample
    comprehensive_sample_info = {}

    # Iterate through the material, polymer, and sample dictionaries
    for material_key, polymer_dict in material_stats_dict.items():

        for polymer_key, sample_dict in polymer_dict.items():
            for sample_key, section_dict in sample_dict.items():
                # print(sample_key)
                # Skip if the sample has already been processed
                if sample_key in comprehensive_sample_info:
                    continue

                # List to store information for all devices in the sample
                all_devices_info = []

                # Iterate through devices in the sample
                for section_key, device_dict in section_dict.items():
                    # print(section_key)
                    for device_key, stats_df in device_dict.items():
                        # print(device_key)
                        # print(stats_df['file_name'].isnull(),'\n', stats_df[property_name])
                        # print(row_index)
                        # device_key, stats_df = dict_items
                        # Check if 'file_name' and property_name exist in stats_df
                        if 'file_name' in stats_df.columns and property_name in stats_df.columns:
                            '''
                            Largest on off ratio algorithm:
                            1)Find a pandas method to find numerical row index of the largest on/off ratio for the current stats dict.
                            1.5) if there is no method, use a for loop which compares the last on/off ratio with the current one (in this loop),
                                 and store the whichever is larger and it's index in a variable defined outside of the loop
                            2)Use that row index to extract the file name for the current device with .iloc
                            '''
                            # print(property_name)
                            # print(stats_df[property_name])
                            max_property_index = stats_df[property_name].index.get_loc(stats_df[property_name].idxmax())
                            property_value = stats_df[property_name].iloc[max_property_index]

                            file_name = stats_df['file_name'].iloc[max_property_index]

                            # Extract the property values for the current device
                            property_values = stats_df[property_name]

                            # Append device information to the list
                            all_devices_info.append({
                                'device_key': device_key,
                                f'{property_name}s': property_values.tolist(),
                                'file_name': file_name,
                                property_name: property_value
                            })

                # Check for NaN values in property_values_all
                if any(math.isnan(value) for device_info in all_devices_info for value in
                       device_info[f'{property_name}s']):
                    print(f"NaN values detected in {property_name}s_all for {material_key}_{polymer_key}_{sample_key}.")

                # Check if property_values_all is empty
                if not all_devices_info:
                    print(f"{property_name}s_all is an empty list for {material_key}_{polymer_key}_{sample_key}.")
                    continue

                # Calculate and store statistical measures
                property_values_all = [value for device_info in all_devices_info for value in
                                       device_info[f'{property_name}s']]
                mean_value = stats_module.mean(property_values_all)
                median_value = stats_module.median(property_values_all)
                mode_value = stats_module.mode(property_values_all)

                # Sort the devices based on mean property_value in descending order
                all_devices_info.sort(key=lambda x: stats_module.mean(x[f'{property_name}s']), reverse=True)

                # # Print the sorted list of devices
                # print(f"Sorted list of devices for {material_key}_{polymer_key}_{sample_key}:")
                # for device_info in all_devices_info:
                #     print(device_info)

                # Store the top 3 devices based on individual property_values
                top3_devices_individual = all_devices_info[:3]

                # Store the comprehensive information for the unique sample name
                comprehensive_sample_info[sample_key] = {
                    'best_device': all_devices_info[0],
                    'top3_devices': top3_devices_individual,
                    f'mean_{property_name}': mean_value,
                    f'median_{property_name}': median_value,
                    f'mode_{property_name}': mode_value
                }

    # Return the comprehensive information for all samples
    return comprehensive_sample_info


