import os
import Class_python_plot as cpp
import matplotlib.pyplot as plt
import Usefull_Functions as uf
import keyboard
import shutil


class yes_no():
    ''' yes or no too the specific graph

    device_file_path = filepath for the device folder | type: str

    :returns
    '''

    def __init__(self, v_data="", c_data="", abs_c_data="", resistance_on_value="", resistance_off_value="",
                 voltage_on_value="", voltage_off_value="", resistance="", log_resistance="", times="",
                 on_off_ratio="", filename="", device_number="", section_name="", device_name="", polymer_name="",
                 np_material_or_stock="", full_path="", save_data="") -> None:


    unpackdataframe()
        # data parsed through from instance class was ran
        self.v_data = v_data
        self.c_data = c_data
        self.abs_c_data = abs_c_data
        self.resistance_on_value = resistance_on_value
        self.resistance_off_value = resistance_off_value
        self.voltage_on_value = voltage_on_value
        self.voltage_off_value = voltage_off_value
        self.resistance = resistance
        self.log_resistance = log_resistance
        self.times = times
        self.on_off_ratio = on_off_ratio
        self.filename = filename
        self.device_number = device_number
        self.section_name = section_name
        self.device_name = device_name
        self.polymer_name = polymer_name
        self.np_material_or_stock = np_material_or_stock
        self.full_path = full_path
        self.save_data = save_data


        self.output_folder = (
            r'C:\Users\Craig-Desktop\OneDrive - The University of Nottingham\Documents\Phd\1) Projects\1) Memristors\1) Curated Data')
        self.checked_files_path = (
            r'C:\Users\Craig-Desktop\OneDrive - The University of Nottingham\Documents\Phd\1) Projects\1) Memristors\1) Curated Data\checked_files.txt')

        self.yes_no_to_data()

    def create_folder_if_not_exists(self, folder):
        folder_path = os.path.join(folder)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder created: {folder_path}")
        else:
            print(f"Folder already exists: {folder_path}")

    def yes_no_to_data(self):
        #print(self.on_off_ratio)
        #print('Filename: ', self.filename)

        checked_files = self.load_checked_files()
        name_in_checked_files = f"{self.np_material_or_stock} - " + f"{self.polymer_name} - " + f"{self.device_name} - " + f"{self.section_name} - " + f"{self.device_number} - " + f"{self.filename} - "

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        # is the filename already contained in the document checked files
        if name_in_checked_files in checked_files:
            print(f"Graph {self.filename}  has already checked and marked ")
            print("")
        else:
            if self.v_data == 1000:
                print("Skipping file due to missing data.")
                checked_files[name_in_checked_files] = "skipped no data"
            else:
                base_filename = os.path.basename(self.full_path)
                output_file_path = os.path.join(self.output_folder, self.filename)

                # terrible way of doing this but plots the graphs using the class plot_python_single
                a = cpp.plot_python_single_sweep(self.v_data, self.c_data, self.abs_c_data)

                a.on_off_ratio = self.on_off_ratio
                a.filename = self.filename
                a.section_name = self.section_name
                a.device_name = self.device_name
                a.polymer_name = self.polymer_name
                a.device_number = self.device_number
                a.np_materials = self.np_material_or_stock
                a.main_plot()


                print("Do you want to copy this file? (y/n): ")
                event = keyboard.read_event(suppress=True)

                if event.name == "y" and event.event_type == keyboard.KEY_DOWN:
                    output_folder2 = os.path.join(self.output_folder, self.np_material_or_stock, self.polymer_name,
                                                  self.device_name)
                    uf.create_folder_if_not_exists(output_folder2)

                    modified_filename = self.modify_filename(self.filename)

                    output_file_path = os.path.join(output_folder2, modified_filename)
                    shutil.copy(self.full_path, output_file_path)
                    checked_files[name_in_checked_files] = "y"

                    # Save self.save_data to a file in device_data_calculations folder
                    calculations_folder = os.path.join(output_folder2, "device_data_calculations")
                    uf.create_folder_if_not_exists(calculations_folder)
                    calculations_file_path = os.path.join(calculations_folder, f"{modified_filename}.txt")
                    with open(calculations_file_path, "w") as calculations_file:
                        calculations_file.write(self.save_data)

                    # Save the figure generated by a.main_plot in the "Python_images" folder
                    python_images_folder = os.path.join(output_folder2, "Python_images")
                    uf.create_folder_if_not_exists(python_images_folder)
                    figure_path = os.path.join(python_images_folder, f"{modified_filename}.png")
                    a.save_plot(figure_path)  # Assuming you have a save_plot method in your class


                elif event.name == "n" and event.event_type == keyboard.KEY_DOWN:
                    checked_files[name_in_checked_files] = "n"

                plt.close()

                print("")
            self.save_checked_files(checked_files)


    def load_checked_files(self):
        checked_files = {}
        if os.path.exists(self.checked_files_path):
            with open(self.checked_files_path, 'r') as file:
                for line in file:
                    filename, state = line.strip().split(',')
                    # this will break if there are any empty spaces underneath
                    checked_files[filename] = state

        return checked_files

    def save_checked_files(self, checked_files):
        with open(self.checked_files_path, 'w') as file:
            for filename, state in checked_files.items():
                file.write(f"{filename},{state}\n")

    def modify_filename(self, original_filename):
        # Customize your filename modification logic here,
        # For example, you can add prefixes, suffixes, or change the extension
        modified_filename = f"{self.section_name} - {self.device_number} - " + original_filename
        return modified_filename
