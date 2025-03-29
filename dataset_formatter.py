# This file contains the code for reading the dataset files and extracting the features from them.

import os
import re
import sys
import numpy as np
from colorama import Fore, Style
from scapy.layers.inet import IP
from flow_labeling import get_flow_label
from ip_addresses import get_ip_address
from utilities import read_timestamp_files, convert_timestamp, _read_pcapng_files, compute_statistical_features


# This function analyzes .pcapng files and reads .timestamps files in a folder and related subfolders
def read_training_files(folder_path, folder_name, delta):
    """
        This function iterates over all the files in the given directory, identifies pcap (.pcapng) and
        timestamps (.timestamps) files, and reads their contents. It then returns two NumPy arrays that are
        used as data and target for the classifier.

        :param folder_path: The path to the folder containing pcap and timestamps files.
        :param folder_name: The name of the folder containing the dataset
        :param delta: The delta value used for filtering packets.

        :return: A tuple of NumPy arrays representing data and target for the classifier.
    """

    dataset_features = []
    dataset_labels = []

    print(f'\n{Fore.MAGENTA}Reading training set in folder: {Style.RESET_ALL}{folder_name}')

    timestamps_cache = read_timestamp_files(folder_path)

    # Iterate over all the files in directory 'folder_path' to search for .pcap files
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:

            # Check if the file is a pcapng file
            if file_name.endswith('.pcapng'):

                file_path = os.path.join(root, file_name)

                # Retrieve current activity timestamps from timestamps cache
                activity_timestamps = timestamps_cache[file_path.split("/")[-3]]

                # Extract device name, activity name and index from the file name
                device_name = file_path.split('/')[-4]
                activity_name = file_path.split('/')[-3]
                file_index = re.match(r"(.+?)(\d+)\.pcapng", file_name).group(2)
                file_index = int(file_index)
                device_ip_address = get_ip_address(device_name)

                # Find the ip address of the current analyzed device
                if device_ip_address == -1:
                    print(f'{Fore.RED}\nERROR: No ip address found for device: {Style.RESET_ALL}{device_name}')
                    sys.exit(1)

                print(f'\n{Fore.BLUE}Reading packets from file: {Style.RESET_ALL}{file_name}')

                # Find the timestamp of the current analyzed file
                file_timestamp = activity_timestamps[file_index - 1]

                # Obtain formatted timestamp
                formatted_timestamp = convert_timestamp(file_timestamp)

                # Read packet flow from the .pcapng file
                filtered_packets = _read_pcapng_files(file_path, device_ip_address, formatted_timestamp, delta)

                # Check if the packets are empty
                if len(filtered_packets) != 0:

                    # Filter packets for out flow
                    outgoing_packets = list(
                        filter(lambda packet: packet[IP].src == device_ip_address, filtered_packets))

                    # Filter packets for in flow
                    incoming_packets = list(
                        filter(lambda packet: packet[IP].dst == device_ip_address, filtered_packets))

                    if len(outgoing_packets) != 0 and len(incoming_packets) != 0:

                        # Compute the features for this flow
                        flow_features = compute_statistical_features(filtered_packets, incoming_packets,
                                                                     outgoing_packets)

                        # Get the label of the current flow
                        label = get_flow_label(activity_name)

                        # Append label to dataset labels only if a label was found
                        if label != -1:
                            dataset_labels.append(label)
                        else:
                            print(f'{Fore.RED}\nERROR: No label found for flow: {Style.RESET_ALL}{activity_name}')
                            sys.exit(1)

                        # Append flow features to dataset features
                        dataset_features.extend(flow_features)
                                
                print(f'{Fore.GREEN}Packets successfully read!{Style.RESET_ALL}')

    print(f'\n{Fore.GREEN}Training set successfully read!{Style.RESET_ALL}')

    return np.array(dataset_features), np.array(dataset_labels)
