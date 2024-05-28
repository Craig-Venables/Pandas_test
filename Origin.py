import originpro as op
import os

""" For plotting the data into origin """

# def data_copy_origin(material_data):
#     """ function for sorting and moving the good files."""
#
#     def traverse_dict(dictionary):
#         all_data = []
#
#         def _traverse_dict(data, keys_parsed=None):
#             if keys_parsed is None:
#                 keys_parsed = []
#
#             for filename, data in data.items():
#                 keys_parsed.append(filename)
#                 if isinstance(data, dict):
#                     _traverse_dict(data, keys_parsed)
#                 else:
#                     all_data.append((filename, data, keys_parsed.copy()))
#                 keys_parsed.pop()  # Remove the last key after processing
#
#         _traverse_dict(dictionary)
#         return all_data
#
#
#
#     def count_y_for_sample_name(checked_files, sample_name):
#         count_y = 0
#         for key, value in checked_files.items():
#             if " - " + sample_name + " - " in key and value == "y":
#                 count_y += 1
#         return count_y
#
#     data_transverse = traverse_dict(material_data)
#
#
#     for filename, data, keys_parsed in data_transverse:
#         """ Here the data for each file is given as data
#         data = pd dataframe """
#
#         # Pull info on the files from the database of information as follows:
#         material = keys_parsed[0]
#         polymer = keys_parsed[1]
#         sample_name = keys_parsed[2]
#         section = keys_parsed[3]
#         device = keys_parsed[4]
#         print(material, polymer, sample_name, section, device, filename)
#
#         key = f"{material} - {polymer} - {sample_name} - {section} - {device} - {filename}"
#         #print(filename)
#         #print(key)
#         #print(checked_files)
#
#         # filepath for the current file
#         filepath_file = os.path.join(f.main_dir, material, polymer, sample_name, section, device, filename)
#
#         # check if file has been checked already if no move on
#         if key in checked_files:
#             print(f"Graph {filename} has already been checked and marked.")
#             print("")
#         else:
#             print("file not in checked_files")
#
#             # read in the checked_files here keeping it in memory adding too it below:
#
#             # call the class for sorting the files
#             yes_no(filename, keys_parsed, data, filepath_file, checked_files)
#             number = count_y_for_sample_name(checked_files,keys_parsed[2])
#             print(keys_parsed[2], number)
#             # append the checked files array with the names and return saving the iterations
#     # save the checked files once finished
#     save_checked_files(checked_files)


def plot_in_origin(device_data,device_path,plot_type,save_file = True):
    """ This opens an instance of origin for a given folder, takes all the data from a file
    and plots it, this does this for all the data files within the folder. It also saves the data as pictures. """

    save_file = str(device_path) + "\\" + f"{plot_type}" + ' graphs.opju'
    if save_file and os.path.exists(save_file):
        print(f"Skipping origin file, already exists.")
        return
    #print("inside function")
    # Unpack 'device_data' on the other side within a loop
    for device_folder, device_data_dict in device_data.items():
        print(device_folder)
        print("please wait working in origin ...")
        # Access 'data' within 'device_data_dict'
        for file_name, data_dict in device_data_dict.items():

            # Graphs use python for the calculations
            pg = plot(data_dict, file_name,device_path)
            pg.plot_origin_using_python(plot_type)

    # save the file?
    if save_file:
        if op.oext:
            op.save(str(device_path) + "\\" + f"{plot_type}" + ' graphs')
            print("")
            print("saved origin file in " f"{device_path}")
            print("")

    # Closes that instance of origin
    if op.oext:
        op.exit()


class plot:
    """
    Class for all functions for data manipulation

    voltage_data = Voltage data | type: int
    current_data = Current data | type: int
    directory_path = working directory path | type: str
    filename = filename of current file | type: str
    graph_template_folder = Area graph template | type: str
    template_name = template use to plot the graph | type: str
    distance = Distance between electrodes default 100E-9 | type: int
    area = Area between electrodes default 100E-6 | type: int
    save_image = Save images of graphs in directory default = false | type: boolean
    """

    def __init__(self, data_dict, filename, save_image=False, distance=100E-9, area=100E-6) -> None:
        self.data_dict = data_dict
        python_file_path = os.path.dirname(os.path.realpath(__file__)) + '\\'
        graph_template_folder = python_file_path + 'Template folder' + '\\'
        template_name = 'Electron_transport_Final.otpu'

        self._unpack_dataframe()


        self.fn = filename
        self.g_temp_folder = graph_template_folder
        self.temp_name = template_name
        self.area = area
        self.distance = distance
        self.save_img = save_image

        # # start an instance of this the classes needed
        # self.func = dm.functions(self.v_data, self.c_data)
        # self.fm = fm.directory()
        # self.fm.d_path = self.d_path

    def _unpack_dataframe(self):
        """ Unpacks dataframe with the names given """
        for column in self.data_dict.columns:
            setattr(self, column.lower(), self.data_dict.get(column))


    # def plot_into_workbook(self):
    #     # give the file path of the temple.ogwu
    #     working_file = self.g_temp_folder + self.temp_name
    #     wks = op.load_book(working_file)[0]  # from user file folder
    #
    #     # Put array into workbook
    #     wks.from_list(0, self.v_data, 'Voltage')
    #     wks.from_list(1, self.c_data, 'Current')
    #
    #     # fixes name issue, sets names as it's broken in templates, *reportedly fixed now
    #     wksn = op.find_book()  # Changes workbook name
    #     wksn.lname = f"{self.fn}"
    #     wks.plot_cloneable(self.g_temp_folder + f"{self.fn}")
    #     gp = op.find_graph()  # changes graph name
    #     gp.lname = wksn.lname  # longname
    #     # gp.name = wks.name # short name

    def plot_origin_using_python(self, plot_type):
        ''' think this takes arrays of numbers '''
        # This works only for my use case, please ignore

        wks = op.new_book('w', lname=f"{self.fn}", hidden=False)[0]

        # plot first 3 voltage current and abs(current)
        wks.from_list(0, self.voltage, 'Voltage', units='V')
        wks.from_list(1, self.current, 'Current', units='A')
        wks.from_list(2, self.abs_current, 'Abs Current')

        # get positive values and plot for positive regions only
        wks.from_list(3, self.current_density_ps, 'Current Density', units='A/cm^2')
        wks.from_list(4, self.electric_field_ps, 'Electric Field', units='V/cm')
        wks.from_list(5, self.inverse_resistance_ps, 'Current/Voltage', units='A/V')
        wks.from_list(6, self.sqrt_voltage_ps, 'Voltage^1/2', units='V^1/2')

        # get positive values and plot for positive regions only
        wks.from_list(7, self.voltage_ng, 'abs(Voltage)', units='V')
        wks.from_list(8, self.current_ng, 'abs(Current)', units='A')
        wks.from_list(9, self.current_density_ng, 'abs(Current Density)', units='A/cm^2')
        wks.from_list(10, self.electric_field_ng, 'abs(Electric Field)', units='V/cm')
        wks.from_list(11, self.inverse_resistance_ng, 'abs(Current/Voltage)', units='A/v')
        wks.from_list(12, self.sqrt_voltage_ng, 'abs(Voltage^1/2)', units='V^1/2')

        # plots the graph using template provided, must be a clonable template
        electron_transport = self.g_temp_folder + 'Electron_transport_Final.otpu'
        iv_log = self.g_temp_folder + 'LOG+IV_v3.otpu'
        # wks.plot_cloneable(iv_log)
        #print(self.fn , plot_type)
        #print(electron_transport)

        if plot_type == 'transport':
            wks.plot_cloneable(electron_transport)
            # Fix short and long names of files
            wks.lname = f"{self.fn}"
            gp = op.find_graph()
            #print(gp)
            gp.lname = wks.lname
            gp.name = wks.name

            #self.save_transport()

        if plot_type == 'iv_log':
            wks.plot_cloneable(iv_log)
            # Fix short and long names of files
            wks.lname = f"{self.fn}"
            gp = op.find_graph()
            gp.lname = wks.lname
            gp.name = wks.name

            #self.save_iv_log()

    # if you want to save the images as a png file
    # def save_transport(self):
    #     # check_if_folder_exists(self.d_path, 'Exported Graphs png (Transport)')
    #     # reference if needed
    #
    #     self.fm.fol_name = 'Exported Graphs png (Transport)'
    #     self.fm.check_if_folder_exists()
    #     g = op.find_graph()
    #     filename_ext = f"{self.fn}" + '.png'
    #     exported_path = self.d_path + '\\Exported Graphs png (Transport)'
    #     g.save_fig(str(exported_path) + '\\' + f"{filename_ext}")
    #     print("Transport image saved")

    # def save_iv_log(self):
    #     # check_if_folder_exists(self.d_path, 'Exported Graphs png (iv_log)')
    #     # reference if needed
    #
    #     #self.fm.fol_name = 'Exported Graphs png (iv_log)'
    #     #self.fm.check_if_folder_exists()
    #
    #     g = op.find_graph()
    #     filename_ext = f"{self.fn}" + '.png'
    #     exported_path = self.d_path + '\\Exported Graphs png (iv_log)'
    #     g.save_fig(str(exported_path) + '\\' + f"{filename_ext}")
    #     # , width=500
    #     print("IV LOG image saved")

    def tile_all_windows(self):
        if self == True:
            op.lt_exec('win-s T')
