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
        'amazon-plug': ['192.168.1.189'],
        'blossom-sprinkler': ['192.168.1.229', '192.168.1.246'],
        'dlink-plug': ['192.168.1.199', '192.168.1.246'],
        'dlink-siren': ['192.168.1.246'],
        'ecobee-thermostat': ['192.168.1.130'],
        'hue-bulb': ['192.168.1.100'],
        'kwikset-doorlock': ['192.168.1.246'],
        'nest-thermostat': ['192.168.1.246'],
        'rachio-sprinkler': ['192.168.1.143'],
        'ring-alarm': ['192.168.1.113'],
        'roomba-vacuum-robot': ['192.168.1.246'],
        'sengled-bulb': ['192.168.1.246', '192.168.1.201'],
        'st-plug': ['192.168.1.246'],
        'tplink-bulb': ['192.168.1.246'],
        'tplink-plug': ['192.168.1.159'],
        'wemo-insight-plug': ['192.168.1.246'],
        'wemo-plug': ['192.168.1.246'],
        'blink-camera': ['192.168.1.228'],
        'google-home': ['10.42.0.179', '192.168.42.120'],
        'arlo-camera': ['192.168.1.246', '10.42.0.31'],
        'echo-dot': ['10.42.0.114'],
        'echo': ['192.168.42.74'],
        'omna-camera': ['10.42.0.32'],
        'samsung-tv': ['192.168.42.65']
    }

    # Iterate over the dictionary and return the IP address if the device name is found
    for device, ip in device_ip_dictionary.items():
        if device in device_name.lower():
            return ip

    # Return -1 if no matching IP address is found
    return -1
