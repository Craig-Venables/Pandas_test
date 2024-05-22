import math

""" statistics for post processing of the data related to more than a single file"""

def calculate_yield(material_sweeps_dict: dict) -> dict:
    """
    Calculate the yield for each sample name based on the number of measured devices and occurrences of "memristive".

    Args:
        material_sweeps_dict (dict): Dictionary containing material sweeps.

    Returns:
        dict: Dictionary with sample names as keys and corresponding yield values. In decending order
    """
    yield_dict = {}
    yield_dict_sect = {}
    for material, polymer_dict in material_sweeps_dict.items():
        for polymer, sample_dict in polymer_dict.items():
            for sample_name, section_dict in sample_dict.items():

                measured = 0
                memristive_device_count = 0
                for section_name, device_dict in section_dict.items():
                    num_measured_devices = len(device_dict)

                    memristive_count = sum(
                        1 for device_data in device_dict.values() if device_data.get('classification') == 'Memristive')

                    # Update measured and memristive_device_count for each section
                    measured += num_measured_devices
                    memristive_device_count += memristive_count

                    if num_measured_devices > 0:
                        yield_value = memristive_count / num_measured_devices
                        yield_dict_sect[f'{material}_{polymer}_{sample_name}_{section_name}'] = yield_value

                if measured > 0:
                    yield_value_sample = memristive_device_count / measured
                    yield_dict[f'{material}_{polymer}_{sample_name}'] = yield_value_sample

    sorted_yield_dict = dict(sorted(yield_dict.items(), key=lambda item: item[1], reverse=True))
    sorted_yield_dict_sect = dict(sorted(yield_dict_sect.items(), key=lambda item: item[1], reverse=True))

    return sorted_yield_dict, sorted_yield_dict_sect


def find_top_samples(material_stats_dict: dict, property_name: str = 'ON_OFF_Ratio', top_n: int = 10) -> tuple:
    """
    This function finds the top samples based on a given property (ON-OFF ratio or normalized area) in a given material_stats_dict.

    Args:
        material_stats_dict (dict): A dictionary containing the material, polymer, and sample dictionaries.
        property_name (str, optional): The name of the property to be used for sorting the samples. Defaults to 'ON_OFF_Ratio'.
        top_n (int, optional): The number of samples to be returned. Defaults to 10.

    Returns:
        tuple: A tuple containing three lists: all_samples_info, samples_with_repetition, and samples_without_repetition.
            all_samples_info (list): A list containing information for all samples, including sample_key, section_key, device_key, file_name, and property_value.
            samples_with_repetition (list): A list containing the sample keys that appear multiple times in all_samples_info.
            samples_without_repetition (list): A list containing the sample keys that appear only once in all_samples_info.

    """
    # List to store information for all samples
    all_samples_info = []

    # Iterate through the material, polymer, and sample dictionaries
    for material_key, polymer_dict in material_stats_dict.items():
        for polymer_key, sample_dict in polymer_dict.items():
            for sample_key, section_dict in sample_dict.items():
                # List to store information for each sample
                sample_info = []

                # Iterate through devices in the sample
                for section_key, device_dict in section_dict.items():
                    for device_key, stats_df in device_dict.items():
                        # Check if 'file_name' and property_name exist in stats_df
                        if 'normalized_areas_avg' in stats_df.columns:
                            property_name = 'normalized_areas_avg'
                        elif 'normalised_area' in stats_df.columns:
                            property_name = 'normalised_area'
                        else:
                            print("Neither 'normalized_areas_avg' nor 'normalised_area' found in stats_df columns.")
                            continue

                        #print(material_key,polymer_key,sample_key,section_key,"-----",device_key)
                        #print(stats_df)

                        if property_name in stats_df.columns:
                            max_property_index = stats_df[property_name].idxmax()
                            property_value = stats_df[property_name].iloc[max_property_index]

                            file_name = stats_df['file_name'].iloc[max_property_index]

                            # Append sample information to the list
                            sample_info.append({
                                'sample_key': sample_key,
                                'section_key': section_key,
                                'device_key': device_key,
                                'file_name': file_name,
                                'property_value': property_value
                            })
                        else:
                            print(f"Column '{property_name}' not found in stats_df.")
                            continue

                # Sort the devices based on the given property in descending order
                sample_info.sort(key=lambda x: (
                    float('-inf') if x['property_value'] is None or math.isnan(x['property_value']) else x[
                        'property_value']), reverse=True)
                top_samples_individual = sample_info[:top_n]

                # Store the top samples based on the given property
                top_samples_individual = sample_info[:top_n]

                # Store the information for all samples
                all_samples_info.extend(top_samples_individual)

    # Separate lists for samples with and without repetition
    samples_with_repetition = [info['sample_key'] for info in all_samples_info]
    samples_without_repetition = list(set(samples_with_repetition))

    return all_samples_info, samples_with_repetition, samples_without_repetition


def find_sample_number_sweeps(material_sweeps_dict: dict, material: str, polymer: str, sample_name: str) -> tuple:
    """
        Find the sample name and total sum of a given material, polymer, and sample name in a material sweeps dictionary.

        Args:
            material_sweeps_dict (dict): Dictionary containing material sweeps.
            material (str): Material name.
            polymer (str): Polymer name.
            sample_name (str): Sample name.

        Returns:
            tuple: Tuple containing the sample name and total sum.
        """
    data = material_sweeps_dict[f'{material}'][f'{polymer}'][f'{sample_name}']

    def recursive_sum(value):
        if isinstance(value, (int, float)):
            return value
        elif isinstance(value, dict):
            return sum(recursive_sum(v) for v in value.values())
        else:
            return 0

    total_sum = sum(
        recursive_sum(value.get('num_of_sweeps', 0)) for inner_dict in data.values() for value in inner_dict.values() if
        isinstance(value, dict))
    # print(total_sum)
    return sample_name, total_sum


def get_num_sweeps_ordered(file_info_dict: dict, material_sweeps_dict: dict) -> dict:
    """
    Get the number of sweeps in the data in an ordered dictionary.

    Parameters:
        file_info_dict (dict): Dictionary containing file information.
        material_sweeps_dict (dict): Dictionary containing material sweeps.

    Returns:
        dict: Ordered dictionary containing file information and total sum.
    """
    result_dict = {}

    def order_dict_by_total_sum(input_dict: dict) -> dict:
        """
        Order a dictionary by the total sum.

        Parameters:
            input_dict (dict): Dictionary to be ordered.

        Returns:
            dict: Ordered dictionary.
        """
        # Sort the dictionary by 'total_sum' in descending order
        sorted_dict = dict(sorted(input_dict.items(), key=lambda item: item[1]['total_sum'], reverse=True))

        return sorted_dict

    for file_key, file_info in file_info_dict.items():
        material = file_info['material']
        polymer = file_info['polymer']
        sample_name = file_info['sample_name']

        # Assuming find_sample_number_sweeps returns 'sample_name' and 'total_sum'
        sample_name, total_sum = find_sample_number_sweeps(material_sweeps_dict, material, polymer, sample_name)

        file_key2 = f'{material}_{polymer}_{sample_name}'

        result_dict[file_key2] = {
            'sample_name': sample_name,
            'total_sum': total_sum
            # 'classification': classification
        }

    ordered_dict = order_dict_by_total_sum(result_dict)
    return ordered_dict
