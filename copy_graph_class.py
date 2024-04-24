import os
import matplotlib.pyplot as plt
import keyboard
import shutil
import plotting as plotting
import pickle
import sys
import file as f

def data_copy(material_data):
    """ function for sorting and moving the good files."""

    def traverse_dict(dictionary):
        all_data = []

        def _traverse_dict(data, keys_parsed=None):
            if keys_parsed is None:
                keys_parsed = []

            for filename, data in data.items():
                keys_parsed.append(filename)
                if isinstance(data, dict):
                    _traverse_dict(data, keys_parsed)
                else:
                    all_data.append((filename, data, keys_parsed.copy()))
                keys_parsed.pop()  # Remove the last key after processing

        _traverse_dict(dictionary)
        return all_data

    def load_checked_files():
        try:
            with open('checked_files.pkl', 'rb') as f:

                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def save_checked_files(checked_files):
        with open('checked_files.pkl', 'wb') as f:
            pickle.dump(checked_files, f)

    def count_y_for_sample_name(checked_files, sample_name):
        count_y = 0
        for key, value in checked_files.items():
            if " - " + sample_name + " - " in key and value == "y":
                count_y += 1
        return count_y

    data_transverse = traverse_dict(material_data)

    # import-checked files here
    checked_files = load_checked_files()


    for filename, data, keys_parsed in data_transverse:
        """ Here the data for each file is given as data 
        data = pd dataframe """

        # Pull info on the files from the database of information as follows:
        material = keys_parsed[0]
        polymer = keys_parsed[1]
        sample_name = keys_parsed[2]
        section = keys_parsed[3]
        device = keys_parsed[4]
        print(material, polymer, sample_name, section, device, filename)

        key = f"{material} - {polymer} - {sample_name} - {section} - {device} - {filename}"

        # filepath for the current file
        filepath_file = os.path.join(f.main_dir, material, polymer, sample_name, section, device, filename)

        # check if file has been checked already if no move on
        if key in checked_files:
            print(f"Graph {filename} has already been checked and marked.")
            print("")
        else:
            print("file not in checked_files")

            # read in the checked_files here keeping it in memory adding too it below:

            # call the class for sorting the files
            yes_no(filename, keys_parsed, data, filepath_file, checked_files)
            number = count_y_for_sample_name(checked_files,keys_parsed[2])
            print(keys_parsed[2], number)
            # append the checked files array with the names and return saving the iterations
    # save the checked files once finished
    save_checked_files(checked_files)



class yes_no():
    ''' yes or no too the specific graph

    device_file_path = filepath for the device folder | type: str

    :returns
    '''

    #def __init__(self, data_dict,file_info_dict) -> None:
    def __init__(self, filename,keys_parsed,dataframe,filepath_file,checked_files) -> None:
        self.filename = filename
        self.material = keys_parsed[0]
        self.polymer = keys_parsed[1]
        self.sample_name = keys_parsed[2]
        self.section_folder = keys_parsed[3]
        self.device_folder = keys_parsed[4]
        self.dataframe = dataframe
        self.filepath = filepath_file
        self.checked_files = checked_files

        self._unpack_dataframe_dd()
        #self._unpack_dataframe_fid()

        # need filepath here somewhere
        #self.file_path = file_info_dict['file_path']

        self.output_folder = (
            r'C:\Users\Craig-Desktop\OneDrive - The University of Nottingham\Documents\Phd\1) Projects\1) Memristors\1) Curated Data')

        self.yes_no_to_data()

    def _unpack_dataframe_dd(self):
        """ Unpacks dataframe with the names given """
        for column in self.dataframe.columns:
            setattr(self, column.lower(), self.dataframe.get(column))


    def create_folder_if_not_exists(self, folder):
        folder_path = os.path.join(folder)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder created: {folder_path}")
        else:
            print(f"Folder already exists: {folder_path}")

    def yes_no_to_data(self):
        checked_files = self.checked_files
        name_in_checked_files = f"{self.material} - {self.polymer} - {self.sample_name} - {self.section_folder} - {self.device_folder} - {self.filename}"


        base_filename = os.path.basename(self.filename)
        output_file_path = os.path.join(self.output_folder, self.filename)

        fig = plotting.graph_temp(self.voltage, self.current, self.abs_current, self.material, self.polymer,
                                  self.sample_name, self.section_folder, self.device_folder, self.filename)

        #print(self.dataframe)
        print(os.path.join(self.output_folder, self.material, self.polymer, self.sample_name))

        print("Do you want to copy this file? (y/n): or exit (s) ")
        event = keyboard.read_event(suppress=True)

        if event.name == "y" and event.event_type == keyboard.KEY_DOWN:
            # yes is pressed

            # Create the output folder in the new destination
            output_folder2 = os.path.join(self.output_folder, self.material, self.polymer, self.sample_name)
            self.create_folder_if_not_exists(output_folder2)

            # modify the filename for the new location
            modified_filename = self.modify_filename(self.filename)
            output_file_path = os.path.join(output_folder2, modified_filename)

            # copy the file to the output folder
            shutil.copy(self.filepath, output_file_path)
            # Add y to the checked files
            checked_files[name_in_checked_files] = "y"

            # save sata from dataframe
            calculations_folder = os.path.join(output_folder2, "device_data_calculations")
            self.create_folder_if_not_exists(calculations_folder)

            # create images folder within the curated data
            python_images_folder = os.path.join(output_folder2, "Python_images")
            self.create_folder_if_not_exists(python_images_folder)
            # save the figure
            figure_path = os.path.join(python_images_folder, f"{modified_filename}.png")
            fig.savefig(figure_path)
            print(f"File saved successfully at {figure_path}")

            # save the data for use later
            calculations_file_path = os.path.join(calculations_folder, f"{modified_filename}.txt")
            self.dataframe.to_csv(calculations_file_path, sep='\t', index=False)

            # with open(calculations_file_path, "w") as calculations_file:
            #     calculations_file.write(self.data.to_string(index=False))
            #
            # with open(calculations_file_path,'w',encoding='utf-8') as file:
            #     file.write(self.data)
            #self.save_checked_files(checked_files)



        if event.name == "s" and event.event_type == keyboard.KEY_DOWN:
            self.save_checked_files(checked_files)
            sys.exit()


        elif event.name == "n" and event.event_type == keyboard.KEY_DOWN:
            checked_files[name_in_checked_files] = "n"

        plt.close()

        print("")
        #self.save_checked_files(checked_files)

    def load_checked_files(self):
        try:
            with open('checked_files.pkl', 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def save_checked_files(self, checked_files):
        with open('checked_files.pkl', 'wb') as f:
            pickle.dump(checked_files, f)

    def modify_filename(self, original_filename):
        # Customize your filename modification logic here,
        # For example, you can add prefixes, suffixes, or change the extension
        modified_filename = f"{self.section_folder} - {self.device_folder} - " + original_filename
        return modified_filename


    # def load_checked_files(self):
    #     checked_files = {}
    #     if os.path.exists(self.checked_files_path):
    #         with open(self.checked_files_path, 'r') as file:
    #             for line in file:
    #                 filename, state = line.strip().split(',')
    #                 # this will break if there are any empty spaces underneath
    #                 checked_files[filename] = state
    #
    #     return checked_files

    # def save_checked_files(self, checked_files):
    #     with open(self.checked_files_path, 'w') as file:
    #         for filename, state in checked_files.items():
    #             file.write(f"{filename},{state}\n")


# def yes_no_to_data(self):
    #     #print(self.on_off_ratio)
    #     #print('Filename: ', self.filename)
    #
    #     checked_files = self.load_checked_files()
    #     name_in_checked_files = f"{self.material} - " + f"{self.polymer} - " + f"{self.sample_name} - " + f"{self.section_folder} - " + f"{self.device_folder} - " + f"{self.file_name} - "
    #
    #     if not os.path.exists(self.output_folder):
    #         os.makedirs(self.output_folder)
    #
    #     # is the filename already contained in the document checked files
    #     if name_in_checked_files in checked_files:
    #         print(f"Graph {self.filename}  has already checked and marked ")
    #         print("")
    #     else:
    #         # if self.v_data == 1000:
    #         #     print("Skipping file due to missing data.")
    #         #     checked_files[name_in_checked_files] = "skipped no data"
    #    #else:
    #         base_filename = os.path.basename(self.file_name)
    #         output_file_path = os.path.join(self.output_folder, self.file_name)
    #
    #         # should reuse code but cba this will do for now
    #         fig = plotting.graph_temp(self.voltage, self.current, self.abs_current, self.material,self.polymer,self.sample_name,self.section_folder,self.device_folder,self.file_name)
    #
    #         print("Do you want to copy this file? (y/n): ")
    #         event = keyboard.read_event(suppress=True)
    #
    #         if event.name == "y" and event.event_type == keyboard.KEY_DOWN:
    #             output_folder2 = os.path.join(self.output_folder, self.material, self.polymer,
    #                                           self.sample_name)
    #             self.create_folder_if_not_exists(output_folder2)
    #
    #             modified_filename = self.modify_filename(self.file_name)
    #
    #             output_file_path = os.path.join(output_folder2, modified_filename)
    #             shutil.copy(self.file_path, output_file_path)
    #             checked_files[name_in_checked_files] = "y"
    #
    #             # Save self.save_data to a file in device_data_calculations folder
    #             calculations_folder = os.path.join(output_folder2, "device_data_calculations")
    #             self.create_folder_if_not_exists(calculations_folder)
    #
    #             # save the data for use later
    #             # calculations_file_path = os.path.join(calculations_folder, f"{modified_filename}.txt")
    #             # with open(calculations_file_path, "w") as calculations_file:
    #             #     calculations_file.write(self.data_dict.to_string(index=False))
    #
    #             # Save the figure generated in the "Python_images" folder
    #             python_images_folder = os.path.join(output_folder2, "Python_images")
    #             self.create_folder_if_not_exists(python_images_folder)
    #             figure_path = os.path.join(python_images_folder, f"{modified_filename}.png")
    #             fig.savefig(figure_path)
    #
    #         elif event.name == "n" and event.event_type == keyboard.KEY_DOWN:
    #             checked_files[name_in_checked_files] = "n"sss
    #
    #         plt.close()
    #
    #         print("")
    #     self.save_checked_files(checked_files)

