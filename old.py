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
