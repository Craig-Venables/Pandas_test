def extract_folder_names(file_path, base_folder="Memristors", folder_structure=None):
    # Set default folder structure if not provided
    if folder_structure is None:
        folder_structure = ["type", "polymer", "sample_name", "section", "device_number"]

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

