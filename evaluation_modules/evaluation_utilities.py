# This file contains utility functions for evaluating user scenarios by processing .pcapng files.
import os

import joblib
from colorama import Style, Fore
from scapy.layers.inet import IP
from common_modules.flow_labeling import get_activity_name_from_label
from common_modules.utilities import compute_statistical_features


# This function creates packet windows from the given list of packets based on the specified delta and overlap.
def window_packets(packets, delta, overlap=2):
    """
    Splits packets within the analyzed .pcapng file into time windows.

    :param packets: list of packets from pcapng file.
    :param delta: duration of each window in seconds.
    :param overlap: overlapping time between windows in seconds (default: 2).

    :return: list of windows, where each window is a list of packets.
    """
    if not packets:
        return []

    windows = []
    start_time = packets[0].time
    end_time = packets[-1].time
    step = delta - overlap  # window shift

    current_start = start_time
    while current_start <= end_time:
        current_end = current_start + delta
        # Select all packets with timestamp in [current_start, current_end)
        window_pkts = [pkt for pkt in packets if current_start <= pkt.time < current_end]

        if window_pkts:
            windows.append({
                'packets': window_pkts,
                'start_time': current_start,
                'end_time': current_end
            })
        current_start += step
    return windows

# This function classifies a window of packets using pre-trained models.
def classify_window(window, device_ip_addresses, delta):
    """
    Computes the features of the window and returns the model predictions.

    :param window: list of packets in a window.
    :param device_ip_addresses: list of IP addresses of the devices to be filtered.
    :param delta: delta value to load the correct model.

    :return: tuple (rf_prediction, xgb_prediction) or None if window is not valid.
    """

    outgoing_packets = [pkt for pkt in window if pkt.haslayer(IP) and pkt[IP].src in device_ip_addresses]
    incoming_packets = [pkt for pkt in window if pkt.haslayer(IP) and pkt[IP].dst in device_ip_addresses]

    # If there are no valid packets for one of the flows, skip the window
    if not outgoing_packets or not incoming_packets:
        return None

    flow_features = compute_statistical_features(window, incoming_packets, outgoing_packets)

    # Load the models
    rf_model = joblib.load(f'rf_models/trained_rf_classifier_{delta}.pkl')
    xgb_model = joblib.load(f'xgb_models/trained_xgb_classifier_{delta}.pkl')

    # Make predictions
    rf_prediction = rf_model.predict(flow_features)
    xgb_prediction = xgb_model.predict(flow_features)

    # Display predictions
    print(f'\n{Fore.YELLOW}Random Forest prediction: {Style.RESET_ALL}{get_activity_name_from_label(rf_prediction[0])}')
    print(f'{Fore.YELLOW}XGBoost prediction: {Style.RESET_ALL}{get_activity_name_from_label(xgb_prediction[0])}')

    return rf_prediction[0], xgb_prediction[0]


# This function writes the evaluation results for each file and each window to an output file.
def write_window_results(output_evaluation_folder_path, main_folder_name, delta, window_results):
    """
    Writes evaluation results for each file and each window to an output file.

    :param output_evaluation_folder_path: The folder path where the evaluation file will be saved.
    :param main_folder_name: The name of the main evaluation folder.
    :param delta: The delta value used (e.g., window duration).
    :param window_results: Dictionary mapping file paths to lists of window prediction dictionaries.
                           Each prediction dictionary should contain "window_index", "rf_prediction", and "xgb_prediction".
    """
    output_file_path = os.path.join(output_evaluation_folder_path, f'evaluation_{main_folder_name}_{delta}_results.txt')

    with open(output_file_path, 'w') as file:
        print(f'\n{Fore.YELLOW}Writing evaluation results for folder: {Style.RESET_ALL}{main_folder_name}/evaluation set')

        file.write(f'Evaluation results for folder {main_folder_name} with delta = {delta}:\n\n')

        # Iterate over each file and write the results for each window
        for file_path, windows in window_results.items():

            # Get the file name
            file_name = file_path.split('/')[-1]

            file.write(f'File: {file_name}\n\n')
            if not windows:
                file.write('\tNo valid windows were processed.\n')
            else:
                for window in windows:
                    file.write(f'\tWindow {window["window_index"]}:\n')
                    file.write(f'\t\tStart Time (MDT): {window["start_time_mdt"]}\n')
                    file.write(f'\t\tEnd Time (MDT): {window["end_time_mdt"]}\n\n')
                    file.write(f'\t\tRandom Forest prediction: {window["rf_prediction"]}\n')
                    file.write(f'\t\tXGBoost prediction: {window["xgb_prediction"]}\n')
            file.write('\n')

        print(f'\n{Fore.GREEN}Results successfully written!{Style.RESET_ALL}')
