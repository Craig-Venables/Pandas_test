import pandas as pd
import statistics
import numpy
import os
import Data as eq
import pdf as pdf
import matplotlib.pyplot as plt
import excell as exc
import file as f
import pickle
import pprint
import math
import sys
import print_info as p
from file import Tee
import shutil
import excell as ex
from file import excel_path
import plotting
import Origin as origin
import re
import copy_graph_class as cg
import os
import pickle

class DataProcessor:
    def __init__(self, main_dir, excel_path):
        self.main_dir = main_dir
        self.excel_path = excel_path
        self.total_samples = self._count_total_samples()
        self.total_files = self._count_total_files()
        self.processed_samples = 0
        self.processed_files = 0
        self.material_stats_dict = {}
        self.material_sweeps_dict = {}
        self.material_data = {}

    def _count_total_samples(self):
        return sum(1 for _ in os.listdir(self.main_dir) if os.path.isdir(os.path.join(self.main_dir, _)))

    def _count_total_files(self):
        return sum(len(files) for _, _, files in os.walk(self.main_dir))

    def process_data(self):
        for material in os.listdir(self.main_dir):
            material_path = os.path.join(self.main_dir, material)
            if os.path.isdir(material_path):
                polymer_stats_dict = {}
                polymer_sweeps_dict = {}
                polymer_data = {}

                for polymer in os.listdir(material_path):
                    polymer_path = os.path.join(material_path, polymer)
                    if os.path.isdir(polymer_path):
                        for sample_name in os.listdir(polymer_path):
                            sample_path = os.path.join(polymer_path, sample_name)
                            if os.path.isdir(sample_path):
                                self.processed_samples += 1
                                percentage_completed_samples = (self.processed_samples / self.total_samples) * 100

                                if pull_fabrication_info_excell:
                                    fabrication_info_dict = exc.save_info_from_solution_devices_excell(sample_name,
                                                                                                       self.excel_path,
                                                                                                       sample_path)
                                sample_sweep_excell_dict = exc.save_info_from_device_info_excell(sample_name,
                                                                                                  sample_path)

                                for section_folder in os.listdir(sample_path):
                                    section_path = os.path.join(sample_path, section_folder)
                                    if os.path.isdir(section_path):
                                        self.processed_files += 1
                                        percentage_completed_files = (self.processed_files / self.total_files) * 100

                                        # Process the files and update dictionaries here

                                        print("--------------------------------")
                                        print(f'Current percentage of files completed: {percentage_completed_files:.2f}%')
                                        print("--------------------------------")

                                print("################################")
                                print(f'Finished processing sample: {sample_name}')
                                print(f'Total percentage of samples completed: {percentage_completed_samples:.2f}%')
                                print("################################")

                                # Store sample data in dictionaries here

                self.material_stats_dict[material] = polymer_stats_dict
                self.material_sweeps_dict[material] = polymer_sweeps_dict
                self.material_data[material] = polymer_data

    def save_results(self):
        with open(os.path.join(self.main_dir, 'material_stats_dict_all.pkl'), 'wb') as file:
            pickle.dump(self.material_stats_dict, file)

        with open(os.path.join(self.main_dir, 'material_sweeps_dict_all.pkl'), 'wb') as file:
            pickle.dump(self.material_sweeps_dict, file)

        with open(os.path.join(self.main_dir, 'material_data_all.pkl'), 'wb') as file:
            pickle.dump(self.material_data, file)