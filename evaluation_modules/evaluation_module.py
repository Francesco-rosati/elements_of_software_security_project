import sys
import joblib
from colorama import Fore, Style
from scapy.layers.inet import IP
from scapy.sendrecv import sniff
from common_modules.flow_labeling import get_activity_name_from_label
from common_modules.ip_addresses import get_ip_address
from common_modules.utilities import compute_statistical_features


# This function evaluates a realistic scenario by reading packets from a pcapng file in the evaluation set
def evaluate_realistic_scenario(folder_path, delta):
    """
    :param folder_path: The path to the evaluation set folder.
    :param delta: The delta value used for filtering packets.

    :return: The classification results.
    """

    # Define file name and file path
    file_name = 'real-scenario.pcapng'
    file_path = f'{folder_path}/{file_name}'

    # Define the device names to be filtered
    device_names = ['tplink-tapo-camera', 'sonos-smart-speaker']

    # Get device IP addresses
    device_ip_addresses = []

    for device_name in device_names:
        device_ip = get_ip_address(device_name)
        if device_ip == -1:
            print(f'{Fore.RED}\nERROR: No IP address found for device: {Style.RESET_ALL}{device_name}')
            sys.exit(1)
        device_ip_addresses.append(device_ip)

    # Read packets from pcapng file

    bpf_filter = ' or '.join([f'ip host {ip}' for ip in device_ip_addresses])

    print(f'\n{Fore.BLUE}Reading packets from file: {Style.RESET_ALL}{file_path}')

    # Read packet flow from the .pcapng file
    packets = sniff(filter=bpf_filter, store=True, offline=file_path)

    print(f'{Fore.GREEN}Packets successfully read!{Style.RESET_ALL}')

    # Check if the packets are empty
    if len(packets) != 0:

        # Filter packets for out flow
        outgoing_packets = list(
            filter(lambda packet: packet[IP].src in device_ip_addresses, packets))

        # Filter packets for in flow
        incoming_packets = list(
            filter(lambda packet: packet[IP].dst in device_ip_addresses, packets))

        if len(outgoing_packets) != 0 and len(incoming_packets) != 0:
            # Compute the features for this flow
            flow_features = compute_statistical_features(packets, incoming_packets, outgoing_packets)

            rf_model = joblib.load(f'rf_models/trained_rf_classifier_{delta}.pkl')

            xgb_model = joblib.load(f'xgb_models/trained_xgb_classifier_{delta}.pkl')

            # Make predictions using the Random Forest model
            rf_prediction = rf_model.predict(flow_features)

            # Make predictions using the XGBoost model
            xgb_prediction = xgb_model.predict(flow_features)

            print(f'\n{Fore.YELLOW}Random Forest prediction: {Style.RESET_ALL}{get_activity_name_from_label(rf_prediction[0])}')
            print(f'{Fore.YELLOW}XGBoost prediction: {Style.RESET_ALL}{get_activity_name_from_label(xgb_prediction[0])}')

            # Return the predictions
            return rf_prediction[0], xgb_prediction[0]

        else:
            return None