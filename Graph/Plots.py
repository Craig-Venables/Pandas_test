# gpts changed code

import os
import re
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont, ImageFile
import matplotlib.gridspec as gridspec
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter
import memristors.analysis as mem
#import memristors.memristors as mem
import Graph.Plot_types as Plot_types

ImageFile.LOAD_TRUNCATED_IMAGES = True


def create_graph(file_info, save_path, voltage, current, abs_current,slope, loop=False, num_sweeps=0,):
    # Create and save the graph with given data
    plt.close('all')
    fig = plt.figure(figsize=(12, 8))
    plt.suptitle(f"{file_info['polymer']} - {file_info['sample_name']} - {file_info['section']} - {file_info['device_number']} - {file_info['file_name']}")

    plt.subplot(2, 2, 1)
    plt.title('Iv_Graph')
    Plot_types.plot_iv(voltage, current)

    plt.subplot(2, 2, 2)
    plt.title('Log_Iv')
    Plot_types.plot_logiv(voltage, abs_current)

    plt.subplot(2, 2, 3)
    plt.title('Iv Avg showing direction')
    if loop:
        split_v_data, split_c_data = split_loops(voltage, current, num_sweeps)
        Plot_types.plot_iv_avg(split_v_data[0], split_c_data[0])
    else:
        Plot_types.plot_iv_avg(voltage, current)

    plt.subplot(2, 2, 4)
    plt.title('Current vs Index')
    Plot_types.plot_current_count(current)

    fig.text(0.01, 0.01, 'Gradient between 0-0.1v = ' f"{slope}", ha='left', fontsize=8)

    plt.ioff()
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight', dpi=200)
    print(f"File saved successfully at {save_path}")

def multi_graph(df):
    voltage = df['voltage']
    current = df['current']
    abs_current = df['abs_current']
    current_voltage = df['inverse_resistance_ps']
    voltage_half = df['sqrt_Voltage_ps']
    current_density = df['current_Density_ps']

    # Create a 6x10 grid of subplots
    fig = plt.figure(figsize=(12, 10))
    gs = gridspec.GridSpec(6, 10, figure=fig)

    # Define your other plot functions here if needed

    def plot_4x2_top_right(ax):
        ax.plot(np.random.rand(10))
        ax.set_title('4x2 Top Right')

    # Add plots using the imported functions
    ax1 = fig.add_subplot(gs[0:4, 0:4])
    Plot_types.plot_iv(voltage,current)
    ax1.set_title('Iv')

    ax2 = fig.add_subplot(gs[0:4, 4:8])
    Plot_types.plot_logiv(voltage, abs_current)  # Use imported function
    ax2.set_title('log_iv')

    ax3 = fig.add_subplot(gs[0:4, 8:10])
    plot_4x2_top_right(ax3)
    ax3.set_title('spare')

    ax4 = fig.add_subplot(gs[4:6, 0:2])
    Plot_types.plot_iv_avg(voltage,current,20)
    ax4.set_title('plot_iv_avg')

    ax5 = fig.add_subplot(gs[4:6, 2:4])
    Plot_types.sclc_ps(voltage, current_density)
    ax5.set_title('sclc_ps')

    ax6 = fig.add_subplot(gs[4:6, 4:6])
    Plot_types.poole_frenkel_ps(current_voltage, voltage_half, fontsize=8)
    ax6.set_title('poole-frenkel')

    ax7 = fig.add_subplot(gs[4:6, 6:8])
    Plot_types.schottky_emission_ps(voltage_half, current, fontsize=8)
    ax7.set_title('schottky')

    ax8 = fig.add_subplot(gs[4:6, 8:10])
    Plot_types.plot_current_count(current)
    ax8.set_title('current_count')

    plt.tight_layout()
    plt.show()


# def multi_graph(df):
#
#     # data = {'voltage': v_data,
#     #         'current': c_data,
#     #         'abs_current': eq.absolute_val(c_data),
#     #         'resistance': eq.resistance(v_data, c_data),
#     #         'voltage_ps': v_data_ps,
#     #         'current_ps': c_data_ps,
#     #         'voltage_ng': v_data_ng,
#     #         'current_ng': c_data_ng,
#     #         'log_Resistance': eq.log_value(eq.resistance(v_data, c_data)),
#     #         'abs_Current_ps': eq.absolute_val(c_data_ps),
#     #         'abs_Current_ng': eq.absolute_val(c_data_ng),
#     #         'current_Density_ps': eq.absolute_val(eq.current_density_eq(v_data_ps, c_data_ps)),
#     #         'current_Density_ng': eq.absolute_val(eq.current_density_eq(v_data_ng, c_data_ng)),
#     #         'electric_field_ps': eq.electric_field_eq(v_data_ps),
#     #         'electric_field_ng': eq.absolute_val(eq.electric_field_eq(v_data_ng)),
#     #         'inverse_resistance_ps': eq.inverse_resistance_eq(v_data_ps, c_data_ps),
#     #         'inverse_resistance_ng': eq.absolute_val(eq.inverse_resistance_eq(v_data_ng, c_data_ng)),
#     #         'sqrt_Voltage_ps': eq.sqrt_array(v_data_ps),
#     #         'sqrt_Voltage_ng': eq.absolute_val(eq.sqrt_array(v_data_ng))}
#
#     voltage = df['voltage']
#     current = df['current']
#     abs_current = df['abs_current']
#     current_voltage = df['inverse_resistance_ps']
#     voltage_half = df['sqrt_Voltage_ps']
#
#     # def plot_4x4_top_mid(ax):
#     #     ax.plot(np.random.rand(10))
#     #     ax.set_title('4x4 Top Mid')
#     #
#     def plot_4x4_top_left(ax):
#         ax.plot(np.random.rand(10))
#         ax.set_title('4x4 Top Left')
#
#     def plot_4x4_top_mid(ax):
#         ax.plot(np.random.rand(10))
#         ax.set_title('4x4 Top Mid')
#
#     def plot_4x2_top_right(ax):
#         ax.plot(np.random.rand(10))
#         ax.set_title('4x2 Top Right')
#
#     def plot_2x2_mid_left_left(ax):
#         ax.plot(np.random.rand(10))
#         ax.set_title('2x2 Mid Left Left')
#
#     def plot_2x2_mid_left_mid(ax):
#         ax.plot(np.random.rand(10))
#         ax.set_title('2x2 Mid Left Mid')
#
#     def plot_2x2_mid_mid_left(ax):
#         ax.plot(np.random.rand(10))
#         ax.set_title('2x2 Mid Mid Left')
#
#     def plot_2x2_mid_mid_right(ax):
#         ax.plot(np.random.rand(10))
#         ax.set_title('2x2 Mid Mid Right')
#
#     def plot_2x2_mid_right_right(ax):
#         ax.plot(np.random.rand(10))
#         ax.set_title('2x2 Mid Right Right')
#
#     # Create a 10x10 grid of subplots
#     fig = plt.figure(figsize=(12, 10))
#     gs = gridspec.GridSpec(6, 10, figure=fig)
#
#     # Add a 4x4 subplot at the top left corner
#     ax1 = fig.add_subplot(gs[0:4, 0:4])
#     Plot_types.plot_iv(voltage,current)
#
#     # Add a 4x4 subplot at the top middle
#     ax2 = fig.add_subplot(gs[0:4, 4:8])
#     Plot_types.plot_logiv(voltage,abs_current)
#
#     # Add a 4x2 subplot at the top right
#     ax3 = fig.add_subplot(gs[0:4, 8:10])
#     plot_4x2_top_right(ax3)
#
#     # # Add 2x2 subplots in the middle section
#     # plot_functions = [Plot_types.plot_iv_avg(voltage,current),
#     #                   Plot_types.sclc_ps(voltage,current),
#     #                   Plot_types.poole_frenkel_ps(current_voltage,voltage_half), Plot_types.schottky_emission_ps(voltage_half,current),
#     #                   Plot_types.plot_current_count(current)]
#
#     # Add 2x2 subplots in the middle section
#     plot_functions = [plot_2x2_mid_left_left, plot_2x2_mid_left_mid,
#                       plot_2x2_mid_mid_left, plot_2x2_mid_mid_right,
#                       plot_2x2_mid_right_right]
#
#     for idx, (row, col, title) in enumerate([(4, 0, '2x2 Mid Left Left'),
#                                              (4, 2, '2x2 Mid Left Mid'),
#                                              (4, 4, '2x2 Mid Mid Left'),
#                                              (4, 6, '2x2 Mid Mid Right'),
#                                              (4, 8, '2x2 Mid Right Right')]):
#         ax = fig.add_subplot(gs[row:row+2, col:col+2])
#         plot_functions[idx](ax)
#
#     plt.tight_layout()
#     plt.show()
#
#
# def multi_graph(df):
#
#     voltage = df['voltage']
#     current = df['current']
#     abs_current = df['abs_current']
#     current_voltage = df['inverse_resistance_ps']
#     voltage_half = df['sqrt_Voltage_ps']
#
#     # def plot_4x4_top_mid(ax):
#     #     ax.plot(np.random.rand(10))
#     #     ax.set_title('4x4 Top Mid')
#     #
#     def plot_4x2_top_right(ax):
#         ax.plot(np.random.rand(10))
#         ax.set_title('4x2 Top Right')
#
#
#     # Create a 10x10 grid of subplots
#     fig = plt.figure(figsize=(12, 10))
#     gs = gridspec.GridSpec(6, 10, figure=fig)
#
#     # Add a 4x4 subplot at the top left corner
#     ax1 = fig.add_subplot(gs[0:4, 0:4])
#     Plot_types.plot_iv(voltage,current)
#
#     # Add a 4x4 subplot at the top middle
#     ax2 = fig.add_subplot(gs[0:4, 4:8])
#     Plot_types.plot_logiv(voltage,abs_current)
#
#     # Add a 4x2 subplot at the top right
#     ax3 = fig.add_subplot(gs[0:4, 8:10])
#     plot_4x2_top_right(ax3)
#
#     # Add 2x2 subplots in the middle section
#     plot_functions = [Plot_types.plot_iv_avg(voltage,current),
#                       Plot_types.sclc_ps(voltage,current),
#                       Plot_types.poole_frenkel_ps(current_voltage,voltage_half), Plot_types.schottky_emission_ps(voltage_half,current),
#                       Plot_types.plot_current_count(current)]
#
#     for idx, (row, col, title) in enumerate([(4, 0, '2x2 Mid Left Left'),
#                                              (4, 2, '2x2 Mid Left Mid'),
#                                              (4, 4, '2x2 Mid Mid Left'),
#                                              (4, 6, '2x2 Mid Mid Right'),
#                                              (4, 8, '2x2 Mid Right Right')]):
#         ax = fig.add_subplot(gs[row:row+2, col:col+2])
#         plot_functions[idx](ax)
#
#     plt.tight_layout()
#     plt.show()



def main_plot(voltage, current, abs_current, save_loc, re_save, file_info,slope,loop=False, num_sweeps=0):
    # Main function to handle Plots and saving graphs
    short_filename = os.path.splitext(file_info['file_name'])[0]
    save_path = os.path.join(save_loc, f"{short_filename}.png")

    if os.path.exists(save_path) and not re_save:
        # Skip saving if the file exists and re_save is False
        return

    create_graph(file_info, save_path, voltage, current, abs_current, slope, loop, num_sweeps,)

def iv_and_log_iv_plot(voltage, current, abs_current, file_info, save_loc="", re_save=False):
    # Plot and save IV and log IV graphs
    short_filename = os.path.splitext(file_info['file_name'])[0]
    save_path = os.path.join(save_loc, f"{short_filename}.png")

    if os.path.exists(save_path) and not re_save:
        # Skip saving if the file exists and re_save is False
        return

    plt.close('all')
    fig = plt.figure(figsize=(12, 8))
    plt.suptitle(f"{file_info['polymer']} - {file_info['sample_name']} - {file_info['section']} - {file_info['device_number']} - {file_info['file_name']}")

    plt.subplot(2, 1, 1)
    Plot_types.plot_iv(voltage, current)

    plt.subplot(2, 1, 2)
    Plot_types.plot_logiv(voltage, abs_current)

    plt.ioff()
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight', dpi=200)
    print(f"File saved successfully at {save_path}")

def main_plot_loop(voltage, current, abs_current, sweep_num, save_loc, re_save, file_info,slope):
    """plots main graph for loops"""
    # Plot and save graphs for each loop/sweep
    short_filename = os.path.splitext(file_info['file_name'])[0]
    save_name = f"{short_filename}- #{sweep_num}.png"
    file_path = os.path.join(save_loc, "Extracted sweeps", file_info['file_name'], save_name)
    folder_path = os.path.join(save_loc, "Extracted sweeps", file_info['file_name'])

    if os.path.exists(file_path) and not re_save:
        # Skip saving if the file exists and re_save is False
        return folder_path

    plt.close('all')
    fig = plt.figure(figsize=(12, 8))
    plt.suptitle(f"{file_info['polymer']} - {file_info['sample_name']} - {file_info['section']} - {file_info['device_number']} - {file_info['file_name']}")

    plt.subplot(2, 2, 1)
    Plot_types.plot_iv(voltage, current)

    plt.subplot(2, 2, 2)
    Plot_types.plot_logiv(voltage, abs_current)

    plt.subplot(2, 2, 3)
    Plot_types.plot_iv_avg(voltage, current)

    plt.ioff()
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    plt.savefig(file_path, bbox_inches='tight', dpi=200)
    print(f"File saved successfully at {file_path}")

    return folder_path

def plot_images_in_folder(folder_path, save_loc):
    # Plot all images in a folder and save as a single image
    files = os.listdir(folder_path)
    images = [file for file in files if file.endswith(('.png', '.jpg'))]

    num_images = len(images)
    fig, axs = plt.subplots(1, num_images, figsize=(15, 5))

    for i, image_file in enumerate(images):
        image_path = os.path.join(folder_path, image_file)
        image = Image.open(image_path)
        axs[i].imshow(image)
        axs[i].axis('off')
        axs[i].text(0.05, 0.95, str(i + 1), color='red', fontsize=12, ha='left', va='top', transform=axs[i].transAxes)

    plt.subplots_adjust(wspace=0.02)
    plt.savefig(save_loc, dpi=200)
    print(f"File saved successfully at {save_loc}")



def split_loops(v_data, c_data, num_loops):
    """ splits the looped data and outputs each sweep as another array coppied from data"""
    total_length = len(v_data)  # Assuming both v_data and c_data have the same length
    size = total_length // num_loops  # Calculate the size based on the number of loops

    # Convert size to integer
    size = int(size)

    # Handle the case when the division leaves a remainder
    if total_length % num_loops != 0:
        size += 1

    split_v_data = [v_data[i:i + size] for i in range(0, total_length, size)]
    split_c_data = [c_data[i:i + size] for i in range(0, total_length, size)]

    return split_v_data, split_c_data


def plot_histograms(on_values, off_values):
    # Plot histograms for on and off values
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    plt.hist(on_values, bins=20, color='blue', alpha=0.7, label='On Values')
    plt.xlabel('Resistance On Value')
    plt.ylabel('Frequency')
    plt.title('Histogram of On Values')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.hist(off_values, bins=20, color='red', alpha=0.7, label='Off Values')
    plt.xlabel('Resistance Off Value')
    plt.ylabel('Frequency')
    plt.title('Histogram of Off Values')
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_index_vs_values(on_values, off_values):
    # Plot index vs resistance values
    plt.figure(figsize=(10, 6))
    indices = range(len(on_values))
    plt.plot(indices, on_values, 'bo-', label='On Values')
    plt.plot(indices, off_values, 'ro-', label='Off Values')
    plt.xlabel('Index')
    plt.ylabel('Resistance Value')
    plt.yscale("log")
    plt.title('Index vs Resistance Values')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_filenames_vs_values(filenames, on_values, off_values):
    # Plot filenames vs resistance values
    plt.figure(figsize=(14, 6))
    x = range(len(filenames))
    plt.plot(x, on_values, 'bo-', label='On Values')
    plt.plot(x, off_values, 'ro-', label='Off Values')
    plt.xticks(x, filenames, rotation=90)
    plt.xlabel('Filename')
    plt.ylabel('Resistance Value')
    plt.yscale("log")
    plt.title('Filename vs Resistance Values')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def grid_spec(df,save_loc,file_info):

    short_filename = os.path.splitext(file_info['file_name'])[0]
    save_path = os.path.join(save_loc, f"{short_filename}.png")
    def format_tick(value, pos):
        # Format tick label as 10^x
        return f'$10^{{{int(value)}}}$'

    voltage = df['voltage']
    current = df['current']
    voltage_ng = df['voltage_ng']
    abs_current = df['abs_current']
    current_voltage = df['inverse_resistance_ps']
    current_voltage_ng = df['inverse_resistance_ng']
    voltage_half = df['sqrt_Voltage_ps']
    voltage_half_ng = df['sqrt_Voltage_ng']
    current_density = df['current_Density_ps']
    current_density_ng = df['current_Density_ng']
    resistance = df['resistance']


    fontsize = 5
    gs = gridspec.GridSpec(4, 5, wspace=0.3, hspace=0.3)

    ax1 = plt.subplot(gs[0:2, 0:2])  # Rows 0 and 1 Columns 0 and 1 iv
    ax1.text(0.05, 0.95, 'Iv ', transform=ax1.transAxes, fontsize=8, va='top', ha='left', color="red")
    Plot_types.plot_iv(voltage,current, fontsize)

    ax2 = plt.subplot(gs[0:2, 2:4])  # logiv
    ax2.text(0.05, 0.95, 'Iv_log ', transform=ax2.transAxes, fontsize=8, va='top', ha='left', color="red")
    Plot_types.plot_logiv(voltage, abs_current, fontsize)

    ax3 = plt.subplot(gs[2, 0])  # sclc
    ax3.text(0.05, 0.95, 'sclc ', transform=ax3.transAxes, fontsize=8, va='top', ha='left', color="red")
    Plot_types.sclc_ps(voltage, current_density, fontsize)

    ax4 = plt.subplot(gs[2, 1])  # sclc -ve
    ax4.text(0.05, 0.95, 'sclc -ve', transform=ax4.transAxes, fontsize=8, va='top', ha='left', color="red")
    Plot_types.sclc_ng(voltage_ng, current_density_ng, fontsize)

    ax5 = plt.subplot(gs[2, 2])  # scxotty
    ax5.text(0.05, 0.95, 'schottky', transform=ax5.transAxes, fontsize=8, va='top', ha='left', color="red")
    Plot_types.schottky_emission_ps(voltage_half, current, fontsize)

    ax6 = plt.subplot(gs[2, 3])  # scotty
    ax6.text(0.05, 0.95, 'shottky -ve', transform=ax6.transAxes, fontsize=8, va='top', ha='left', color="red")
    Plot_types.schottky_emission_ng(voltage_half_ng, current, fontsize)

    ax7 = plt.subplot(gs[0, 4])  # pf +ve
    ax7.text(0.05, 0.95, 'pf +ve', transform=ax7.transAxes, fontsize=8, va='top', ha='left', color="red")
    Plot_types.poole_frenkel_ps(current_voltage, voltage_half, fontsize)

    ax8 = plt.subplot(gs[1, 4])  # pf-ve
    ax8.text(0.05, 0.95, 'Poole-frenkel -ve', transform=ax8.transAxes, fontsize=8, va='top', ha='left', color="red")
    Plot_types.poole_frenkel_ng(current_voltage_ng, voltage_half_ng, fontsize)

    ax9 = plt.subplot(gs[3, 0:2])  # resis coubt
    ax9.text(0.05, 0.95, 'resistance time', transform=ax9.transAxes, fontsize=8, va='top', ha='left', color="red")
    Plot_types.resistance_time(resistance)

    ax10 = plt.subplot(gs[3, 2:4])  # volt count
    ax10.text(0.05, 0.95, 'voltage count', transform=ax10.transAxes, fontsize=8, va='top', ha='left', color="red")
    Plot_types.plot_current_count(current,fontsize)
    ax11 = plt.subplot(gs[3, 4])  # direction
    ax11.text(0.05, 0.95, 'direction', transform=ax11.transAxes, fontsize=8, va='top', ha='left', color="red")
    Plot_types.plot_iv_avg(voltage,current, 20, fontsize)

    ax12 = plt.subplot(gs[2, 4])  # information
    ax12.text(0.05, 0.95, 'info', transform=ax12.transAxes, fontsize=8, va='top', ha='left', color="red")

    # Adjusting tick label font size
    for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12]:
        ax.tick_params(axis='both', which='both', labelsize=6)  # Adjust labelsize as needed

    for ax in [ax3, ax4, ax5, ax6, ax7, ax8]:
        ax.xaxis.set_major_formatter(FuncFormatter(format_tick))
        ax.yaxis.set_major_formatter(FuncFormatter(format_tick))

        # ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        # ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

    # Adjust layout to prevent overlap
    # plt.tight_layout()

    # Show plot
    #plt.show()

    plt.ioff()
    plt.tight_layout()
    plt.savefig(save_path,  dpi=300)
    print(f"File saved successfully at {save_path}")