# This file contains the code used to map the device names to the corresponding IP addresses

# This function returns the IP address associated with the device name passed as parameter
def get_ip_address(device_name):
    """
    This function returns the IP address associated with the device name passed as parameter.
    :param device_name: this is the name of the device.
    :return: the IP address associated with the device name.
    """

    # Dictionary containing the IP address for each device name
    device_ip_dictionary = {
        'tplink-tapo-camera': '192.168.1.153',
        'sonos-smart-speaker': '192.168.1.173'
    }

    # Iterate over the dictionary and return the IP address if the device name is found
    for device, ip in device_ip_dictionary.items():
        if device in device_name.lower():
            return ip

    # Return -1 if no matching IP address is found
    return -1
