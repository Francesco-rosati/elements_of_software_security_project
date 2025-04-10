# This module is responsible for evaluating the user scenarios by reading packets from two pcapng files in the evaluation set.

import sys
from colorama import Fore, Style
from common_modules.flow_labeling import get_activity_name_from_label
from common_modules.ip_addresses import get_ip_address
from common_modules.utilities import list_pcapng_files, read_evaluation_pcapng_files, convert_timestamp_to_mdt
from evaluation_modules.evaluation_utilities import window_packets, classify_window

# Define overlap time in seconds -> you can change it according to the model you are using
# The overlap time is the time between two consecutive windows. It is used to ensure that the windows are not completely disjoint.
# Be sure to set the overlap time to a value that is less than the delta time.
overlap = 2

# This function evaluates all the user scenarios by reading packets from a pcapng file in the evaluation set
def evaluate_user_scenarios(folder_path, delta):
    """
    This function processes all .pcapng files in the folder, splits the packets into overlapping time windows,
    and performs classification on each window.

    :param folder_path: The path to the evaluation set folder.
    :param delta: The delta value used for filtering packets.

    :return: A dictionary with, for each file, a list of predictions for each window.
    """

    # Define the device names to be filtered
    device_names = ['sonos-smart-speaker', 'tplink-tapo-camera']

    # Get device IP addresses
    device_ip_addresses = []

    for device_name in device_names:
        device_ip = get_ip_address(device_name)
        if device_ip == -1:
            print(f'{Fore.RED}\nERROR: No IP address found for device: {Style.RESET_ALL}{device_name}')
            sys.exit(1)
        device_ip_addresses.append(device_ip)

    results = {}

    # Get the list of .pcapng files in the folder
    pcapng_files = list_pcapng_files(folder_path)

    if not pcapng_files:
        print(f"{Fore.RED}No .pcapng files found in folder: {folder_path}{Style.RESET_ALL}")
        return results

    for file_path in pcapng_files:

        # Get file name
        file_name = file_path.split('/')[-1]

        # Read packets from the current .pcapng file
        print(f'\n{Fore.BLUE}Reading packets from file: {Style.RESET_ALL}{file_path}')

        packets = read_evaluation_pcapng_files(file_path, device_ip_addresses)

        print(f'{Fore.GREEN}Packets successfully read!{Style.RESET_ALL}')

        if not packets:
            print(f"{Fore.RED}No packets read from {file_name}{Style.RESET_ALL}")
            continue

        # Split packets into time windows with 2 seconds overlap
        windows = window_packets(packets, delta, overlap)
        file_results = []
        for idx, window in enumerate(windows):
            print(f"\nProcessing window {idx + 1}/{len(windows)}\n")

            # Convert window start and end times to MDT format
            start_mdt = convert_timestamp_to_mdt(window['start_time'])
            end_mdt = convert_timestamp_to_mdt(window['end_time'])

            print(f"{Fore.YELLOW}Window start time: {Style.RESET_ALL}{start_mdt}")
            print(f"{Fore.YELLOW}Window end time: {Style.RESET_ALL}{end_mdt}")

            # Classify the window
            prediction = classify_window(window['packets'], device_ip_addresses, delta)

            if prediction is None:
                print(f"{Fore.RED}Window {idx + 1} is not valid!\nNo incoming or outgoing packets to analyze!{Style.RESET_ALL}")
                continue

            file_results.append({
                "window_index": idx,
                "start_time_mdt": start_mdt,
                "end_time_mdt": end_mdt,
                "rf_prediction": get_activity_name_from_label(prediction[0]),
                "xgb_prediction": get_activity_name_from_label(prediction[1])
            })
        results[file_path] = file_results

    return results