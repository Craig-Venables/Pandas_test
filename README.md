pip install reportlab matplotlib
Read me provided by tabine 

### Important

Make sure that all files are text files you can easily do this using power rename and
NOT *.txt within the search bar to find all the files in the directory that arnt texts and then rename them
using power rename, add the last letter into the top search bar and the extension .txt in the one below
then set to extension only.

### File structure matters, it needs to go:

_**['top folder]['defining feature 1'][[f'{defining feature 2}'][f'{sample_name}'][['section']['device_number']['sweep_file]]**_

_ie ['Data]['Quantum Dots'][[f'{Ws2}'][f'{D12-0.2mg/ml...}'][['G']['1']['1-fs-1v.txt]]_

# Code Overview
This code is a script that was created to assist in analyzing the data collected from measuring the capacitance of various materials and devices. The code is designed to be modular, allowing for easy modification and expansion. The main functions of the code are as follows:

1. Import necessary libraries: The code imports a number of libraries, including Pandas, NumPy, Matplotlib, and others, that are used for data analysis and visualization.

2. Define classes and functions: The code defines several classes and functions that are used for various tasks, such as redirecting print output, analyzing data from files, and creating PDFs.

3. Create a main loop: The code creates a main loop that iterates through folders containing data, such as materials, polymers, and samples. This allows the code to process data for multiple materials and samples simultaneously.

4. Navigate through subfolders: The code navigates through subfolders within each folder, such as polymers within a material folder and devices within a sample folder. This allows the code to process data for multiple devices within a sample.

5. Process data for each file: The code processes data for each file in a device folder, including calculating capacitance and other properties, and saving the results in a DataFrame.

6. Calculate statistics for each device and section: The code calculates statistics for each device and section, including the mean and median ON-OFF ratio and the maximum capacitance.

7. Create PDFs with graphs and data: The code creates PDFs with graphs and data for each sample, including the graphs and data for each device and section.

8. Save data for later use: The code saves data for later use, including the data for each sample, the statistics for each device and section, and the PDFs with graphs and data.

# How to Use the Code
The code is designed to be easy to use and modify. To use the code, you can simply run the main function in the script and follow the prompts. The code is designed to be modular, so you can easily modify or expand the code as needed.

# Limitations and Future Improvements
One limitation of the code is that it is currently designed to work with a specific file structure and format for the data. However, this can be easily modified by modifying the code to work with a different file structure.

In the future, there are a number of improvements that could be made to the code, including:

1. Adding support for additional file formats: The code currently supports only text files, but it could be expanded to support other file formats, such as Excel files.

2. Adding support for additional analysis methods: The code currently uses a simple analysis method for calculating capacitance, but it could be expanded to support additional analysis methods, such as Fourier analysis.

3. Adding support for additional properties: The code currently calculates only the ON-OFF ratio and normalized area, but it could be expanded to calculate additional properties, such as the capacitance density or dielectric constant.

4. Adding support for additional output formats: The code currently creates PDFs with graphs and data, but it could be expanded to create other output formats, such as HTML or LaTeX files.

5. Adding support for additional file structures: The code currently assumes a specific file structure, but it could be expanded to work with different file structures.

Overall, the code is a useful tool for analyzing capacitance data and could be easily modified and expanded to meet the needs of a variety of applications.