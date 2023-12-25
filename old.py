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
