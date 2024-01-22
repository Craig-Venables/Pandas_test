import os
''' This file contains everything to do with files, this includes the file location as a variable, this is so it can be imported in all files n'''
#other file too test


# notts computers

# excel_path = r"C:\Users\ppxcv1\OneDrive - The University of Nottingham\Documents\Phd\solutions and devices.xlsx"
# main_dir = r'C:\Users\ppxcv1\OneDrive - The University of Nottingham\Desktop\Origin Test Folder\1) Memristors'

# home pc

excel_path = r"C:\Users\Craig-Desktop\OneDrive - The University of Nottingham\Documents\Phd\solutions and devices.xlsx"
main_dir = r"C:\Users\Craig-Desktop\OneDrive - The University of Nottingham\Desktop\Origin Test Folder\1) Memristors"
#main_dir = r"C:\Users\Craig-Desktop\OneDrive - The University of Nottingham\Documents\Phd\2) Data\1) Devices\0) old data backup\1) Memristors"
def check_if_folder_exists(d_path,fol_name):
    if not os.path.exists(str(d_path) + '\\' + f"{fol_name}"):
        os.makedirs(str(d_path) + '\\' + f"{fol_name}")
        return f"{fol_name}", "exists"
    return 'already exists'



def short_name(filepath):
    file_info = extract_folder_names(filepath)
    short_name = file_info.get('sample_name') + " - " + file_info.get('section') + ' - ' + file_info.get('device_number') + " - " + file_info.get('file_name')

    return short_name

def long_name(filepath):
    file_info = extract_folder_names(filepath)
    long_name = file_info.get('type') + " - " + file_info.get('polymer') + " - " + \
                file_info.get('sample_name') + " - " + file_info.get('section') + ' - ' + \
                file_info.get('device_number') + " - " + file_info.get('file_name')
    return long_name



def filereader(filepath):
    with open(filepath, "r") as f:  # open the file as read only
        fread = f.readlines()
        fread.pop(0)
        return fread


def extract_folder_names(file_path, base_folder="Memristors", folder_structure=None):
    # Set default folder structure if not provided
    if folder_structure is None:
        folder_structure = ["type", "polymer", "sample_name", "section", "device_number","file_name"]

    # Extract the relevant part of the path
    start_index = file_path.find(base_folder)
    if start_index != -1:
        relevant_part = file_path[start_index + len(base_folder) + 1:]  # Add 1 to skip the backslash

    # Split the path into directories
    directories = relevant_part.split("\\")  # Split using backslash as the separator

    # Create a dictionary to store the variable names and folder names
    variable_names = {}

    # Generate variable names and store folder names
    for i, (directory, structure) in enumerate(zip(directories, folder_structure)):
        variable_name = f"{structure}"
        variable_names[variable_name] = directory

    return variable_names

