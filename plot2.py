import matplotlib.pyplot as plt
import numpy as np
import file as f
import scipy as sp
import pathlib as pl
import os



class plot2():
    '''
    Class for plotting graphs
    '''

    def __init__(self, data,file_info,save_loc,filepath) -> None:
        self.data = data
        self.file_info = file_info
        self._unpack_dataframe_data()
        self._unpack_dataframe_file_info()


        # gets file info
        # self.type = file_info.get('type')
        # self.polymer = file_info.get('polymer')
        # self.sample_name = file_info.get('sample_name')
        # self.section = file_info.get('section')
        # self.device_number = file_info.get('device_number')
        # self.filename = file_info.get('file_name')
        self.save_loc = save_loc
        self.short_filename = os.path.splitext(self.filename)[0]

        file_info = f.extract_folder_names(filepath)
        short_name = f.short_name(filepath)
        long_name = f.long_name(filepath)

        # looped data
        self.looped_info = False
        self.normalized_areas = ""
        self.ps_areas = ""
        self.ng_areas = ""

        self.fig = None
        print(self.section)

    def _unpack_dataframe_data(self):
        """ Unpacks dataframe with the names given """
        for column in self.data.columns:
            setattr(self, column.lower(), self.data.get(column))

    def _unpack_dataframe_file_info(self):
        """ Unpacks dataframe with the names given """
        for column in self.file_info.columns:
            setattr(self, column.lower(), self.file_info.get(column))
