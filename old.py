
# print(material_sweeps_dict)

# # Assuming material_names_dict is the given dictionary
# for material, material_dict in material_names_dict.items():
#     print("Material Name:", material)
#
#     for polymer, polymer_dict in material_dict.items():
#         print("  Polymer Name:", polymer)
#
#         for sample_name, sample_info in polymer_dict.items():
#             print("    Sample Name:", sample_name)
#
#             # Extract additional information if needed
#             for key, value in sample_info.items():
#                 print(f"      {key}: {value}")

# # Assuming material_names_dict is the given dictionary
# material_name = list(material_names_dict['material'].keys())[0]
# polymer_name = list(material_names_dict['material'][material_name]['polymer'].keys())[0]
# sample_name = material_names_dict['material'][material_name]['polymer'][polymer_name]['sample_name']
#
# print("Material Name:", material_name)
# print("Polymer Name:", polymer_name)
# print("Sample Name:", sample_name)


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


# print the file info dictionary
# for file_key, file_info in file_info_dict.items():
#     print(f'File Key: {file_key}')
#     print(f'Material: {file_info["material"]}')
#     print(f'Polymer: {file_info["polymer"]}')
#     print(f'Sample Name: {file_info["sample_name"]}')
#     print(f'Section Folder: {file_info["section_folder"]}')
#     print(f'Device Folder: {file_info["device_folder"]}')
#     print(f'File Name: {file_info["file_name"]}')
#     print(f'File Path: {file_info["file_path"]}')
#     print('-' * 50)



# # Information on the polymer
# for sample_name, section_name in sample_sweeps_dict.items():
#     print("------------------------")
#     print(f"sample Name:{sample_name}")
#     print("------------------------")
#     for section_name, device_number in section_name.items():
#         print(f"section Name:{section_name}")
#         print("------------------------")
#         for device_number, info in device_number.items():
#             print(f"device number:{device_number}")
#             print(info)
#             print("------------------------")
#
#
# for sample_name, section_name in sample_stats_dict.items():
#     print("------------------------")
#     print(f"sample Name:{sample_name}" )
#     print("------------------------")
#     for section_name, device_number in section_name.items():
#         print(f"section Name:{section_name}")
#         print("------------------------")
#         for device_number, info in device_number.items():
#             print(f"device number:{device_number}")
#             print(info)
#             print("------------------------")






# def split_data_in_sect(voltage, current,v_max,v_min):
#     positive = [(v, c) for v, c in zip(voltage, current) if 0 <= v <= v_max]
#     negative = [(v, c) for v, c in zip(voltage, current) if v_min <= v <= 0]
#
#     print (len(positive),len(negative))
#
#     # this makes sure that the arrays positive and negative are of the same length if not
#     # it repeats the last value , this shouldn't have too much of an effect on the result
#     len_positive, len_negative = len(positive), len(negative)
#     if len_positive < len_negative:
#         final_positive_value = positive[-1]
#         positive += [final_positive_value] * (len_negative - len_positive)
#     elif len_negative < len_positive:
#         final_negative_value = negative[-1]
#         negative += [final_negative_value] * (len_positive - len_negative)
#
#     positive1 = list(zip(*positive[:len(positive)//2]))
#     positive2 = list(zip(*positive[len(positive)//2:]))
#
#     negative1 = list(zip(*negative[:len(negative)//2]))
#     negative2 = list(zip(*negative[len(negative)//2:]))
#
#     # create dataframe for device
#     sections = {'voltage_ps_sect1': positive1[0],
#                 'current_ps_sect1': positive1[1],
#                 'voltage_ps_sect2': positive2[0],
#                 'current_ps_sect2': positive2[1],
#                 'voltage_ng_sect1': negative1[0],
#                 'current_ng_sect1': negative1[1],
#                 'voltage_ng_sect2': negative2[0],
#                 'current_ng_sect2': negative2[1]}
#
#     # print(len(negative1[0]),len(negative2[0]))
#     # print(len(negative1[1]), len(negative2[1]))
#     #print(negative1, negative2)
#
#     print(len(positive1), len(positive2))
#     df_sections = pd.DataFrame(sections)
#     return df_sections



# def split_data_in_sect(voltage, current,v_max,v_min):
#     positive = [(v, c) for v, c in zip(voltage, current) if 0 <= v <= v_max]
#     negative = [(v, c) for v, c in zip(voltage, current) if v_min <= v <= 0]
#
#     # there is a better way of doing this for sure
#     positive1 = list(zip(*positive[:len(positive)//2]))
#     positive2 = list(zip(*positive[len(positive)//2:]))
#
#     negative1 = list(zip(*negative[:len(negative)//2]))
#     negative2 = list(zip(*negative[len(negative)//2:]))
#     # his dosnt work wshen there is an uneven number for v/c data
#     # create dataframe for device
#     sections = {'voltage_ps_sect1': positive1[0],
#                 'current_ps_sect1': positive1[1],
#                 'voltage_ps_sect2': positive2[0],
#                 'current_ps_sect2': positive2[1],
#                 'voltage_ng_sect1': negative1[0],
#                 'current_ng_sect1': negative1[1],
#                 'voltage_ng_sect2': negative2[0],
#                 'current_ng_sect2': negative2[1]}
#
#     print("Negative1:", negative1)
#     print(len(negative1[0]))
#     print("Negative2:", negative2)
#     print(len(negative2[0]))
#     print("Positive1:", positive1)
#     print(len(positive1[0]))
#     print("Positive2:", positive2)
#     print(len(positive2[0]))
#
#     df_sections = pd.DataFrame(sections)
#     return df_sections
#     #for debugging


# def split_data_in_sect(voltage, current,v_max,v_min):
#     positive = [(v, c) for v, c in zip(voltage, current) if 0 <= v <= v_max]
#     negative = [(v, c) for v, c in zip(voltage, current) if v_min <= v <= 0]
#
#     # Pad the shorter sections with NaN
#     positive1 = list(zip_longest(*positive[:len(positive) // 2], fillvalue=np.nan))
#     positive2 = list(zip_longest(*positive[len(positive) // 2:], fillvalue=np.nan))
#
#     negative1 = list(zip_longest(*negative[:len(negative) // 2], fillvalue=np.nan))
#     negative2 = list(zip_longest(*negative[len(negative) // 2:], fillvalue=np.nan))
#
#     # Create a dictionary for DataFrame
#
#     # his dosnt work wshen there is an uneven number for v/c data
#     # create dataframe for device
#     sections = {'voltage_ps_sect1': positive1[0],
#                 'current_ps_sect1': positive1[1],
#                 'voltage_ps_sect2': positive2[0],
#                 'current_ps_sect2': positive2[1],
#                 'voltage_ng_sect1': negative1[0],
#                 'current_ng_sect1': negative1[1],
#                 'voltage_ng_sect2': negative2[0],
#                 'current_ng_sect2': negative2[1]}
#
#     print("Negative1:", negative1)
#     print(len(negative1[0]))
#     print("Negative2:", negative2)
#     print(len(negative2[0]))
#     print("Positive1:", positive1)
#     print(len(positive1[0]))
#     print("Positive2:", positive2)
#     print(len(positive2[0]))
#
#     df_sections = pd.DataFrame(sections)
#     return df_sections
#     #for debugging





# def extract_components(file_path):
#     # Find the index of "Memristors" (case insensitive)
#     index_of_memristors = file_path.lower().find('1) Memristors')
#
#     # Extract the substring from "1) Memristors" onwards
#     if index_of_memristors != -1:
#         relevant_part = file_path[index_of_memristors + len('1) Memristors'):]
#
#         # Split the relevant part by '\\' to get individual parts
#         parts = relevant_part.split('\\')
#
#         # Extracting components
#         if len(parts) == 6:
#             return {
#                 'Memristor Type': '1) Memristors ' + parts[0],
#                 'Polymer Used': parts[2],
#                 'Sample Name': parts[3],
#                 'Section': parts[4],
#                 'Device Number': parts[5]
#             }
#         else:
#             raise ValueError("File path structure doesn't match the expected format.")
#     else:
#         raise ValueError("The string '1) Memristors' is not present in the file path.")

#old unpack method

# self.v_data = self.data.get("Voltage")
# self.c_data = self.data.get("Current")
# self.abs_c_data = self.data.get("Abs_Current")
# self.resistance = self.data.get("Resistance")
# self.v_data_ps = self.data.get("Voltage_ps")
# self.c_data_ps = self.data.get("Current_ps")
# self.v_data_ng = self.data.get("Voltage_ng")
# self.c_data_ng = self.data.get("Current_ng")
# self.log_res = self.data.get("Log_Resistance")
# self.abs_c_data_ps = self.data.get("Abs_Current_ps")
# self.abs_c_data_ng = self.data.get("Abs_Current_ng")
# self.c_density_ps = self.data.get("Current_Density_ps")
# self.c_density_ng = self.data.get("Current_Density_ng")
# self.e_field_ps = self.data.get("Electric_field_ps")
# self.e_field_ng = self.data.get("Electric_field_ng")
# self.inv_res_ps = self.data.get("Inverse_resistance_ps")
# self.inv_res_ng = self.data.get("Inverse_resistance_ng")
# self.sqrt_v_data = self.data.get("Sqrt_Voltage")
# self.on_off_ratio = self.data.get("on_off_ratio")
