
''' for printing all info '''
def print_on_off_ratio_info(input):
    # Print the comprehensive information outside the function
    for sample_key, sample_info in input.items():
        print(f"Comprehensive Information for {sample_key}:")
        print(f"Best Device: #{sample_info['best_device']['device_key']}, Mean ON_OFF_Ratio: {sample_info['mean_ON_OFF_Ratio']}")
        print(f"Top 3 Devices:")
        for idx, device_info in enumerate(sample_info['top3_devices'], start=1):
            print(f"#{idx}: Device: #{device_info['device_key']}, ON_OFF_Ratio: {device_info['ON_OFF_Ratio']}, File Name: {device_info['file_name']}")
        print(f"Mean ON_OFF_Ratio: {sample_info['mean_ON_OFF_Ratio']}")
        print(f"Median ON_OFF_Ratio: {sample_info['median_ON_OFF_Ratio']}")
        print(f"Mode ON_OFF_Ratio: {sample_info['mode_ON_OFF_Ratio']}")
        print("\n")

def print_normalised_area_info(input):

    for sample_key, sample_info in input.items():
        print(f"Comprehensive Information for {sample_key}:")
        print(
            f"Best Device: #{sample_info['best_device']['device_key']}, Mean normalised_area: {sample_info['mean_normalised_area']}")
        print(f"Top 3 Devices:")
        for idx, device_info in enumerate(sample_info['top3_devices'], start=1):
            print(
                f"#{idx}: Device: #{device_info['device_key']}, ON_OFF_Ratio: {device_info['normalised_area']}, File Name: {device_info['file_name']}")
        print(f"Mean normalised_area: {sample_info['mean_normalised_area']}")
        print(f"Median normalised_area: {sample_info['median_normalised_area']}")
        print(f"Mode normalised_area: {sample_info['mode_normalised_area']}")
        print("\n")
