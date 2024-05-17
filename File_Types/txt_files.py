from memristors import memristors as eq


def txt_file(file_name,file_path, total_files, plot_graph, save_df, device_path, re_save_graph, processed_files, num_of_sweeps,file_data,list_of_file_stats,list_of_graphs,list_of_measured_files):
    # began changing this into function not sure yet
    """Loops through each file in the folder and analyses them using the
    functions here"""

    # Percentage completed
    processed_files += 1
    percentage_completed_files = (processed_files / total_files) * 100

    # Checks and returns the sweep type of the file also checks for nan
    # values if nan values are present returns None

    sweep_type = eq.check_sweep_type(file_path)
    # print(sweep_type)

    if sweep_type == 'Iv_sweep':
        """ for simple iv sweeps"""

        # Performs analysis on the file given returning the dataframe
        analysis_result = eq.file_analysis(file_path, plot_graph, save_df,
                                           device_path, re_save_graph)

        # if analysis_result is None:
        #     # if there is an error in reading the file it will just continue
        #     # skipping
        #     continue

        num_sweeps, short_name, long_name, data, file_stats, graph = analysis_result

        # keeps count of the number of sweeps by each device
        num_of_sweeps += num_sweeps

        # storing information from analysis
        list_of_measured_files.append(long_name)
        list_of_graphs.append(graph)
        list_of_file_stats.append(file_stats)
        file_data[f'{file_name}'] = data

        return percentage_completed_files, processed_files, num_of_sweeps, num_sweeps, short_name, long_name, data, file_stats
    else:
        # if there is an error in reading the file it will just continue
        # skipping
        print("Not iv sweep")

        # continue


