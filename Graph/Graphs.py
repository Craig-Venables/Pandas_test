import matplotlib.pyplot as plt
import numpy as np

# temp file fopr graph sorting

def create_graph():
    plt.close('all')
    fig = plt.figure(figsize=(12, 8))

    plt.suptitle(
        f'{polymer} -' + f'{sample_name} -' + ' ' + f'{section} -' + ' '
        + f'{device_number} -' + ' ' + filename)

    # using the functions main_plot the graphs
    plt.subplot(2, 2, 1) # plot graph 1
    plt.title('Iv_Graph')
    plot_iv(voltage, current)

    plt.subplot(2, 2, 2) # plot graph 2
    plt.title('Log_Iv')
    plot_logiv(voltage, abs_current)

    plt.subplot(2, 2, 3) # plot graph 3
    plt.title('Iv Avg showing direction')
    if loop:
        # This dosnt save correctly it shows the correct image, but dosnt save
        split_v_data, split_c_data = split_loops(voltage, current, num_sweeps)
        plot_iv_avg(split_v_data[0], split_c_data[0])
    else:
        plot_iv_avg(voltage, current)

    # Create subplot for the final plot with two graphs
    plt.subplot(2, 2, 4) # plot graph 4
    plt.title('Current vs Index')
    plot_current_count(current)
    # plot_iv_subplots(voltage, current)
    # text = (crossing_points)
    # plt.text(0.5, 0.5, text, ha='center', va='center', fontsize=12)
    # plt.show()

    # Turn off interactive mode
    plt.ioff()
    file_path = os.path.join(save_loc, f"{short_filename}.png")
    plt.tight_layout()
    plt.savefig(file_path, bbox_inches='tight', dpi=200)
    # plt.show()
    print(f"File saved successfully at {file_path}")



def main_plot(voltage, current, abs_current, save_loc, re_save, file_info, loop=False, num_sweeps=0):
    '''
        plots iv and log iv graphs as subplots and saves it
    '''

    type = file_info.get('type')
    polymer = file_info.get('polymer')
    sample_name = file_info.get('sample_name')
    section = file_info.get('section')
    device_number = file_info.get('device_number')
    filename = file_info.get('file_name')
    save_loc = save_loc
    short_filename = os.path.splitext(filename)[0]

    file_path = os.path.join(save_loc, f"{short_filename}.png")

    if os.path.exists(file_path):
        # File exists
        if re_save:
            create_graph()
            # Plot the graph
            # Re-save is True, so create the file (overwriting if it exists)
        if not re_save:
            # Re-save is False wit file exists, skip plot
            pass
    # Save the graph
    else:
        # File doesn't exist
        create_graph()