import pandas as pd
import numpy
import os
import Data as eq
import pdf as pdf
import matplotlib.pyplot as plt
import excell as exc
import plot as plot
import file as f
from file import filepath, excel_path
import excell as ex

# pip install reportlab matplotlib

# to add
# Todo add in the device name and polymer etc into the graphs when they get saved
# Todo Statistics- pull data from the statisitcs sheet i fill out when measuring the devices
#  - creat a file that saves all the data collected from each device an sweeps within the data
# - histogram all the data
# - reorganise the functions
#
# Add a try except when file reading, so if the first way dosnt work it tries something else.
# i.e tries csv or a different method of extracting data from a text file
# add something about working out what kind of data i am taking and it should react acodingly
# have it create the origin graphs for all files towards the end, hiwever only do this if there isnt already an origin
# file created for each

# creats a sub folder that containes all information used within python called "python info" here oit saves all the
# dataframes, the arry info and anything else ready for use later, create another folder named images where it saves
# all the images for each file and within that have another for each of the looped data with all the individual
# images in, with a full overview of each create a final overview pdf of each device with all the sweeps information
# ie average enclosed area, avaerage switching
#

# find a way to incorporate the file created that keeps track of all the info from each sweep from past resuts where
# i give the endurance nuber of sweeps etc celled _____

save_df = False
plot_graph = True
re_analyse = True
eq.set_pandas_display_options()


# Function to perform an operation on a file
def process_file(file_path):
    # Perform your operation on the file here
    pass


# Function to run after processing all files in a folder
def full_device_info():
    # Perform action after processing all files
    pass


# Navigate through the main directory
main_dir = r'C:\Users\ppxcv1\OneDrive - The University of Nottingham\Desktop\Origin Test Folder\1) Memristors'
for type_folder in os.listdir(main_dir):
    type_path = os.path.join(main_dir, type_folder)
    if os.path.isdir(type_path):
        # Navigate through sub-folders (e.g., polymer)
        for polymer_folder in os.listdir(type_path):
            polymer_path = os.path.join(type_path, polymer_folder)

            if os.path.isdir(polymer_path):
                # Navigate through sample_name folders
                for sample_name in os.listdir(polymer_path):
                    sample_path = os.path.join(polymer_path, sample_name)
                    print("working on ", sample_name)

                    if os.path.isdir(sample_path):
                        # Anything to device that doesn't require information on individual sweeps
                        # sample name ie D14-Stock-Gold-PVA(2%)-Gold-s7
                        # Pull info from excell sheet here

                        info_dict = exc.save_info(sample_name,f.excel_path,sample_path)

                        print("working on", sample_path)
                        # Navigate through section folders
                        for section_folder in os.listdir(sample_path):
                            # Anything to section that doesn't require information on individual sweeps
                            section_path = os.path.join(sample_path, section_folder)
                            if os.path.isdir(section_path):
                                # Navigate through device_number folders
                                for device_folder in os.listdir(section_path):
                                    device_path = os.path.join(section_path, device_folder)
                                    #
                                    if os.path.isdir(device_path):

                                        # keeps a list of all files processed as well as each area measured
                                        list_of_measured_files = []
                                        list_of_areas = []
                                        list_of_areas_loops = []
                                        list_of_looped_array_info = []
                                        list_of_df = []
                                        list_of_graphs = []

                                        # add more here into how each array changes over each array
                                        # Process each file in the device_number folder
                                        for file_name in os.listdir(device_path):
                                            if file_name.endswith('.txt'):

                                                # Does work on the file here

                                                # checks If in excell sheet on file its capacitive or not if capacative does something else

                                                file_path = os.path.join(device_path, file_name)

                                                file_info, short_name, long_name, df, area, areas_loops, looped_array_info, graph = eq.file_analysis(
                                                    file_path, plot_graph, save_df,device_path)
                                                print("file_info",type(file_info))

                                                # add check to see if device is capacitive then ignore area maybe
                                                # check file maybe change loops into data into and averaging it check
                                                # needs to be added that does somthing if there is only  half loop ie
                                                # 0-1-0-1 etc this can be done by looking at vmax and min and if 0 is
                                                # vmin or vmax it assumes just a sweep within one region

                                                # append all the information to a master set of arrays
                                                list_of_df.append(df)
                                                list_of_measured_files.append(file_info)
                                                list_of_areas.append(area)
                                                list_of_areas_loops.append(areas_loops)
                                                list_of_looped_array_info.append(looped_array_info)
                                                list_of_graphs.append(graph)

                                                if areas_loops is None and looped_array_info is None:
                                                    print("Worked on a single sweep file")
                                                elif areas_loops is not None or looped_array_info is not None:
                                                    print("Worked on a multi sweep file")
                                                else:
                                                    print("Something broke")

                                        # device number
                                        print("final list of measured files")
                                        print(list_of_measured_files)
                                        print(list_of_areas)

                                        # After processing all files in the device_number folder
                                # calculation for ech section and the statistics of each
                                #pdf.create_pdf_with_graphs_and_data_for_section()
                                # section name

                        # sample_name
                        # graphs = ["Graph1", "Graph2"]  # List of graph file names

                        # can add this here instead

                        #exc.save_info(sample_name, f.excel_path, sample_path)
                        def get_data_for_pdf():
                            data = [
                                "Summary device.",
                                "Line 2:",
                                "Line 3:"]
                            return data


                        data = get_data_for_pdf()

                        # Show the plot
                        plt.show()
                        #graphs = some_function_comparing_all_files
                        pdf.create_pdf_with_graphs_and_data_for_sample(sample_path,f"{file_info.get('sample_name')}.pdf", graph, info_dict)

                # polymer
# Perform actions in subsequent folders (e.g., g 200µm, D14-Stock-Gold-PVA(2%)-Gold-s7)
# (You can similarly navigate through these folders and perform actions on the processed data)


# Get information
# ex.save_info(file_info.get('sample_name'),excell_path,savelocation)

# Gets all information from a file wether a single sweep or multiple sweeps
# file_info,short_name,long_name,df,area,areas_loops,looped_array_info = eq.file_analysis(filepath,plot_graph,save_df)


# file_info = result['file_info']
# short_name = result['short_name']
# long_name = result['long_name']
# df = result['df']


# if save_df:
#     # save the sada frame
#     print(long_name)
#     df.to_csv(long_name, index=False)
