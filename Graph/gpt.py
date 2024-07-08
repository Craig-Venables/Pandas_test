# gpts changed code

import os
import re
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont, ImageFile
#import memristors.memristors as mem

ImageFile.LOAD_TRUNCATED_IMAGES = True

def plot_iv(voltage, current, fontsize=8):
    # Plot voltage against current
    plt.plot(voltage, current, color='blue')
    plt.ylabel('Current', fontsize=fontsize)
    plt.xlabel('Voltage', fontsize=fontsize)

def plot_logiv(voltage, abs_current, fontsize=8):
    # Plot voltage against absolute current on a logarithmic scale
    plt.plot(voltage, abs_current, color='blue')
    plt.yscale("log")
    plt.ylabel('Abs Current', fontsize=fontsize)
    plt.xlabel('Voltage', fontsize=fontsize)

def plot_current_count(current, fontsize=8):
    # Plot current against its index
    plt.plot(range(len(current)), current, 'r-')
    plt.ylabel('Current', fontsize=fontsize)
    plt.xlabel('Index', fontsize=fontsize)

def plot_iv_avg(voltage, current, num_points=20, fontsize=8):
    # Plot averaged IV curve with arrows indicating direction
    step_size = len(voltage) // num_points
    avg_voltage = [np.mean(voltage[i:i + step_size]) for i in range(0, len(voltage), step_size)]
    avg_current = [np.mean(current[i:i + step_size]) for i in range(0, len(current), step_size)]

    plt.scatter(avg_voltage, avg_current, c='b', marker='o', label='Averaged Data', s=10)
    for i in range(1, len(avg_voltage)):
        plt.annotate('', xy=(avg_voltage[i], avg_current[i]), xytext=(avg_voltage[i - 1], avg_current[i - 1]),
                     arrowprops=dict(arrowstyle='->', color='red'))

    plt.grid(True)

def create_graph(file_info, save_path, voltage, current, abs_current, loop=False, num_sweeps=0):
    # Create and save the graph with given data
    plt.close('all')
    fig = plt.figure(figsize=(12, 8))
    plt.suptitle(f"{file_info['polymer']} - {file_info['sample_name']} - {file_info['section']} - {file_info['device_number']} - {file_info['file_name']}")

    plt.subplot(2, 2, 1)
    plt.title('Iv_Graph')
    plot_iv(voltage, current)

    plt.subplot(2, 2, 2)
    plt.title('Log_Iv')
    plot_logiv(voltage, abs_current)

    plt.subplot(2, 2, 3)
    plt.title('Iv Avg showing direction')
    if loop:
        split_v_data, split_c_data = split_loops(voltage, current, num_sweeps)
        plot_iv_avg(split_v_data[0], split_c_data[0])
    else:
        plot_iv_avg(voltage, current)

    plt.subplot(2, 2, 4)
    plt.title('Current vs Index')
    plot_current_count(current)

    plt.ioff()
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight', dpi=200)
    print(f"File saved successfully at {save_path}")

def main_plot(voltage, current, abs_current, save_loc, re_save, file_info, loop=False, num_sweeps=0):
    # Main function to handle plotting and saving graphs
    short_filename = os.path.splitext(file_info['file_name'])[0]
    save_path = os.path.join(save_loc, f"{short_filename}.png")

    if os.path.exists(save_path) and not re_save:
        # Skip saving if the file exists and re_save is False
        return

    create_graph(file_info, save_path, voltage, current, abs_current, loop, num_sweeps)

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
    plot_iv(voltage, current)

    plt.subplot(2, 1, 2)
    plot_logiv(voltage, abs_current)

    plt.ioff()
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight', dpi=200)
    print(f"File saved successfully at {save_path}")

def main_plot_loop(voltage, current, abs_current, sweep_num, save_loc, re_save, file_info):
    # Plot and save graphs for each loop/sweep
    short_filename = os.path.splitext(file_info['file_name'])[0]
    save_name = f"{short_filename}-#{sweep_num}.png"
    file_path = os.path.join(save_loc, "Extracted sweeps", file_info['file_name'], save_name)
    folder_path = os.path.join(save_loc, "Extracted sweeps", file_info['file_name'])

    if os.path.exists(file_path) and not re_save:
        # Skip saving if the file exists and re_save is False
        return folder_path

    plt.close('all')
    fig = plt.figure(figsize=(12, 8))
    plt.suptitle(f"{file_info['polymer']} - {file_info['sample_name']} - {file_info['section']} - {file_info['device_number']} - {file_info['file_name']}")

    plt.subplot(2, 2, 1)
    plot_iv(voltage, current)

    plt.subplot(2, 2, 2)
    plot_logiv(voltage, abs_current)

    plt.subplot(2, 2, 3)
    plot_iv_avg(voltage, current)

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

def create_gif_from_folder(folder_path, output_gif, fps=2, restart_duration=2):
    # Create a GIF from images in a folder
    try:
        image_files = sorted([os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.png')],
                             key=lambda x: int(re.search(r'\d+', os.path.basename(x)).group()))
        if not image_files:
            print("No image files found in the folder.")
            return

        images = []
        for idx, image_file in enumerate(image_files):
            image = Image.open(image_file).resize((1046, 759))
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("arial.ttf", 40)
            draw.text((30, 30), str(idx + 1), fill="red", font=font)
            images.append(np.array(image))

        # Add a black screen at the end to indicate restart
        black_image = np.zeros_like(images[0])
        images.append(black_image)
        images.extend([black_image] * int(restart_duration * 2))

        imageio.mimsave(output_gif, images, format='GIF', fps=fps)
        print(f"GIF created successfully at {output_gif}")

    except Exception as e:
        print(f"An error occurred: {e}")

def split_loops(v_data, c_data, num_loops):
    # Split the looped data into segments based on the number of loops
    size = len(v_data) // num_loops + (len(v_data) % num_loops != 0)
    return ([v_data[i:i + size] for i in range(0, len(v_data), size)],
            [c_data[i:i + size] for i in range(0, len(c_data), size)])

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
