import os
''' This file contains everything to do with files, this includes the file location as a variable, this is so it can be imported in all files n'''
#other file too test


# notts computers

#excel_path = r"C:\Users\ppxcv1\OneDrive - The University of Nottingham\Documents\Phd\solutions and devices.xlsx"
#main_dir = r'C:\Users\ppxcv1\OneDrive - The University of Nottingham\Desktop\Origin Test Folder\1) Memristors'
#main_dir = r"C:\Users\ppxcv1\OneDrive - The University of Nottingham\Documents\Phd\2) Data\1) Devices\0) old data backup\1) Memristors"
# Template_for_device_xls_path = r"C:\Users\ppxcv1\OneDrive - The University of Nottingham\Documents\Phd\Template for device.xlsx"

# home pc

excel_path = r"C:\Users\Craig-Desktop\OneDrive - The University of Nottingham\Documents\Phd\solutions and devices.xlsx"
main_dir = r"C:\Users\Craig-Desktop\OneDrive - The University of Nottingham\Desktop\Origin Test Folder\1) Memristors"
#main_dir = r"C:\Users\Craig-Desktop\OneDrive - The University of Nottingham\Documents\Phd\2) Data\1) Devices\0) old data backup\1) Memristors"
main_dir = r"C:\Users\Craig-Desktop\OneDrive - The University of Nottingham\Documents\Phd\2) Data\1) Devices\1) Memristors"
# Template_for_device_xls_path = r"C:\Users\Craig-Desktop\OneDrive - The University of Nottingham\Documents\Phd\Template for device.xlsx"
# files to ignore when looking through directory add as appropriate
ignore_files = ('.xlsx',  '.gif', '.bmp', '.tiff', '.ico', '.odt', '.ods', '.odp', '.txt', '.rtf', '.csv', '.json',\
    '.xml', '.yaml', '.html', '.css', '.js', '.php', '.sql', '.log', '.bak', '.tar', '.gz', '.zip', '.7z', '.rar', \
    '.tgz', '.java', '.class', '.jar', '.bat', '.sh', '.ps1', '.cmd', '.dll', '.lib', '.obj', '.pdb', '.exe', '.iso',\
    '.mp3', '.wav', '.flac', '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.pdf', '.epub', '.mobi', '.djvu', '.chm',\
    '.jpg', '.png', '.svg', '.eps', '.ai', '.psd', '.tif', '.bat', '.cfg', '.ini', '.conf', '.md', '.bak', '.patch',\
    '.diff', '.sql', '.bak', '.bak2', '.bak3', '.bak4', '.bak5', '.backup', '.old', '.new', '.temp', '.tmp', '.swp', \
    '.swo', '.swn', '.swo', '.log', '.out', '.err''.doc','.docx','.ogwu','.opju', '.Wdf','.pptx', '.jpeg','.xls')

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

class Tee:
    def __init__(self, file, stdout):
        self.file = file
        self.stdout = stdout
        self.closed = False

    def write(self, data):
        if not self.closed:
            self.file.write(data)
        self.stdout.write(data)

    def flush(self):
        if not self.closed:
            self.file.flush()
        self.stdout.flush()

    def close(self):
        if not self.closed:
            self.file.close()
            self.closed = True
