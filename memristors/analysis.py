import numpy as np
import file as f
import math
import os
import excell as exc
import re
import logging
#import Plots
import matplotlib
# Force non-interactive backend before any pyplot is imported by other modules
matplotlib.use("Agg")
import Graph.Plots as Plots
import pandas as pd
import pickle
import memristors.Files_ as Files_
import memristors.equations as eq
import Graph.Gifs as Gifs
import matplotlib.pyplot as plt
from typing import Tuple, List, Dict, Any
from concurrent.futures import ProcessPoolExecutor, as_completed

logger = logging.getLogger("mem_analysis")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logger.addHandler(_handler)


debugging = False

''' all on mesmerisers here
 '''

def memristors_currated(loc):
    print(loc)
    # using the repo suggested by mike smith


def _process_file_worker(args: tuple) -> Any:
    """Worker for parallel per-file processing.
    Returns None if file should be skipped, else a tuple:
    (file_name, short_name, long_name, num_sweeps, df_file_stats, df)
    """
    (
        file_name,
        file_path,
        device_path,
        plot_graph,
        save_df,
        re_save_graph,
        short_name,
        long_name,
        skip_half_sweeps,
        save_parquet,
    ) = args

    result = file_analysis(
        filepath=file_path,
        plot_graph=plot_graph,
        save_df=save_df,
        device_path=device_path,
        re_save_graph=re_save_graph,
        short_name=short_name,
        long_name=long_name,
        skip_half_sweeps=skip_half_sweeps,
        save_parquet=save_parquet,
    )
    if result is None:
        return None
    num_sweeps, short_name, long_name, df, df_file_stats, _graph = result
    return (file_name, short_name, long_name, num_sweeps, df_file_stats, df)


def memristor_devices(path, params, excel_path):
    """ Takes the path sorts the data and returns file info

    :param path: Path to the folder containing all the data
    :returns:
    Material_stats_dict = All the statistics for all devices
    Material_sweeps_dict = Contains all the sweeps per device along with the classification
    Material_data = Contains all the data extracted from the sweep (Voltage,current,abs_current etc....)

    """
    logger.info("Starting Memristors analysis")

    # empty dictionary's for later use
    material_stats_dict = {}
    material_sweeps_dict = {}
    material_data = {}
    file_info_dict = {}

    plot_graph = params['plot_graph']
    plot_gif = params['plot_gif']
    sort_graphs = params['sort_graphs']
    origin_graphs = params['origin_graphs']
    pull_fabrication_info_excell = params['pull_fabrication_info_excell']
    save_df = params['save_df']
    re_save_graph = params['re_save_graph']
    re_analyse = params['re_analyse']


    # Pre-compute totals once for progress tracking
    total_samples = sum(1 for e in os.scandir(path) if e.is_dir())
    total_files = sum(len(files) for _, _, files in os.walk(path))
    processed_samples = 0
    processed_files = 0

    # Load processed cache once
    checked_cache_path = os.path.join('memristors', 'checked_files.pkl')
    try:
        with open(checked_cache_path, 'rb') as _cf:
            checked_cache = pickle.load(_cf)
    except Exception:
        checked_cache = {}

    for material_entry in os.scandir(path):
        if not material_entry.is_dir():
            continue
        material = material_entry.name
        material_path = material_entry.path

        # Navigate through polymers
        polymer_stats_dict = {}
        polymer_sweeps_dict = {}
        polymer_data = {}

        for polymer_entry in os.scandir(material_path):
            if not polymer_entry.is_dir():
                continue
            polymer = polymer_entry.name
            polymer_path = polymer_entry.path

            # Navigate through samples
            sample_stats_dict = {}
            sample_sweeps_dict = {}
            sample_data = {}

            for sample_entry in os.scandir(polymer_path):
                if not sample_entry.is_dir():
                    continue
                sample_name = sample_entry.name
                sample_path = sample_entry.path

                processed_samples += 1
                percentage_completed = (processed_samples / total_samples) * 100

                if pull_fabrication_info_excell:
                    fabrication_info_dict = exc.save_info_from_solution_devices_excell(sample_name, excel_path, sample_path)
                sample_sweep_excell_dict = exc.save_info_from_device_info_excell(sample_name, sample_path)

                section_stats_dict = {}
                section_sweeps_dict = {}
                section_data = {}

                # Sections
                for section_entry in os.scandir(sample_path):
                    if not section_entry.is_dir():
                        continue
                    section_folder = section_entry.name
                    section_path = section_entry.path

                    device_sweeps_dict = {}
                    device_stats_dict = {}
                    device_data = {}

                    numeric_pattern = re.compile(r'\d+')
                    def extract_numeric_part(name: str) -> int:
                        m = numeric_pattern.search(name)
                        return int(m.group()) if m else 0

                    sorted_devices = sorted([e.name for e in os.scandir(section_path) if e.is_dir()], key=extract_numeric_part)
                    for device_folder in sorted_devices:
                        if device_folder == 'plots_combined':
                            continue
                        device_path = os.path.join(section_path, device_folder)

                        list_of_file_stats: List[pd.DataFrame] = []
                        file_data: Dict[str, pd.DataFrame] = {}
                        num_of_sweeps = 0

                        classification = Files_.device_clasification(sample_sweep_excell_dict, device_folder, section_folder, device_path)

                        # Build tasks
                        tasks = []
                        for f_entry in os.scandir(device_path):
                            if not f_entry.is_file():
                                continue
                            file_name = f_entry.name
                            file_path = f_entry.path
                            file_key = f'{material}_{polymer}_{sample_name}_{section_folder}_{device_folder}_{file_name}'
                            file_info_dict[file_key] = {
                                'material': material,
                                'polymer': polymer,
                                'sample_name': sample_name,
                                'section_folder': section_folder,
                                'device_folder': device_folder,
                                'file_name': file_name,
                                'file_path': file_path,
                            }
                            if not file_name.endswith('.txt'):
                                continue
                            short_name = f.short_name(file_path)
                            long_name = f.long_name(file_path)
                            cache_key = long_name
                            if (not re_analyse) and (checked_cache.get(cache_key) == 'done'):
                                continue

                            tasks.append((
                                file_name,
                                file_path,
                                device_path,
                                plot_graph,
                                save_df,
                                re_save_graph,
                                short_name,
                                long_name,
                                params.get('skip_half_sweeps', False),
                                params.get('save_parquet', False),
                            ))

                        # Execute tasks
                        results = []
                        workers = max(1, int(params.get('parallel_workers', 1)))
                        if workers > 1 and tasks:
                            with ProcessPoolExecutor(max_workers=workers) as ex:
                                fut_map = {ex.submit(_process_file_worker, t): t for t in tasks}
                                for fut in as_completed(fut_map):
                                    try:
                                        res = fut.result()
                                        if res is not None:
                                            results.append(res)
                                    except Exception as e:
                                        logger.warning("Worker failed for %s: %s", fut_map[fut][0], e)
                        else:
                            for t in tasks:
                                try:
                                    res = _process_file_worker(t)
                                    if res is not None:
                                        results.append(res)
                                except Exception as e:
                                    logger.warning("Sequential processing failed for %s: %s", t[0], e)

                        # Merge results
                        for file_name, short_name, long_name, num_sweeps, df_file_stats, df in results:
                            num_of_sweeps += num_sweeps
                            list_of_file_stats.append(df_file_stats)
                            file_data[file_name] = df
                            checked_cache[long_name] = 'done'

                        # Device-level outputs
                        save_name = "_Device" + f"{device_folder}" + ".gif"
                        save_name_slow = "_Device_slow" + f"{device_folder}" + ".gif"
                        folder_path = device_path + '\\' + "python_images"
                        output_gif_loc = os.path.join(folder_path, save_name)
                        output_gif_loc2 = os.path.join(folder_path, save_name_slow)

                        if plot_gif:
                            if does_it_exist(output_gif_loc, re_save_graph):
                                Gifs.create_gif_from_folder(folder_path, output_gif_loc, 2, restart_duration=10)
                            if does_it_exist(output_gif_loc2, re_save_graph):
                                Gifs.create_gif_from_folder(folder_path, output_gif_loc2, 1, restart_duration=10)

                        if len(list_of_file_stats) >= 2:
                            device_stats_dict[f'{device_folder}'] = pd.concat(list_of_file_stats, ignore_index=True)

                        device_data[f'{device_folder}'] = file_data
                        device_sweeps_dict[f'{device_folder}'] = {'num_of_sweeps': num_of_sweeps, 'classification': classification}

                        if origin_graphs:
                            try:
                                from Graph.Origin import Origin as OriginMod
                                OriginMod.plot_in_origin(device_data, device_path, 'transport')
                                OriginMod.plot_in_origin(device_data, device_path, 'iv_log')
                            except Exception as e:
                                logger.warning("Failed to plot in Origin: %s", e)

                    # Section-level
                    section_stats_dict[f'{section_folder}'] = device_stats_dict
                    section_sweeps_dict[f'{section_folder}'] = device_sweeps_dict
                    section_data[f'{section_folder}'] = device_data

                # Sample-level
                sample_stats_dict[f'{sample_name}'] = section_stats_dict
                sample_sweeps_dict[f'{sample_name}'] = section_sweeps_dict
                sample_data[f'{sample_name}'] = section_data

                print("")
                print("################################")
                print("Finished processing - ", sample_name)
                print("################################")

                # Persist stats in sample folder
                with open(sample_path + '/' + sample_name + '_Stats', 'wb') as file:
                    pickle.dump(sample_stats_dict, file)
                with open(sample_path + '/' + sample_name + '_data', 'wb') as file:
                    pickle.dump(sample_data, file)
                save_df_off_stats(sample_path, sample_stats_dict, sample_sweeps_dict)

            # Polymer-level
            polymer_stats_dict[f'{polymer}'] = sample_stats_dict
            polymer_sweeps_dict[f'{polymer}'] = sample_sweeps_dict
            polymer_data[f'{polymer}'] = sample_data

        # Material-level
        material_stats_dict[f'{material}'] = polymer_stats_dict
        material_sweeps_dict[f'{material}'] = polymer_sweeps_dict
        material_data[f'{material}'] = polymer_data

    # save all the information to pkl file
    with open(path + '/material_stats_dict_all.pkl', 'wb') as file:
        pickle.dump(material_stats_dict, file)

    with open(path + '/material_sweeps_dict_all.pkl', 'wb') as file:
        pickle.dump(material_sweeps_dict, file)

    with open(path + '/material_data_all.pkl', 'wb') as file:
        pickle.dump(material_data, file)

    with open(path + '/file_info_dict.pkl', 'wb') as file:
        pickle.dump(file_info_dict, file)



    # Persist the processed cache
    try:
        with open(os.path.join('memristors', 'checked_files.pkl'), 'wb') as _cfw:
            pickle.dump(checked_cache, _cfw)
    except Exception as e:
        logger.warning("Failed to save processed cache: %s", e)

    logger.info("Completed analysis of %d materials", len(material_sweeps_dict))
    return material_stats_dict, material_sweeps_dict,material_data,file_info_dict


def file_analysis(filepath, plot_graph, save_df, device_path, re_save_graph, short_name, long_name,
                  skip_half_sweeps: bool = False, save_parquet: bool = False):
    """ For all info from a single file this determines if a file is a single sweep or multiple sweep and does
     the appropriate action  """
    #print(filepath)
    file_info = f.extract_folder_names(filepath)

    # Read the information from the file
    try:
        # Pull voltage and current data from file
        v_data, c_data,time = split_iv_sweep(filepath)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("probably due too the file not being what it expects please check")

    # print(filepath)
    # print(v_data,c_data,time)
    # get positive and negative values of voltage and current data for equations later
    v_data_ps, c_data_ps = eq.filter_positive_values(v_data, c_data)
    v_data_ng, c_data_ng = eq.filter_negative_values(v_data, c_data)
    # checks for looped data and calculates the number of loops
    num_sweeps = check_for_loops(v_data)

    # create a dataframe for the device of all the data
    data = {'voltage': v_data,
            'current': c_data,
            'abs_current': eq.absolute_val(c_data),
            'resistance': eq.resistance(v_data, c_data),
            'voltage_ps': v_data_ps,
            'current_ps': c_data_ps,
            'voltage_ng': v_data_ng,
            'current_ng': c_data_ng,
            'log_Resistance': eq.log_value(eq.resistance(v_data, c_data)),
            'abs_Current_ps': eq.absolute_val(c_data_ps),
            'abs_Current_ng': eq.absolute_val(c_data_ng),
            'current_Density_ps': eq.absolute_val(eq.current_density_eq(v_data_ps, c_data_ps)),
            'current_Density_ng': eq.absolute_val(eq.current_density_eq(v_data_ng, c_data_ng)),
            'electric_field_ps': eq.electric_field_eq(v_data_ps),
            'electric_field_ng': eq.absolute_val(eq.electric_field_eq(v_data_ng)),
            'inverse_resistance_ps': eq.inverse_resistance_eq(v_data_ps, c_data_ps),
            'inverse_resistance_ng': eq.absolute_val(eq.inverse_resistance_eq(v_data_ng, c_data_ng)),
            'sqrt_Voltage_ps': eq.sqrt_array(v_data_ps),
            'sqrt_Voltage_ng': eq.absolute_val(eq.sqrt_array(v_data_ng)),

            }

    df = pd.DataFrame(data)
    df = df.dropna()

    # Plots.multi_graph(df)
    # Plots.grid_spec(df,file_info)

    # get the gradient of the line from x=0 - x=val for initial resistance if needed through 0 use below
    # df_sections = split_data_in_sect(df['voltage'], df["current"],0.1,-0.1)
    #slope = gradient(df['voltage'], df["current"],filepath)
    try:
        slope = gradient(df['voltage'], df["current"], filepath)
    except:
        #print("error in for slope calculation for ",filepath)
        slope = "no data"

    # if there is more than one loop adds
    if num_sweeps == 0.5:
        if skip_half_sweeps:
            return None
        # else fall-through continue as single-sweep like legacy behaviour
    if num_sweeps > 1:
        loops = True
        # Data processing for multiple sweeps

        # splits the loops depending on the number of sweeps
        split_v_data, split_c_data = split_loops(df['voltage'], df["current"], num_sweeps)
        # Calculates the metrics for each array returning the areas
        #todo this needs checking its correct
        ps_areas, ng_areas, areas, normalized_areas, ron, roff, von, voff = calculate_metrics_for_loops(split_v_data,
                                                                                                        split_c_data)

        # create dataframe for a device of all the data
        areas_loops = {'ps_area': [ps_areas],
                       'ng_area': [ng_areas],
                       'areas': [areas],
                       'normalised_areas': [normalized_areas],
                       }
        df_areas_loops = pd.DataFrame(areas_loops, index=[0])

        # Calculate the average values for each array
        ps_area_avg = sum(ps_areas) / len(ps_areas)
        ng_area_avg = sum(ng_areas) / len(ng_areas)
        areas_avg = sum(areas) / len(areas)
        normalized_areas_avg = sum(normalized_areas) / len(normalized_areas)
        ron_avg = sum(ron) / len(ron)
        roff_avg = sum(roff) / len(roff)
        von_avg = sum(von) / len(von)
        voff_avg = sum(voff) / len(voff)

        # Create a dictionary for the new DataFrame
        file_stats = {
            'file_name': [file_info.get('file_name')],
            'ps_area_avg': [ps_area_avg],
            'ng_area_avg': [ng_area_avg],
            'areas_avg': [areas_avg],
            'normalized_areas_avg': [normalized_areas_avg],
            'resistance_on_value': [ron_avg],
            'resistance_off_value': [roff_avg],
            'ON_OFF_Ratio': [eq.zero_devision_check(ron_avg, roff_avg)],
            'voltage_on_value': [von_avg],
            'voltage_off_value': [voff_avg],
        }

        # Create a new DataFrame
        df_file_stats = pd.DataFrame(file_stats, index=[0])

        # Analyze the array changes
        # calculate the changes between each of the areas
        percent_change, avg_change, avg_relative_change, std_relative_change = analyze_array_changes(normalized_areas)

        # create dataframe for device of all the data
        looped_array_info = {'percentage_change': [percent_change],
                             'avg_change': [avg_change],
                             'avg_relative_change': [avg_relative_change],
                             'stf_relative_change': [std_relative_change]}
        looped_array_info = pd.DataFrame(looped_array_info, index=[0])

        f.check_if_folder_exists(device_path, "python_images")

        save_loc = device_path + '\\' + "python_images"
        save_loc_iv = device_path + '\\' + "Iv only"
        #save_loc_iv = device_path + '\\' + "Iv only"



        if plot_graph:

            f.check_if_folder_exists(save_loc, "Looped_Data_in_row")
            row_save = os.path.join(save_loc, "Looped_Data_in_row")

            count = 0
            for arr_v, arr_c in zip(split_v_data, split_c_data):
                count += 1
                # Plots all the graphs individually
                abs_arr_c = eq.absolute_val(arr_c)
                folder_path = Plots.main_plot_loop(arr_v, arr_c, abs_arr_c, count, save_loc, re_save_graph, file_info, slope)
                #Plots.images_in_row(arr_v, arr_c, absolute_val(arr_c) ,file_info, row_save)

            # Plots all the loops on one graph outside of the loop

            f.check_if_folder_exists(save_loc, "GIFS",)
            gif_save_loc = os.path.join(save_loc,"GIFS")
            graph = Plots.main_plot(df['voltage'], df['current'], df['abs_current'], save_loc, re_save_graph,
                                    file_info,slope ,True, num_sweeps)

            # plots GIF of all graphs in looped data
            file_name = os.path.splitext(file_info.get('file_name'))[0]
            save_name_gif = "_" + file_name + ".gif"
            output_gif_loc = os.path.join(gif_save_loc, save_name_gif)

            if re_save_graph or not os.path.exists(output_gif_loc):
                Gifs.create_gif_from_folder(folder_path, output_gif_loc, 2, restart_duration=10)

            save_name_row = file_name + ".png"
            save_loc_images_in_folder = os.path.join(row_save,save_name_row)
            if re_save_graph or not os.path.exists(save_loc_images_in_folder):
                Plots.plot_images_in_folder(folder_path, save_loc_images_in_folder)

            if num_sweeps >= 5:

                f.check_if_folder_exists(save_loc, "Dc-Endurance")

                def find_nearest_indices(array, value):
                    array = np.array(array)
                    indices = np.where(np.isclose(array, value, atol=1e-3))[0]
                    return indices

                def extract_current_values(split_v_data, split_c_data, voltages, num_sweeps):
                    # Ensure num_sweeps is an integer
                    num_sweeps = int(num_sweeps)

                    # Initialize a dictionary to store the current values for each voltage, including negatives
                    all_voltages = voltages + [-v for v in voltages]
                    results = {v: [] for v in all_voltages}

                    # Iterate over each cycle starting from 1 instead of 0
                    for cycle in range(1, num_sweeps + 1):
                        v_data = split_v_data[cycle - 1]  # Adjusting index to match 0-based indexing
                        c_data = split_c_data[cycle - 1]

                        # For each voltage, find the closest current values and store them
                        for v in voltages:
                            indices = np.where(np.isclose(v_data.values, v, atol=1e-3))[
                                0]  # Use .values to handle any index issues
                            if len(indices) == 2:  # Expect exactly two matches (forward and reverse sweep)
                                current_values = [c_data.iloc[indices[0]], c_data.iloc[indices[1]]]
                            else:
                                current_values = [np.nan, np.nan]  # Fallback if not exactly two matches
                            results[v].append(current_values)

                        # Now handle the negative voltages similarly
                        for v in [-v for v in voltages]:
                            indices = np.where(np.isclose(v_data.values, v, atol=1e-3))[0]
                            if len(indices) == 2:  # Expect exactly two matches (forward and reverse sweep)
                                current_values = [c_data.iloc[indices[0]], c_data.iloc[indices[1]]]
                            else:
                                current_values = [np.nan, np.nan]
                            results[v].append(current_values)

                    # Convert results to DataFrames
                    dfs = {}
                    for v in voltages:
                        # Combine positive and negative voltage data into one DataFrame
                        pos_data = pd.DataFrame(results[v], columns=[f'Current_Forward_(OFF)_{v}V', f'Current_Reverse_(ON)_{v}V'])
                        neg_data = pd.DataFrame(results[-v],
                                                columns=[f'Current_Forward_(ON)_{-v}V', f'Current_Reverse_(OFF)_{-v}V'])
                        combined_df = pd.concat([pos_data, neg_data], axis=1)
                        combined_df.index += 1  # Adjust the DataFrame index to start from 1
                        dfs[v] = combined_df


                        # Save Paths
                        save_loc_dc_endurance_df = os.path.join(save_loc,'Dc-Endurance','Data')
                        f.check_if_folder_exists(os.path.join(save_loc,'Dc-Endurance'),'Data')
                        save_loc_dc_endurance_images = os.path.join(save_loc, 'Dc-Endurance')

                        # Save Paths
                        csv_file = f'{file_name}_current_values_{v}V.csv'
                        csv_path = os.path.join(save_loc_dc_endurance_df, csv_file)
                        if re_save_graph or not os.path.exists(csv_path):
                            combined_df.to_csv(csv_path, index_label='Cycle')


                            # Plot the graphs and save the figure
                            fig, ax = plt.subplots(2, 1, figsize=(10, 8))

                            # First subplot: Positive voltages
                            ax[0].plot(combined_df.index, combined_df[f'Current_Forward_(OFF)_{v}V'], marker='o',
                                       label=f'OFF Value {v}V')
                            ax[0].plot(combined_df.index, combined_df[f'Current_Reverse_(ON)_{v}V'], marker='o',
                                       label=f'ON Value {v}V')
                            ax[0].set_xlabel('Cycle')
                            ax[0].set_ylabel('Current (A)')
                            ax[0].set_title(f'Current vs Cycle for {v}V {file_name}')
                            ax[0].legend()
                            ax[0].grid(True)

                            # Second subplot: Negative voltages
                            ax[1].plot(combined_df.index, combined_df[f'Current_Forward_(ON)_{-v}V'], marker='o',
                                       label=f'ON Value {-v}V')
                            ax[1].plot(combined_df.index, combined_df[f'Current_Reverse_(OFF)_{-v}V'], marker='o',
                                       label=f'OFF Value {-v}V')
                            ax[1].set_xlabel('Cycle')
                            ax[1].set_ylabel('Current (A)')
                            ax[1].set_title(f'Current vs Cycle for {-v}V')
                            ax[1].legend()
                            ax[1].grid(True)

                            # Adjust layout and save the plot
                            fig.tight_layout()
                            fig_file = os.path.join(save_loc_dc_endurance_images,f'{file_name}_plot_{v}V.png')
                            if re_save_graph or not os.path.exists(fig_file):
                                plt.savefig(fig_file)
                            plt.close(fig)

                            # Create a final plot with all the voltages
                    num_voltages = len(voltages)
                    fig, axs = plt.subplots(num_voltages, 2, figsize=(12, 4 * num_voltages))

                    for i, v in enumerate(voltages):
                        # Plot for positive voltages
                        axs[i, 0].plot(dfs[v].index, dfs[v][f'Current_Forward_(OFF)_{v}V'], marker='o', label=f'OFF Value {v}V')
                        axs[i, 0].plot(dfs[v].index, dfs[v][f'Current_Reverse_(ON)_{v}V'], marker='o', label=f'ON Value {v}V')
                        axs[i, 0].set_xlabel('Cycle')
                        axs[i, 0].set_ylabel('Current (A)')
                        axs[i, 0].set_title(f'Current vs Cycle for {v}V')
                        axs[i, 0].legend()
                        axs[i, 0].grid(True)

                        # Plot for negative voltages
                        axs[i, 1].plot(dfs[v].index, dfs[v][f'Current_Forward_(ON)_{-v}V'], marker='o',
                                       label=f'ON Value {-v}V')
                        axs[i, 1].plot(dfs[v].index, dfs[v][f'Current_Reverse_(OFF)_{-v}V'], marker='o',
                                       label=f'OFF Value {-v}V')
                        axs[i, 1].set_xlabel('Cycle')
                        axs[i, 1].set_ylabel('Current (A)')
                        axs[i, 1].set_title(f'Current vs Cycle for {-v}V')
                        axs[i, 1].legend()
                        axs[i, 1].grid(True)


                    # Add a main title with the filename
                    fig.suptitle(f'Current vs Cycle for Different Voltages ({file_name})', fontsize=16)
                    fig.suptitle(short_name, fontsize=16)

                    fig.tight_layout()
                    final_fig_file = os.path.join(save_loc_dc_endurance_images,f'_{file_name}_final_plot.png')
                    if re_save_graph or not os.path.exists(final_fig_file):
                        plt.savefig(final_fig_file)
                    plt.close(fig)

                    return dfs

                voltages = [0.1,0.15,0.2]

                # Extract current values
                extract_current_values(split_v_data, split_c_data, voltages, num_sweeps)

                # # Print the resulting DataFrames
                # for v, df in dfs.items():
                #     print(f"DataFrame for {v}V:\n", df, "\n")

        else:
            graph = None




    # # this is for later
    # if num_sweeps == 0.5:
    #     # print("skipping as half sweep")
    #     return None
    else:
        loops = False
        # Data Processing for a single sweep
        ps_area, ng_area, area, normalized_area = area_under_curves(df['voltage'], df["current"])
        resistance_on_value, resistance_off_value, voltage_on_value, voltage_off_value = on_off_values(df['voltage'], df["current"])

        # calculate the initial resistance when first measuring

        file_stats = {'file_name': [file_info.get('file_name')],
                      'ps_area': [ps_area],
                      'ng_area': [ng_area],
                      'area': [area],
                      'normalised_area': [normalized_area],
                      'resistance_on_value': [resistance_on_value],
                      'resistance_off_value': [resistance_off_value],
                      'ON_OFF_Ratio': [eq.zero_devision_check(resistance_on_value, resistance_off_value)],
                      'voltage_on_value': [voltage_on_value],
                      'voltage_off_value': [voltage_off_value],
                      # 'crossing_points': [find_crossings(v_data, c_data)],
                      }
        df_file_stats = pd.DataFrame(file_stats, index=[0])

        f.check_if_folder_exists(device_path, "python_images")
        save_loc = os.path.join(device_path, "python_images")
        save_loc_iv = device_path + '\\' + "Iv only"
        f.check_if_folder_exists(save_loc, "Concution_graphs")
        save_loc_grid = os.path.join(save_loc,"Concution_graphs")

        if plot_graph:
            # this needs finishing
            graph = Plots.main_plot(df['voltage'], df['current'], df['abs_current'], save_loc, re_save_graph, file_info,slope)
            #Plots.iv_and_log_iv_plot(data.get('voltage'), data.get('current'), data.get('abs_current'), save_loc_iv,
#                                       cross_points, re_save_graph, file_info)

            if does_it_exist(save_loc_grid,re_save_graph):
                Plots.grid_spec(df,save_loc_grid,file_info)
        else:
            graph = None

        if save_df:
            # save the data frame
            logger.info(long_name)
            df.to_csv(long_name, index=False)
            if save_parquet:
                try:
                    parquet_path = os.path.splitext(long_name)[0] + '.parquet'
                    df.to_parquet(parquet_path, index=False)
                except Exception as e:
                    logger.warning("Parquet export failed for %s: %s", long_name, e)
        areas_loops = None
        looped_array_info = None
    return num_sweeps, short_name, long_name, df, df_file_stats, graph


def gradient(voltage, current, filename):
    # Filter data for voltage between 0 and max_voltage
    mask = (voltage >= 0) & (voltage <= (max(voltage)/10))
    #print((max(voltage)/10)) #commonly 0.1
    v_filtered = voltage[mask]
    c_filtered = current[mask]

    # Check for NaN, infinite, or zero values
    if np.any(np.isnan(v_filtered)) or np.any(np.isnan(c_filtered)):
        raise ValueError("Filtered data contains NaN values",filename)
    if np.any(np.isinf(v_filtered)) or np.any(np.isinf(c_filtered)):
        raise ValueError("Filtered data contains infinite values",filename)

    # Ensure there are enough unique data points
    if len(v_filtered) < 2 or len(c_filtered) < 2:
        raise ValueError("Not enough data points to perform linear fit",filename)

    if len(np.unique(v_filtered)) < 2 or len(np.unique(c_filtered)) < 2:
        raise ValueError("Not enough unique data points to perform linear fit",filename)

    # Debug: Print filtered data
    #print("Filtered voltage data:", v_filtered)
    #print("Filtered current data:", c_filtered)

    # Calculate the gradient (slope) using numpy's polyfit for linear fit
    try:
        slope, intercept = np.polyfit(v_filtered, c_filtered, 1)
    except np.linalg.LinAlgError as e:
        raise RuntimeError("Linear fit did not converge") from e

    return slope
# def gradient(voltage, current, max_voltage):
#     """ calculate the gradient between 0 and max voltage of a sweep
#     """
#     max_voltage2 = max(voltage)
#     mask = (voltage >= 0) & (voltage <= max_voltage2)
#     v_filtered = voltage[mask]
#     c_filtered = current[mask]
#
#     # Calculate the gradient (slope) using numpy's polyfit for linear fit
#     slope, intercept = np.polyfit(v_filtered, c_filtered, 1)
#     #print(f"The gradient (slope) between 0 and 0.1V is: {slope}")
#     return slope

def does_it_exist(filepath, re_save):
    if os.path.exists(filepath):
        # File exists
        if re_save:
            return True
            # Plot the graph
            # Re-save is True, so create the file (overwriting if it exists)
        if not re_save:
            # Re-save is False wit file exists, skip plot
            pass
    # Save the graph
    else:
        # File doesn't exist
        return True


def split_loops(v_data, c_data, num_loops):
    """ splits the looped data and outputs each sweep as another array"""
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


def analyze_array_changes(arr):
    ''' calculate the array changes for each of the values of enclosed area'''

    # Calculate the percentage change over the length
    percent_change = ((arr[-1] - arr[0]) / arr[0]) * 100

    # Calculate the average change over time
    avg_change = (arr[-1] - arr[0]) / (len(arr) - 1)

    # Compute relative changes between consecutive elements
    relative_changes = np.diff(arr) / arr[:-1]

    # Calculate statistics
    avg_relative_change = np.mean(relative_changes)
    std_relative_change = np.std(relative_changes)

    return percent_change, avg_change, avg_relative_change, std_relative_change


def calculate_metrics_for_loops(split_v_data, split_c_data):
    '''
    Calculate various metrics for each split array of voltage and current data.
    anything that needs completing on loops added in here

    Parameters:
    - split_v_data (list of lists): List containing split voltage arrays
    - split_c_data (list of lists): List containing split current arrays

    Returns:
    - ps_areas (list): List of PS areas for each split array
    - ng_areas (list): List of NG areas for each split array
    - areas (list): List of total areas for each split array
    - normalized_areas (list): List of normalized areas for each split array
    '''

    # Initialize lists to store the values for each metric
    ps_areas = []
    ng_areas = []
    areas = []
    normalized_areas = []
    ron = []
    roff = []
    von = []
    voff = []

    # Loop through each split array
    for idx in range(len(split_v_data)):
        sub_v_array = split_v_data[idx]
        sub_c_array = split_c_data[idx]

        #print(sub_v_array)

        # Call the area_under_curves function for the current split arrays
        ps_area, ng_area, area, norm_area = area_under_curves(sub_v_array, sub_c_array)

        # Append the values to their respective lists
        ps_areas.append(ps_area)
        ng_areas.append(ng_area)
        areas.append(area)
        normalized_areas.append(norm_area)

        r_on, r_off, v_on, v_off = on_off_values(sub_v_array, sub_c_array)

        ron.append(r_on)
        roff.append(r_off)
        von.append(v_on)
        voff.append(v_off)

        # Print the values for the current split array
        # print(f"Metrics for split array {idx + 1}:")
        # print(f"PS Area Enclosed: {ps_area}")
        # print(f"NG Area Enclosed: {ng_area}")
        # print(f"Total Area Enclosed: {area}")
        # print(f"Normalized Area Enclosed: {norm_area}")
        # print("------")

    # Print the lists of values
    # print("\nList of PS Areas:", ps_areas)
    # print("List of NG Areas:", ng_areas)
    # print("List of Total Areas:", areas)
    # print("List of Normalized Areas:", normalized_areas)

    # Return the calculated metrics
    return ps_areas, ng_areas, areas, normalized_areas, ron, roff, von, voff


def area_under_curves(v_data, c_data):
    """
    only run this for an individual sweep
    :return: ps_area_enclosed,ng_area_enclosed,total_area_enclosed
    """
    # finds v max and min
    v_max, v_min = bounds(v_data)

    # creates dataframe of the sweep in sections
    df_sections = split_data_in_sect(v_data, c_data, v_max, v_min)

    # calculate the area under the curve for each section
    sect1_area = abs(area_under_curve(df_sections.get('voltage_ps_sect1'), df_sections.get('current_ps_sect1')))
    sect2_area = abs(area_under_curve(df_sections.get('voltage_ps_sect2'), df_sections.get('current_ps_sect2')))
    sect3_area = abs(area_under_curve(df_sections.get('voltage_ng_sect1'), df_sections.get('current_ng_sect1')))
    sect4_area = abs(area_under_curve(df_sections.get('voltage_ng_sect2'), df_sections.get('current_ng_sect2')))

    # plot to show where each section is on the hysteresis
    # plt.plot(df_sections.get('voltage_ps_sect1'), df_sections.get('current_ps_sect1'),color="blue" )
    # plt.plot(df_sections.get('voltage_ps_sect2'), df_sections.get('current_ps_sect2'),color="green")
    # plt.plot(df_sections.get('voltage_ng_sect1'), df_sections.get('current_ng_sect1'),color="red")
    # plt.plot(df_sections.get('voltage_ng_sect2'), df_sections.get('current_ng_sect2'),color="yellow")
    # #plt.legend()
    # plt.show()
    # plt.pause(0.1)

    # blue - green
    # red - yellow

    ps_area_enclosed = abs(sect2_area) - abs(sect1_area)
    ng_area_enclosed = abs(sect3_area) - abs(sect4_area)
    area_enclosed = ps_area_enclosed + ng_area_enclosed
    norm_area_enclosed = area_enclosed / (abs(v_max) + abs(v_min))

    # added nan check as causes issues later if not a value
    if math.isnan(norm_area_enclosed):
        norm_area_enclosed = 0
    if math.isnan(ps_area_enclosed):
        ps_area_enclosed = 0
    if math.isnan(ng_area_enclosed):
        ng_area_enclosed = 0
    if math.isnan(area_enclosed):
        area_enclosed = 0

    return ps_area_enclosed, ng_area_enclosed, area_enclosed, norm_area_enclosed


def split_data_in_sect(voltage, current, v_max, v_min):
    # splits the data into sections and clculates the area under the curve for how "memeristive" a device is.
    zipped_data = list(zip(voltage, current))

    positive = [(v, c) for v, c in zipped_data if 0 <= v <= v_max]
    negative = [(v, c) for v, c in zipped_data if v_min <= v <= 0]

    # Find the maximum length among the four sections
    max_len = max(len(positive), len(negative))

    # Split positive section into two equal parts
    positive1 = positive[:max_len // 2]
    positive2 = positive[max_len // 2:]

    # Split negative section into two equal parts
    negative3 = negative[:max_len // 2]
    negative4 = negative[max_len // 2:]

    # Find the maximum length among the four sections
    max_len = max(len(positive1), len(positive2), len(negative3), len(negative4))

    # Calculate the required padding for each section
    pad_positive1 = max_len - len(positive1)
    pad_positive2 = max_len - len(positive2)
    pad_negative3 = max_len - len(negative3)
    pad_negative4 = max_len - len(negative4)

    # Limit the padding to the length of the last value for each section
    last_positive1 = positive1[-1] if positive1 else (0, 0)
    last_positive2 = positive2[-1] if positive2 else (0, 0)
    last_negative3 = negative3[-1] if negative3 else (0, 0)
    last_negative4 = negative4[-1] if negative4 else (0, 0)

    positive1 += [last_positive1] * pad_positive1
    positive2 += [last_positive2] * pad_positive2
    negative3 += [last_negative3] * pad_negative3
    negative4 += [last_negative4] * pad_negative4

    # Create DataFrame for device
    sections = {
        'voltage_ps_sect1': [v for v, _ in positive1],
        'current_ps_sect1': [c for _, c in positive1],
        'voltage_ps_sect2': [v for v, _ in positive2],
        'current_ps_sect2': [c for _, c in positive2],
        'voltage_ng_sect1': [v for v, _ in negative3],
        'current_ng_sect1': [c for _, c in negative3],
        'voltage_ng_sect2': [v for v, _ in negative4],
        'current_ng_sect2': [c for _, c in negative4],
    }

    df_sections = pd.DataFrame(sections)
    return df_sections


def area_under_curve(voltage, current):
    """
    Calculate the area under the curve given voltage and current data.
    """

    # print(voltage,current)
    voltage = np.array(voltage)
    current = np.array(current)
    # Calculate the area under the curve using the trapezoidal rule
    area = np.trapz(current, voltage)
    # which ever is in np.trapz(y,x), Using a decreasing x corresponds to integrating in reverse: ie negative value?
    return area


def bounds(data):
    """
    :param data:
    :return: max and min values of given array max,min
    """
    max = np.max(data)
    min = np.min(data)
    return max, min


def check_for_loops(v_data) -> float:
    """
    Robust loop detection using zero-crossing events with tolerance to floating noise.
    Returns 0.5 for half-sweeps, 1 for a single loop, or an estimated number for multi-loops.
    """
    v_arr = np.asarray(v_data)
    if v_arr.size == 0:
        return 0
    vmax = np.max(np.abs(v_arr))
    if vmax == 0:
        return 0
    tol = max(1e-6, 1e-3 * vmax)

    # Identify zero-crossing events (from negative to positive or vice versa)
    signs = np.sign(v_arr)
    # Treat small values within tolerance as zeros
    signs[np.abs(v_arr) <= tol] = 0
    # Collapse consecutive duplicates to count events
    diffs = np.diff(signs)
    # Count transitions that pass through zero or change sign
    zero_events = np.sum(diffs != 0)

    # Heuristic mapping to loops
    if zero_events <= 1:
        return 0.5
    if zero_events <= 3:
        return 1
    # Approximate: each additional full sweep adds about 3 transitions
    loops_est = max(1.0, round(zero_events / 3.0))
    return float(loops_est)


def split_iv_sweep(filepath):
    data = np.loadtxt(filepath, unpack=True, skiprows=1)
    voltage = data[0]
    current = data[1]
    # try:
    #     time = data[2]
    time = None
    return voltage, current,time


def check_sweep_type(filepath, output_file):
    import re

    def is_number(s):
        """Check if a string represents a number."""
        try:
            float(s)
            return True
        except ValueError:
            return False

    # Open the file at the given filepath
    with open(filepath, 'r', encoding='utf-8') as file:
        # Read the first line and remove any leading/trailing whitespace
        first_line = file.readline().strip()
        # print(first_line)

        # Check if the first line is empty, indicating no more lines
        if not first_line:
            print("No more lines after the first. Returning None.")
            with open(output_file, 'a', encoding='utf-8') as out_file:
                out_file.write(filepath + '\n')
            return None

        # Read the second line and remove any leading/trailing whitespace
        second_line = file.readline().strip()

        # Check if the second line is empty, indicating no more lines
        if not second_line:
            # print("No more lines after the second. Returning None.")
            with open(output_file, 'a', encoding='utf-8') as out_file:
                out_file.write(filepath + '\n')
            return None

        # Read the next three lines and remove any leading/trailing whitespace
        nan_check_lines = [file.readline().strip() for _ in range(3)]
        # Check if any of the next three lines contain the word "NaN"
        if any('NaN' in line for line in nan_check_lines):
            # print("One of the lines contains 'nan'. Returning None.")
            with open(output_file, 'a', encoding='utf-8') as out_file:
                out_file.write(filepath + '\n')
            return None

    # Define dictionaries for different types of sweeps and their expected column headings
    sweep_types = {
        'Iv_sweep': [
            ['voltage', 'current'],  # Pattern 1
            ['vOLTAGE', 'cURRENT'],  # Pattern 2
            ['VSOURC - Plot 0', 'IMEAS - Plot 0'],
            ['VSOURC - Plot 0	IMEAS - Plot 0'],
            ['Voltage', 'Current','Time'],  # Pattern 1

            # Add more patterns if needed
        ],
        'Endurance': ['Iteration #', 'Time (s)', 'Resistance (Set)', 'Set Voltage', 'Time (s)', 'Resistance (Reset)',
                      'Reset Voltage'],
        'Retention': ['Iteration #', 'Time (s)', 'Current (Set)'],
        # 'type4': ['V', 'z', 'Pressure'],
    }

    # Check if the actual headings match any of the expected ones
    for sweep_type, expected_patterns in sweep_types.items():
        for pattern in expected_patterns:
            # Check if all headings in the pattern are present in the first line
            if all(heading in first_line for heading in pattern):
                if pattern == ['VSOURC - Plot 0', 'IMEAS - Plot 0']:
                    print(
                        "Warning: Pattern 3 matched for Iv_sweep. Consider updating the data format. Check data, check_sweep_type, filepath below:")
                    print("file found at", filepath)
                # print(f"Column headings match {sweep_type} sweep.")
                return sweep_type

    # Check if there are only two columns and they start with numbers, indicating an IV sweep
    first_line_values = first_line.split()
    second_line_values = second_line.split()
    if len(first_line_values) == 2 and len(second_line_values) == 2:
        if is_number(first_line_values[0]) and is_number(first_line_values[1]) and is_number(
                second_line_values[0]) and is_number(second_line_values[1]):
            return 'Iv_sweep'

    # print("Column headings do not match any expected sweep types.")
    # Store the file path in the output file and return None
    with open(output_file, 'a', encoding='utf-8') as out_file:
        out_file.write(filepath + '\n')

    return None


# def check_sweep_type(filepath):
#     def is_number(s):
#         """Check if a string represents a number."""
#         try:
#             float(s)
#             return True
#         except ValueError:
#             return False
#
#     # Open the file at the given filepath
#     with open(filepath, 'r') as file:
#         # Read the first line and remove any leading/trailing whitespace
#         first_line = file.readline().strip()
#         # print(first_line)
#
#         # Check if the first line is empty, indicating no more lines
#         if not first_line:
#             print("No more lines after the first. Returning None.")
#             return None
#
#         # Read the second line and remove any leading/trailing whitespace
#         second_line = file.readline().strip()
#
#         # Check if the second line is empty, indicating no more lines
#         if not second_line:
#             # print("No more lines after the second. Returning None.")
#             return None
#
#         # Read the next three lines and remove any leading/trailing whitespace
#         nan_check_lines = [file.readline().strip() for _ in range(3)]
#         # Check if any of the next three lines contain the word "NaN"
#         if any('NaN' in line for line in nan_check_lines):
#             # print("One of the lines contains 'nan'. Returning None.")
#             return None
#
#         # # Check if any line in the file contains the word "nan"
#         # if any('NaN' in line.lower() for line in file.readlines()):
#         #     print("The file contains 'nan'.")
#         #     return None
#
#     # Define dictionaries for different types of sweeps and their expected column headings
#     sweep_types = {
#         'Iv_sweep': [
#             ['voltage', 'current'],  # Pattern 1
#             ['vOLTAGE', 'cURRENT'],  # Pattern 2
#             ['VSOURC - Plot 0', 'IMEAS - Plot 0'],
#             # Add more patterns if needed
#         ],
#         'Endurance': ['Iteration #', 'Time (s)', 'Resistance (Set)', 'Set Voltage', 'Time (s)', 'Resistance (Reset)',
#                       'Reset Voltage'],
#         'Retention': ['Iteration #', 'Time (s)', 'Current (Set)'],
#         # 'type4': ['V', 'z', 'Pressure'],
#     }
#
#     # Check if the actual headings match any of the expected ones
#     for sweep_type, expected_patterns in sweep_types.items():
#         for pattern in expected_patterns:
#             # Check if all headings in the pattern are present in the first line
#             if all(heading in first_line for heading in pattern):
#                 if pattern == ['VSOURC - Plot 0', 'IMEAS - Plot 0']:
#                     print(
#                         "Warning: Pattern 3 matched for Iv_sweep. Consider updating the data format. check data, check_sweep_type, filepath below:")
#                     print("file found at", filepath)
#                 # print(f"Column headings match {sweep_type} sweep.")
#                 return sweep_type
#
#     # Check if there are only two columns and they start with numbers, indicating an IV sweep
#     first_line_values = first_line.split()
#     second_line_values = second_line.split()
#     if len(first_line_values) == 2 and len(second_line_values) == 2:
#         if is_number(first_line_values[0]) and is_number(first_line_values[1]) and is_number(
#                 second_line_values[0]) and is_number(second_line_values[1]):
#             return 'Iv_sweep'
#
#     # print("Column headings do not match any expected sweep types.")
#     # Perform another action if needed, e.g., return None or do something else
#
#     with open(output_file, 'a') as out_file:
#         out_file.write(filepath + '\n')
#     return None

## ------------------------------------------------------------------------------------##



def on_off_values(voltage_data, current_data):
    """
    Calculates r on off and v on off values for an individual device
    """
    # Convert DataFrame columns to lists
    voltage_data = voltage_data.to_numpy()
    current_data = current_data.to_numpy()
    # Initialize lists to store Ron and Roff values
    resistance_on_value = []
    resistance_off_value = []
    # Initialize default values for on and off voltages
    voltage_on_value = 0
    voltage_off_value = 0

    # Get the maximum voltage value
    max_voltage = round(max(voltage_data), 1)
    # Catch edge case for just negative sweep only
    if max_voltage == 0:
        max_voltage = abs(round(min(voltage_data), 1))

    # Set the threshold value to 0.2 times the maximum voltage
    threshold = round(0.2 * max_voltage, 2)
    # print("threshold,max_voltage")
    # print(threshold,max_voltage)
    # print(len(voltage_data))
    # print(voltage_data)

    # Filter the voltage and current data to include values within the threshold
    filtered_voltage = []
    filtered_current = []
    for index in range(len(voltage_data)):
        #print(index)
        if -threshold < voltage_data[index] < threshold:
            filtered_voltage.append(voltage_data[index])
            filtered_current.append(current_data[index])
    # print(filtered_voltage)

    resistance_magnitudes = []
    for idx in range(len(filtered_voltage)):
        if filtered_voltage[idx] != 0 and filtered_current[idx] != 0:
            resistance_magnitudes.append(abs(filtered_voltage[idx] / filtered_current[idx]))

    if not resistance_magnitudes:
        # Handle the case when the list is empty, e.g., set default values or raise an exception.
        print("Error: No valid resistance values found.")
        return 0, 0, 0, 0

    # # Calculate the resistance magnitude for each filtered data point
    # resistance_magnitudes = []
    # for idx in range(len(filtered_voltage)):
    #     if filtered_voltage[idx] != 0:
    #         resistance_magnitudes.append(abs(filtered_voltage[idx] / filtered_current[idx]))
    # print(resistance_magnitudes)
    # Store the minimum and maximum resistance values
    resistance_off_value = min(resistance_magnitudes)
    resistance_on_value = max(resistance_magnitudes)

    # Calculate the gradients for each data point
    gradients = []
    for idx in range(len(voltage_data)):
        if idx != len(voltage_data) - 1:
            if voltage_data[idx + 1] - voltage_data[idx] != 0:
                gradients.append(
                    (current_data[idx + 1] - current_data[idx]) / (voltage_data[idx + 1] - voltage_data[idx]))

    # Find the maximum and minimum gradient values
    max_gradient = max(gradients[:(int(len(gradients) / 2))])
    min_gradient = min(gradients)

    # Use the maximum and minimum gradient values to determine the on and off voltages
    for idx in range(len(gradients)):
        if gradients[idx] == max_gradient:
            voltage_off_value = voltage_data[idx]
        if gradients[idx] == min_gradient:
            voltage_on_value = voltage_data[idx]

    # Return the calculated Ron and Roff values and on and off voltages
    return resistance_on_value, resistance_off_value, voltage_on_value, voltage_off_value


def save_df_off_data(sample_path, final_data_dict, final_sweeps_dict):
    """
    saves df of data for each sample

    :param sample_path: full sample path
    :return: n/a saves file stats_dict in the location sample path
    """
    # Open the file in write mode
    with open(sample_path + '/final_data_dict.txt', 'w', encoding='utf-8') as file:

        file.write("###########################\n")
        # Iterate through sample_stats_dict
        for sample_name, section_info_stats in final_data_dict.items():
            file.write("------------------------\n")
            file.write(f"Sample Name: {sample_name}\n")
            file.write("------------------------\n")

            # Iterate through section_info_stats
            for section_name, devices in section_info_stats.items():
                file.write(f"Section Name: {section_name}\n")
                file.write("------------------------\n")

                # Access corresponding information from sample_sweeps_dict
                section_info_sweeps = final_sweeps_dict.get(sample_name, {}).get(section_name, {})

                # Iterate through devices
                for device_number, info in devices.items():
                    file.write(f"Device Number: {device_number}\n")
                    # Print corresponding info from sample_sweeps_dict if available
                    sweeps_info = section_info_sweeps.get(device_number, "No sweeps info available")
                    file.write(f"Number of sweeps: {sweeps_info}\n")
                    # file.write(f"{info}\n")
                    file.write("------------------------\n")

                    # Iterate through the first 5 items in info
                    for sweep, sweep_value in info.items():
                        file.write(f"{sweep}: {sweep_value}\n")
                        # print(sweep)
                        file.write("------------------------\n")


def save_df_off_stats(sample_path, final_stats_dict, final_sweeps_dict):
    """

    :param sample_path: full sample path
    :return: n/a saves file stats_dict in the location sample path
    """
    # Open the file in write mode
    with open(sample_path + '/stats_dict.txt', 'w', encoding='utf-8') as file:

        file.write("###########################\n")
        # Iterate through sample_stats_dict
        for sample_name, section_info_stats in final_stats_dict.items():
            file.write("------------------------\n")
            file.write(f"Sample Name: {sample_name}\n")
            file.write("------------------------\n")

            # Iterate through section_info_stats
            for section_name, devices in section_info_stats.items():
                file.write(f"Section Name: {section_name}\n")
                file.write("------------------------\n")

                # Access corresponding information from sample_sweeps_dict
                section_info_sweeps = final_sweeps_dict.get(sample_name, {}).get(section_name, {})

                # Iterate through devices
                for device_number, info in devices.items():
                    file.write(f"Device Number: {device_number}\n")
                    # Print corresponding info from sample_sweeps_dict if available
                    sweeps_info = section_info_sweeps.get(device_number, "No sweeps info available")
                    file.write(f"Number of sweeps: {sweeps_info}\n")
                    file.write(f"{info}\n")
                    file.write("------------------------\n")

    # def save_df_off_stats(sample_path, final_stats_dict, final_sweeps_dict):
    #     """
    #
    #     :param sample_path: full sample path
    #     :return: n/a saves file stats_dict in the location sample path
    #     """
    #     # Open the file in write mode
    #     with open(sample_path + '/stats_dict.txt', 'w', encoding='utf-8') as file:
    #
    #         file.write("###########################\n")
    #         # Iterate through sample_stats_dict
    #         for sample_name, section_info_stats in final_stats_dict.items():
    #             file.write("------------------------\n")
    #             file.write(f"Sample Name: {sample_name}\n")
    #             file.write("------------------------\n")
    #
    #             # Iterate through section_info_stats
    #             for section_name, devices in section_info_stats.items():
    #                 file.write(f"Section Name: {section_name}\n")
    #                 file.write("------------------------\n")
    #
    #                 # Access corresponding information from sample_sweeps_dict
    #                 section_info_sweeps = final_sweeps_dict.get(sample_name, {}).get(section_name, {})
    #
    #                 file.write(f"Device Number: {section_name}\n")
    #                 # Print corresponding info from sample_sweeps_dict if available
    #                 sweeps_info = section_info_sweeps.get(section_name, "No sweeps info available")
    #                 file.write(f"Number of sweeps: {sweeps_info}\n")
    #                 file.write(f"{devices}\n")
    #                 file.write("------------------------\n")


def set_pandas_display_options() -> None:
    """Set pandas display options."""
    # Ref: https://stackoverflow.com/a/52432757/
    display = pd.options.display

    display.max_columns = 1000
    display.max_rows = 1000
    display.max_colwidth = 199
    display.width = 1000
    # display.precision = 2  # set as needed
    # display.float_format = lambda x: '{:,.2f}'.format(x)  # set as needed
