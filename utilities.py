# This file contains some useful functions to read files, compute statistics and convert timestamps

import os
import sys
import pytz
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from colorama import Fore, Style


# This function reads a .timestamps file and returns a list of timestamps
def read_timestamp_files(folder_path):
    timestamps_cache = {}

    # iterate over all the files in directory 'folder_path' to search for .timestamps files
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            # check if the file is a .timestamps file
            if file_name.endswith('.timestamps'):

                timestamps = []

                timestamps_folder = root.split("/")[-2]

                if timestamps_folder not in timestamps_cache:
                    print(f'\n{Fore.BLUE}Reading timestamps from file: {Style.RESET_ALL}{file_name}')

                    file_path = os.path.join(root, file_name)

                    # read timestamps from the .timestamps file
                    with open(file_path, 'r') as file:
                        timestamps.extend(line.strip() for line in file)

                    timestamps_cache[timestamps_folder] = timestamps

                    print(f'{Fore.GREEN}Timestamps successfully read!{Style.RESET_ALL}')

    return timestamps_cache


# This function converts a timestamp in order to make it comparable with the packet timestamps
def convert_timestamp(timestamp):

    # Convert timestamp into a datetime object and return the UNIX timestamp (epoch time)
    try:

        uci_timezone = pytz.timezone('America/Los_Angeles')

        uci_datetime = datetime.strptime(timestamp, "%m/%d/%Y %I:%M:%S %p")

        uci_datetime_with_tz = uci_timezone.localize(uci_datetime)

        return uci_datetime_with_tz.timestamp()
    except ValueError:
        pass

    try:

        gmt_datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")

        gmt_datetime += timedelta(hours=1)

        return gmt_datetime.timestamp()
    except ValueError:
        print(f'{Fore.RED}\nERROR: timestamp format for {timestamp} not recognized!{Style.RESET_ALL}')
        sys.exit(1)


# This function computes the Median Absolute Deviation of the input data
def _compute_mad(data):
    # Compute the median of the data
    median_value = np.median(data, axis=0)

    # Return the median absolute deviation of the data
    return np.median(np.abs(data - median_value))


# This function takes the list of packets and returns some statistical features on it
def compute_statistical_features(packets, incoming_packets, outgoing_packets):
    # Create a list for the complete packet lengths
    packet_lengths = [len(packet) for packet in packets]
    incoming_packet_lengths = [len(packet) for packet in incoming_packets]
    outgoing_packet_lengths = [len(packet) for packet in outgoing_packets]

    # Create a Pandas data frame with statistical features for complete, incoming and outgoing flow
    df = pd.DataFrame({
        'Complete Maximum': [np.max(packet_lengths)],
        'Outgoing Maximum': [np.max(outgoing_packet_lengths)],
        'Complete Skew': [pd.Series(packet_lengths).skew()],
        'Outgoing Variance': [pd.Series(outgoing_packet_lengths).var()],
        'Outgoing Standard Deviation': [pd.Series(outgoing_packet_lengths).std()],
        'Outgoing Kurtosis': [pd.Series(outgoing_packet_lengths).kurtosis()],
        'Outgoing Skew': [pd.Series(outgoing_packet_lengths).skew()],
        'Outgoing Median Absolute Deviation': [_compute_mad(np.array(outgoing_packet_lengths))],
        'Outgoing 90th Percentile': [np.percentile(outgoing_packet_lengths, 90)],
        'Complete Mean': [np.mean(packet_lengths)],
        'Complete Kurtosis': [pd.Series(packet_lengths).kurtosis()],
        'Outgoing Mean': [np.mean(outgoing_packet_lengths)],
        'Variance': [pd.Series(packet_lengths).var()],
        'Standard Deviation': [pd.Series(packet_lengths).std()],
        'Complete 90th Percentile': [np.percentile(packet_lengths, 90)],
        'Outgoing 80th Percentile': [np.percentile(outgoing_packet_lengths, 80)],
        'Complete Median Absolute Deviation': [_compute_mad(np.array(packet_lengths))],
        'Incoming Variance': [pd.Series(incoming_packet_lengths).var()],
        'Incoming Skew': [pd.Series(incoming_packet_lengths).skew()],
        'Incoming Standard Deviation': [pd.Series(incoming_packet_lengths).std()],
        'Incoming Kurtosis': [pd.Series(incoming_packet_lengths).kurtosis()],
        'Incoming Median Absolute Deviation': [_compute_mad(np.array(incoming_packet_lengths))],
        'Complete Number of packets': [len(packet_lengths)],
        'Outgoing 70th Percentile': [np.percentile(outgoing_packet_lengths, 70)],
        'Outgoing Number of packets': [len(outgoing_packet_lengths)],
        'Incoming Number of packets': [len(incoming_packet_lengths)],
        'Incoming Mean': [np.mean(incoming_packet_lengths)],
        'Incoming 30th Percentile': [np.percentile(incoming_packet_lengths, 30)],
        'Incoming 40th Percentile': [np.percentile(incoming_packet_lengths, 40)],
        'Incoming 60th Percentile': [np.percentile(incoming_packet_lengths, 60)],
        'Complete 10th Percentile': [np.percentile(packet_lengths, 10)],
        'Complete 20th Percentile': [np.percentile(packet_lengths, 20)],
        'Incoming 50th Percentile': [np.percentile(incoming_packet_lengths, 50)],
        'Incoming 20th Percentile': [np.percentile(incoming_packet_lengths, 20)],
        'Complete 80th Percentile': [np.percentile(packet_lengths, 80)],
        'Complete 30th Percentile': [np.percentile(packet_lengths, 30)],
        'Incoming 10th Percentile': [np.percentile(incoming_packet_lengths, 10)],
        'Outgoing 60th Percentile': [np.percentile(outgoing_packet_lengths, 60)],
        'Incoming 80th Percentile': [np.percentile(incoming_packet_lengths, 80)]
    })

    return df.to_numpy()
