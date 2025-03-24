# This file contains the code for reading the dataset files and extracting the features from them.

import os
import sys
from itertools import takewhile
import numpy as np
from scapy.all import sniff
from colorama import Fore, Style
from scapy.layers.inet import IP
from flow_labeling import get_flow_label
from ip_addresses import get_ip_address
from utilities import read_timestamp_files, convert_timestamp, compute_statistical_features


# This function reads a .pcap file and returns a list of packets
def _read_pcap_files(file_path, ip_addresses):
    # filter packets by host ip address
    bpf_filter = ' or '.join([f'ip host {ip}' for ip in ip_addresses])

    return sniff(filter=bpf_filter, store=True, offline=file_path)


# This function analyzes .pcap files and reads .timestamps files in a folder and related subfolders
def read_dataset_files(folder_path, folder_name):
    """
        This function iterates over all the files in the given directory, identifies pcap (.pcap) and
        timestamps (.timestamps) files, and reads their contents. It then returns two NumPy arrays that are
        used as data and target for the classifier.

        :param folder_path: The path to the folder containing pcap and timestamps files.
        :param folder_name: The name of the folder containing the dataset

        :return: A tuple of NumPy arrays representing data and target for the classifier.
    """

    dataset_features = []
    dataset_labels = []

    print(f'\n{Fore.MAGENTA}Reading dataset in folder: {Style.RESET_ALL}{folder_name}')

    timestamps_cache = read_timestamp_files(folder_path)

    # iterate over all the files in directory 'folder_path' to search for .pcap files
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            # check if the file is a pcap file
            if file_name.endswith('.pcap'):

                file_path = os.path.join(root, file_name)

                # retrieve current folder timestamps from timestamps cache
                folder_timestamps = timestamps_cache[root.split("/")[-2]]

                device_name = file_name.split(".")[0]
                device_ip_addresses = get_ip_address(device_name)

                # find the ip address of the current analyzed device
                if device_ip_addresses == -1:
                    print(f'{Fore.RED}\nERROR: No ip address found for device: {Style.RESET_ALL}{device_name}')
                    sys.exit(1)

                print(f'\n{Fore.BLUE}Reading packets from file: {Style.RESET_ALL}{file_name}')

                # read packet flow from the .pcap file
                packets = _read_pcap_files(file_path, device_ip_addresses)

                # This function filters packets according to timestamp and a delta time (in seconds)
                delta = 20

                first_element = 0

                for timestamp in folder_timestamps:

                    # obtain formatted timestamp
                    formatted_timestamp = convert_timestamp(timestamp)

                    # find the first packet with a timestamp greater than or equal to the current timestamp
                    while first_element < len(packets) and packets[first_element].time < formatted_timestamp:
                        first_element += 1

                    # if the first packet with a timestamp greater than or equal to the current timestamp is found
                    if first_element < len(packets):
                        # filter packets according to timestamps
                        filtered_packets = list(takewhile(lambda packet: formatted_timestamp < packet.time < formatted_timestamp + delta, packets[first_element:]))

                        if len(filtered_packets) != 0:

                            # filter packets for out flow
                            outgoing_packets = list(
                                filter(lambda packet: packet[IP].src in device_ip_addresses, filtered_packets))

                            # filter packets for in flow
                            incoming_packets = list(
                                filter(lambda packet: packet[IP].dst in device_ip_addresses, filtered_packets))

                            if len(outgoing_packets) != 0 and len(incoming_packets) != 0:

                                # compute the features for this flow
                                flow_features = compute_statistical_features(filtered_packets, incoming_packets, outgoing_packets)

                                # get the label of the current flow
                                activity = root.split('/')[-2]
                                label = get_flow_label(activity)

                                # append label to dataset labels only if a label was found
                                if label != -1:
                                    dataset_labels.append(label)
                                else:
                                    print(f'{Fore.RED}\nERROR: No label found for flow: {Style.RESET_ALL}{activity}')
                                    sys.exit(1)

                                # append flow features to dataset features
                                dataset_features.extend(flow_features)

                print(f'{Fore.GREEN}Packets successfully read!{Style.RESET_ALL}')

    print(f'\n{Fore.GREEN}Dataset successfully read!{Style.RESET_ALL}')

    return np.array(dataset_features), np.array(dataset_labels)
